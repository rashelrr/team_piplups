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
  - Home page http://127.0.0.1:5000/ 
    - Clears and creates table for storing reviews submitted by users
    - Expects users to choose an action: login, signup, select a restaurant to see reviews, view all restaurants, view all restaurants above a certain rating, or add a review
  - Home page http://127.0.0.1:5000/home
    - Expects users to Expects users to choose an action: select a restaurant to see reviews, view all restaurants, view all restaurants above a certain rating, add a review, or edit a review
  - http://127.0.0.1:5000/readreviews?restaurant=---&stars=-
    - Retrieves reviews matching the query, aka reviews for a restaurant and/or
      x stars and above
    - User must enter one or both parameters
- GET / POST
  - Signup page http://127.0.0.1:5000/signup
    - Creates an account for users if they do not already have an account
    - Expects the user to enter a valid username and password and submit via the signup button
  - Login page http://127.0.0.1:5000/login
    - Logs the user in with the a username and password credential
    - Expects the user to enter a valid username and corresponding password
  - Restaurant display page http://127.0.0.1:5000/rest_display_all?
    - Displays all restaurants and average star rating across all reviews
    - Expects users to enter the name of a restaurant to see reviews for that restaurant
  - Restaurant display page https://127.0.0.1/rest_display_star_filter?star=---
    - Displays all restaurants and average star rating across all reviews for restaurants whose average rating is above the number specified by the user
    - Expects users to enter the name of a restaurant to see reviews for that restaurant
  - http://127.0.0.1:5000/addreview?restaurant=---&stars=---&review=---&uni=---
    - Adds review to database if user hasn't already reviewed that restaurant
    - User must enter all parameters   
  - http://127.0.0.1:5000/editreview?restaurant=&stars=&review=&uni=
    - When a user has already reviewed a restaurant but wants to edit that
      review.
    - User must enter all parameters
- GET
  - Restaurant review page http://127.0.0.1:5000/rest_info?name=---
    - Displays all reviews (star rating, review, uni) for a specified restaurant
    - Expects users select radio button to filter reviews at or above 


**URL Parameters:**
- restaurant=[string] (case-insensitive)
- stars=[integer]
- review=[string]
- uni=[string]        (case-insensitive)

