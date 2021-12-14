# Team Piplups - Members
- Rashel Rojas - rdr2139
- Mauricio Guerrero - mg4145
- Daisy Ye - yy3131
- Dayna Lee - dl3410
- Sana Ahmed - sa3892

## About LionEats
Our service allows users to read and leave reviews for restaurants near campus
and around NYC.

## How to Run Service:
Service is hosted here: https://lioneats.herokuapp.com/

## How to Run Client:
Download the repo and enter into the terminal 'python3 client_app.py'.
Now enter "http://127.0.0.1:5000/" into the browser and navigate through the client!
- While testing, if you attempt to login and you run into a loop in which the client 
  keeps bringing you back and forth between the login and singup page, run this in
  the browser: https://lioneats.herokuapp.com/clear

## CI for Service: Travis CI
  - Click the green check mark at the top of the repo. Click 'Details' next to Travis
    CI. Click 'The build'. Travis CI will open in a new tab.
  - Under 'Job log' shows the CI report. Here you can see Travis runs our unit tests, 
    coverage tool, and style checker.

## Style Checker: Flake8
  - Report (bugs.txt) is in our repo 

## Coverage Tool: Coverage.py
  - Travis displays the coverage percentage for test_app.py and test_db.py under 'Job log'
  - The folder htmlcov/ in our repo also has test_app.py and test_db.py that you can open 
    on your computer to view the coverage percentages (download repo, run 'coverage html' 
    in terminal and then open up those files from htmlcov folder).

## Bug Finder: SonarCloud
  - Click the green check mark at the top of the repo. Click 'Details' next to SonarCloud
    and then 'View more details on SonarCloud.'

## System Tests for Service:
- Postman was used for testing GET and POST requests. 
  - See the Collections in Postman for our workspace.


## API Documentation:

**Endpoints:** 
- GET
  - Homepage https://lioneats.herokuapp.com/ 
    - Creates tables for storing reviews submitted by users and user accounts
      if the tables didn't already exist 
    - Does not return anything except for a welcome message to the user
  - Clear https://lioneats.herokuapp.com/clear 
    - Deletes then creates tables for storing reviews submitted by users and user accounts
    - Does not return anything
  - Edit review https://lioneats.herokuapp.com/editreview
    - When a user is logged in and clicks on the Edit review button
    - Displays all the review made by this user and has a search engine for the user to edit a review for a specific restaurant
    - returns status_code 200 and success 
    - if the user is not logged in yet, this page will redirect to the login page 
  - Edit Review Search https://lioneats.herokuapp.com/edit_review_search
    - When a user clicks on the submit button after putting in a restaurant name 
    - will display error message if restaurant is not found (status_code = 500)
    - returns status code 200 if the review is successfully found 
    - if the review exists, will show the page that the user can put in the new rating and review 
- POST
  - Login https://lioneats.herokuapp.com/login
    - Allows users to login to LionEats client app
    - Assumes user logs in with a string username and password
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful login, 500 if failure
    - Failure messages returned if username/password does not exist as an account
    > Example Json Response: {"status":"wrong password", "status_code":"500"}
  - Signup https://lioneats.herokuapp.com/signup
    - Allows users to sign up to LionEats client app
    - Assumes user signs up with a string username and password
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful signup, 500 if failure
    - Failure messages returned if username is already linked to an account
    > Example Json Response: {"status":"account exists", "status_code":"500"}
  - Add Review https://lioneats.herokuapp.com/addreview
    - Allows users to add reviews to the database
    - Assumes given valid uni
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful add, 500 if failure
    - Faiure messages returned if there is already a review left at the restaurant by the username 
    > Example Json Response: {"status":"failure", "status_code":"500"}
  - Update star and Review https://lioneats.herokuapp.com/update_star_and_review 
    - When the user puts in both the new star and new review and hit submit, he/she will be redirected to the edit review page 
    - returns status code 200 
    - the user has to update both fields because they are required


---- @team: below needs to be updated for heroku----
Example assumption: All API entries assume the client’s user already has an account on Facebook and is currently logged into Facebook
Example expectation: The /do_something endpoint expects a date in YYYY-MM-DD format, a length of time in HH:MM 24-hour format, and an activity_name string of length minimum 8 characters and maximum 64 characters
Ideally, your documentation should also include a usage example for each API entry with both a request and possible responses (including error codes)

  - Restaurant display http://127.0.0.1:5000/rest_display_all?
    - Displays all restaurants and average star rating across all reviews
    - User can enter the name of a restaurant to see reviews for that restaurant
  - Restaurant display https://127.0.0.1/rest_display_star_filter?star=---
    - Displays all restaurants and average star rating across all reviews for restaurants whose average rating is above the number specified by the user
    - User can enter the name of a restaurant to see reviews for that restaurant
    - User must enter all parameters
  - Add review http://127.0.0.1:5000/preaddreview
    - Displays form for users to fill out
    - User must enter all fields given
    - add_review()
      - Helper method
      - Adds review to the database if user hasn't already reviewed the restaurant
      - Sends popup if review is sucessfully added
  - Update Review http://127.0.0.1:5000/update_star_and_review
    - When the user clicks "submit" button on edit review page (and added updated review (star rating, review) for a specified restaurant, given UNI, to the database)
    - Displays all reviews (restaurant name, star rating, review, and uni) a user has left
    - User must enter all parameters
- GET
  - Restaurant review page http://127.0.0.1:5000/rest_info?name=---
    - Displays all reviews (star rating, review, uni) for a specified restaurant
    - User can select radio button to filter reviews at or above the specified number
    - User must enter all parameters
  - Restaurant review page http://127.0.0.1:5000/rest_info?star=---&name=---
    - Displays all reviews (star rating, review, uni) that are above the specified number
    - User must enter all parameters
  - Edit review page http://127.0.0.1:5000/edit_review_search?name=---
    - Displays a review (star rating, review, uni) for a specific restaurant given UNI
    - User must enter all parameters (UNI, restaurant name)

