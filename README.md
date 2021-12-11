# Team Piplups - Members
- Rashel Rojas - rdr2139
- Mauricio Guerrero - mg4145
- Daisy Ye - yy3131
- Dayna Lee - dl3410
- Sana Ahmed - sa3892

## About LionEats
Our service allows users to read and leave reviews for restaurants near campus
and around NYC.

## How to Build/Run Service/Client:
To run the client: Download the repo and enter into the terminal 'python3 app.py'.

## CI, Bug Checker, Style Checker, Coverage for Service:
- CI: Travis CI
  - Click the green check mark at the top of the repo. Click 'Details' next to Travis
    CI. Click 'The build'. Travis CI will open in a new tab. The job log shows the CI's
    actions. 'View config' shows that Travis CI runs our style checker and coverage tool.
- Style Checker: Flake8
  - Report (bugs.txt) is in our repo 
- Coverage Tool: Coverage.py
  - Travis displays the coverage percentage for test_app.py and test_db.py under 'Job log'
  - The folder htmlcov/ in our repo also has test_app.py and test_db.py that you can open 
    on your computer to view the coverage percentages.
- Bug Finder: SonarCloud
  - Click the green check mark at the top of the repo. Click 'Details' next to SonarCloud
    and then 'View more details on SonarCloud.'

## System Tests for Service:
- Postman was used for testing GET and POST requests. 
  - See the Collections in Postman for system tests and run.

## Unit Tests for Service:
- To run unit tests using VS Code, enter "Python: Configure Tests" and select
  unittest. You will then be prompted to select the directory of where the tests 
  are located and finally choose "test_*.py".
  - Then enter 'coverage run -m unittest discover' to view tests that passed. 

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

