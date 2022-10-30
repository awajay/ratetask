# Average rate API
Average rate calculation API. API will return the response from the date_from to date_to for given origin and destination
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
 <b>&emsp; * Running on http://127.0.0.1:5000  </b> <br>

<b>To deactivate virtual environment use below command </b>
<br>&emsp; venv\Scripts\deactivate.bat <br>

<h2> API endpoint</h2>
<br>
POST http://127.0.0.1:5000/rates?date_from=date_from&date_to=date_to&origin=origin&destination=destination
<br>
     * query param values - date_from, date_to, origin, destination  <br>
     * date format should be: YYYY-MM-DD <br>  
     * origin/destination should have PORT code or region slug <br>
<h3> Response </h3><br>

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
  <h2> Error Response </h2>
  <br><b>
  
  &emsp;1. If origin/ destination is empty </b>
  <br>&emsp;GET (http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=)
  <br>
  <br>&emsp; Response is as -  ![image](https://user-images.githubusercontent.com/17041004/198880045-888a039f-6c8a-4726-8062-c1426ce51040.png)
  <br><br><b>
    &emsp;2. If date_from/date_to are not valid </b>
  <br>&emsp;GET (http://127.0.0.1:5000/rates?date_from=2016-01-32&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main)
  <br>
  <br>&emsp; Response is as - ![image](https://user-images.githubusercontent.com/17041004/198880132-e22defd5-8919-43af-9aea-36a0b1d8d66a.png)
  <br>
  <br><b>
  &emsp;3. If DATABASE_URL have incorrect password or configuration is not present or db connection not established </b>
  <br>&emsp; Change DATABASE_URL for test as - 
  ![image](https://user-images.githubusercontent.com/17041004/198881626-7ab9ce4c-0476-4a54-83c5-6c5ff0da8f54.png)

  <br>&emsp; GET (http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main)
  <br>
  <br>&emsp; Response is as - ![image](https://user-images.githubusercontent.com/17041004/198880815-c8569fe7-4eb3-412b-83a8-5d11d4db66bc.png)
  <br>
  <br>

  <h2> Contact </h2>
  <br>&emsp;
  For any query please email on : <b> ajayawasthimca@gmail.com </b>
  
