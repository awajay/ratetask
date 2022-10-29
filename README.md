# Average rate API
Average rate calculation API. API will return the response for the range of dates , for given origin and destination
<h1> Steps for run </h1>
1) clone repository <br>
2) change DATABASE_URL value as per your environment <br>

&emsp;   DATABASE_URL variable exist in .env file as below <br>
  &emsp;<b><i>DATABASE_URL=postgresql://postgres:ratetask@localhost:5432/postgres</I></b>
  <br>
   &emsp;Here example is for localhost means postgres is installed on local machine 
  <br>
   &emsp;There will be user postgres , password in ratetask and database name is postgres
<br>
3) install virtual environment ( if not install )
<br>
&emsp; pip install virtualenv
<br>
4) create virtual environment from below command <br>
&emsp;python -m venv venv <br>
5) Activate virtual environment from below command in command prompt
<br>&emsp; . venv\Scripts\activate.bat
<br> <b> In Windows below command will be used for activate virtual env </b>
<br>&emsp; venv\Scripts\activate.bat <br>
6) install required package using below command <br>
&emsp;   pip install -r requirement.txt <br>
7) to run app execute below command in command prompt <br>
<b>&emsp;   flask run </b><br>
&emsp; if getting below line then your environment is working fine  <br>
 <b>&emsp; * Running on http://127.0.0.1:5000 <br>

<b>To deactivate virtual environment use below command </b>
<br>&emsp; venv\Scripts\deactivate.bat <br>

<h2> API endpoint</h2>
<br>
POST http://127.0.0.1:5000/rates?date_from=date_from&date_to=date_to&origin=origin&destination=destination
<br>
     * query param values - date_from, date_to, origin, destination  <br>
     * date format should be: YYYY-MM-DD <br>  
     * origin/destination should have PORT code or region slug <br>
<h3>
Response </h3><br>

[
  {
    "day": "YYYY-MM-DD",
    "average_price": "average_price"
  },
  {
    "day": "YYYY-MM-DD",
    "average_price": "null"
  },
  ...
  ...
]
 
   
