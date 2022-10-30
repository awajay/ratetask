import os

import psycopg2
from dotenv.main import DotEnv
from flask import jsonify

# geo code check query
PORT_CODE_CHECK = "select parent_slug from PORTS where code = (%s)"

# final response attribute
AVG_FINAL_PREFIX_Q = "select to_char(day,'YYYY-MM-DD'),round(avg(average),0),count(*) from ("

# generate date series
DATE_SERIES_START_STR = AVG_FINAL_PREFIX_Q + "select * from  ( select day::date FROM generate_series(date(%s), " \
                                             "date(%s), interval  '1 day') day ) d LEFT JOIN ("
DATE_SERIES_END_STR = " ) t using(day) "

AVG_RATE_INITIAL_Q_STR = DATE_SERIES_START_STR + "select day," \
                                                 "avg(price) as average from prices " \
                                                 "group by day, orig_code,dest_code " \
                                                 "having day>=(%s) and day<=(%s) and "
AVR_RATE_END_SUFFIX = DATE_SERIES_END_STR + ") as avgbygeo group by day order by day"

# SIMPLE CASE QUERY PORT CODE identified in PORTS itself
AVG_RATE_BY_PORT_CODE_Q = AVG_RATE_INITIAL_Q_STR + "orig_code =(%s) and dest_code =(%s) " + AVR_RATE_END_SUFFIX

# origin matched with PORT.CODE and destination matched with REGIONS.slug = PORT.PARENT_SLUG
AVG_RATE_BY_ORIG_C_DEST_SLUG_Q = AVG_RATE_INITIAL_Q_STR + "orig_code = (%s) and dest_code in ( " \
                                                          "select code from ports p, regions r " \
                                                          "where p.parent_slug = r.slug and (" \
                                                          "r.parent_slug = (%s) or  p.parent_slug =(%s)))" \
                                 + AVR_RATE_END_SUFFIX
# destination matched with PORT.CODE and origin matched with REGIONS.slug = PORT.PARENT_SLUG
AVG_RATE_BY_ORIG_SLUG_DEST_C_Q = AVG_RATE_INITIAL_Q_STR + "orig_code in ( select code from ports p, regions r where " \
                                                          "p.parent_slug = r.slug and (r.parent_slug = (%s) or  " \
                                                          "p.parent_slug = (%s)) ) and dest_code=(%s) " \
                                 + AVR_RATE_END_SUFFIX
# origin and destination matched with REGIONS.slug = PORT.PARENT_SLUG
AVG_RATE_BY_ORIG_DEST_SLUG_Q = AVG_RATE_INITIAL_Q_STR + "orig_code in ( select code from ports p, regions r where " \
                                                        "p.parent_slug = r.slug and (r.parent_slug = (%s) or  " \
                                                        "p.parent_slug = (%s)) ) and dest_code in ( select code from " \
                                                        "ports p, regions r where p.parent_slug = r.slug and (" \
                                                        "r.parent_slug = (%s) or  p.parent_slug = (%s)) ) " \
                               + AVR_RATE_END_SUFFIX


def avg_rate_response(avg_rate_list):
    average_price = []
    print(avg_rate_list)
    for avg_price in avg_rate_list:
        if isinstance(avg_price[2], int) and avg_price[2] > 2:
            average_price.append({"day": avg_price[0], "average_price": avg_price[1]})
        else:
            average_price.append({"day": avg_price[0], "average_price": 'null'})
    return average_price


def get_db_conn():
    db_url = os.environ.get("DATABASE_URL")
    print("DB URL:%s" % db_url)
    if not db_url:
        print("DATABASE_URL configuration not present")
        connection = None
    else:
        try:
            connection = psycopg2.connect(db_url)
        except Exception as err:
            print(err)
            connection = None
    return connection


def get_avg_rate(date_from, date_to, origin, destination):
    orig_code_flag = False
    dest_code_flag = False
    connection = get_db_conn()
    if not connection:
        return jsonify({"error": "db connection fail. Please check log for detail"}), 500
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(PORT_CODE_CHECK, (origin,))
                is_code = cursor.fetchall()
                if is_code:
                    orig_code_flag = True

                cursor.execute(PORT_CODE_CHECK, (destination,))
                is_code = cursor.fetchall()
                if is_code:
                    dest_code_flag = True
                # origin and destination input are not matched with code
                if orig_code_flag is False and dest_code_flag is False:
                    print(
                        "origin and destination are matched with slug only. Query is :'%s'" % AVG_RATE_BY_ORIG_DEST_SLUG_Q)
                    cursor.execute(AVG_RATE_BY_ORIG_DEST_SLUG_Q,
                                   (date_from, date_to, date_from, date_to, origin, origin, destination, destination,))
                    avg_rate_list = cursor.fetchall()
                # check orig_code is in PORTS or not
                elif orig_code_flag is True:
                    # check dest_code is in PORTS or not
                    if dest_code_flag is True:
                        print("origin and destination matched with code. Query is :'%s'" % AVG_RATE_BY_ORIG_DEST_SLUG_Q)
                        cursor.execute(AVG_RATE_BY_PORT_CODE_Q,
                                       (date_from, date_to, date_from, date_to,
                                        origin,
                                        destination,))
                        avg_rate_list = cursor.fetchall()
                    else:
                        print("origin matched with code and destination matched with slug. Query is :'%s'"
                              % AVG_RATE_BY_ORIG_C_DEST_SLUG_Q)
                        # check for slug to get dest_code
                        cursor.execute(AVG_RATE_BY_ORIG_C_DEST_SLUG_Q,
                                       (date_from, date_to, date_from, date_to, origin, destination, destination,))
                        avg_rate_list = cursor.fetchall()
                else:
                    if dest_code_flag is True:
                        print("origin matched with slug and destination matched with code. Query is: %s"
                              % AVG_RATE_BY_ORIG_SLUG_DEST_C_Q)
                        cursor.execute(AVG_RATE_BY_ORIG_SLUG_DEST_C_Q,
                                       (date_from, date_to, date_from, date_to, origin,
                                        origin, destination,))
                        avg_rate_list = cursor.fetchall()
                if not avg_rate_list:
                    print("empty avg_rate_list by origin:%s and destination:%s" % (origin, destination))
                return jsonify(avg_rate_response(avg_rate_list))
    except Exception as err:
        print(err)
        return jsonify({"error": str(err)}), 500
