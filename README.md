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
  - Home http://127.0.0.1:5000/ 
    - Clears and creates table for storing reviews submitted by users
    - Users can choose an action: login, signup, select a restaurant to see reviews, view all restaurants, view all restaurants above a certain rating, or add a review
  - Home http://127.0.0.1:5000/home
    - Takes away signup and login options from / endpoint and adds edit review option
    - Users can choose an action: select a restaurant to see reviews, view all restaurants, view all restaurants above a certain rating, add a review, or edit a review
- GET / POST
  - Signup http://127.0.0.1:5000/signup
    - Creates an account for users if they do not already have an account
  - Login http://127.0.0.1:5000/login
    - Logs the user in with the a username and password credential
    - User must enter a username that exists in the database and the corresponding password
  - Restaurant display http://127.0.0.1:5000/rest_display_all?
    - Displays all restaurants and average star rating across all reviews
    - User can enter the name of a restaurant to see reviews for that restaurant
  - Restaurant display https://127.0.0.1/rest_display_star_filter?star=---
    - Displays all restaurants and average star rating across all reviews for restaurants whose average rating is above the number specified by the user
    - User can enter the name of a restaurant to see reviews for that restaurant
    - User must enter all parameters
  - Edit review http://127.0.0.1:5000/editreview
    - When a user has already reviewed a restaurant but wants to edit that review
    - Displays all reviews (restaurant name, star rating, review, and uni) a user has left
    - User can enter the name of a restaurant they want the edit the review for
    - User must enter all parameters
  - Add review http://127.0.0.1:5000/preaddreview
    - Displays form for users to fill out
    - User must enter all fields given
    - add_review()
      - Helper method
      - Adds review to the database if user hasn't already reviewed the restaurant
      - Sends popup if review is sucessfully added
- GET
  - Restaurant review page http://127.0.0.1:5000/rest_info?name=---
    - Displays all reviews (star rating, review, uni) for a specified restaurant
    - User can select radio button to filter reviews at or above the specified number
    - User must enter all parameters
  - Restaurant review page http://127.0.0.1:5000/rest_info?star=---&name=---
    - Displays all reviews (star rating, review, uni) that are above the specified number
    - User must enter all parameters


**URL Parameters:**
- restaurant=[string] (case-insensitive)
- stars=[integer]
- review=[string]
- uni=[string]        (case-insensitive)

