# Team Piplups - Members

- Rashel Rojas - rdr2139
- Mauricio Guerrero - mg4145
- Daisy Ye - yy3131
- Dayna Lee - dl3410
- Sana Ahmed - sa3892


## How to Build/Run Service:
Enter into the terminal `python3 app.py` or `make run`. 

## How to Test Service:
- Postman was used for testing GET and POST requests. 
  - See the Collections in Postman for system tests and run.

- Additionally, you can test the service by using the provided URLs in our API
  documentation.
  - To do this, run the service and go to the base URL ('http://127.0.0.1:5000/')
    to create the necessary database tables.
  - Once there you can enter `sqlitebrowser Lion_Eats` into another terminal to
    view the contents of the database.
    - Reload sqlitebrowser (Ctrl+R) after running addreview and editreview
      endpoints to view the new changes

- To run unit tests using VS Code, enter "Python: Configure Tests" and select
  unittest. You will then be prompted to select the directory of where the tests are
  located and finally choose "test_*.py".
  - Then enter 'coverage run -m unittest discover' to view cases that passed.
  - Important: Before running unit tests, make sure that the service is running
    locally, aka that http://127.0.0.1:5000/ is running. This is because
    test_app.py requires that the service is running.

- Sample Tests: 
  - http://127.0.0.1:5000/ 
  - http://127.0.0.1:5000/readreviews?restaurant=Fumo
  - http://127.0.0.1:5000/readreviews?stars=1
  - http://127.0.0.1:5000/addreview?restaurant=koronet&stars4=&review=delicious&uni=mg4145
 

## API Documentation:

**Endpoints:** 
- GET
  - http://127.0.0.1:5000/
    - Clears and creates table for storing reviews submitted by users
  - http://127.0.0.1:5000/readreviews?restaurant=---&stars=-
    - Retrieves reviews matching the query, aka reviews for a restaurant and/or
      x stars and above
    - User must enter one or both parameters
- GET / POST
  - http://127.0.0.1:5000/addreview?restaurant=---&stars=---&review=---&uni=---
    - Adds review to database if user hasn't already reviewed that restaurant
    - User must enter all parameters   
  - http://127.0.0.1:5000/editreview?restaurant=&stars=&review=&uni=
    - When a user has already reviewed a restaurant but wants to edit that
      review.
    - User must enter all parameters


**URL Parameters:**
- restaurant=[string] (case-insensitive)
- stars=[integer]
- review=[string]
- uni=[string]        (case-insensitive)


## Note for Second Iteration: Dealing with Invalid Types/Empty Fields
- In our UI for readreviews/add review/edit review, user must select one of
  five checkboxes. This allows us to restrict the user from entering anything
  other than an int and an int in the allowed range (1-5). Thus, there is no
  need to check if the passed rating is a valid value.
- Also, if the user tries to (1) submit a query for readreviews (2) submit a
  review (3) submit an edited review without filling all of the required
  fields, then our .js files will create the following endpoints:
  - 'http://127.0.0.1:5000/readreviews'
  - 'http://127.0.0.1:5000/addreview'
  - 'http://127.0.0.1:5000/editreview'
- When these endpoints are processed in app.py, error messages will be
  returned via jsonify such as 'Please enter all required fields' back to the
  frontend. This is how we will deal with empty fields.
