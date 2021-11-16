# Team Piplups - Members

- Rashel Rojas - rdr2139
- Mauricio Guerrero - mg4145
- Daisy Ye - yy3131
- Dayna Lee - dl3410
- Sana Ahmed - sa3892


## How to Build/Run Service:
Enter into the terminal `python3 app.py` or run `make run` from provided Makefile. 


## How to Test Service:
- Postman was used for testing GET and POST requests. 
  - See the Collections in Postman and run.
- Additionally, you can test the service by using the provided URLs in our API documentation.
  - To do this run the service and go to the base URL to create the database.
  - Once there you can use `sqlitebrowser Lion_Eats` to see the database.
    - You can reload the database as you see fit. 
    - It is highly suggested you do so for addreview and editreview
- Sample Tests: 
  - http://127.0.0.1:5000/ 
  - http://127.0.0.1:5000/readreviews?restaurant=Fumo
  - http://127.0.0.1:5000/readreviews?stars=1
  - http://127.0.0.1:5000/addreview?restaurant=koronet&stars4=&review=delicious&uni=mg4145


## API Documentation

**Base URL for all endpoints:** http://127.0.0.1:5000/

**Endpoints:** 
- GET
  - http://127.0.0.1:5000/
  - http://127.0.0.1:5000/readreviews?restaurant=&stars=&
    - User may enter one or more parameters 
- GET / POST
  - http://127.0.0.1:5000/addreview?restaurant=&stars=&review=&uni=
    - User must enter all parameters   
  - http://127.0.0.1:5000/editreview?restaurant=&stars=&review=&uni=
    - User must enter all parameters

**URL Parameters:**
- restaurant=[string]
- stars=[integer]
- review=[string]
- uni=[string]
