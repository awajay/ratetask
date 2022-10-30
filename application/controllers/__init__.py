from datetime import datetime
from flask import Blueprint, request, jsonify

from application.services import get_avg_rate

rates_bp = Blueprint('', __name__)


@rates_bp.get("/rates")
def rate():
    args = request.args
    print(args)
    if not args['origin']:
        return jsonify({"error": "origin should be non-empty"}), 400
    else:
        origin = args['origin']

    if not args['destination']:
        return jsonify({"error": "destination should be non-empty"}), 400
    else:
        destination = args['destination']

    date_from = args['date_from']
    date_to = args['date_to']
    print("Arguments are date_from:%s date_to:%s , origin:%s , destination:%s"
          % (date_from, date_to, origin, destination))

    try:
        res_from = bool(datetime.strptime(date_from, '%Y-%m-%d'))
    except ValueError:
        res_from = False
        print("Invalid date_from format:%s"
              % date_from)
        return jsonify({"error": "Invalid date_from format"}), 400

    try:
        res_to = bool(datetime.strptime(date_to, '%Y-%m-%d'))
    except ValueError:
        res_to = False
        print("Invalid date_to format:%s"
              % date_to)
        return jsonify({"error": "Invalid date_to format"}), 400

    return get_avg_rate(date_from, date_to, origin, destination)
