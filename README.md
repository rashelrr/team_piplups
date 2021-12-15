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
  - Restaurant Display Filter https://lioneats.herokuapp.com/rest_display?star=---
    - Displays the restaurants in the database whose average rating is at or above the specified number and their average rating
    - The user is directed here when they selects a numbered radio button and hit filter on the homepage
    - The user must select a radio button before filtering
    - Allows the user to enter a restaurant name to see its reviews
    - Returns status code 200
  - Restaurant Reviews https://lioneats.herokuapp.com/rest_info?name=---
    - Displays all reviews (star rating, review, uni) for a specified restaurant
    - User can select radio button to filter reviews at or above the specified number
    - The user is directed here when they enter a restaurant name into the search box and hit the view button from either the home page or either restaurant display page
    - User must enter a restaurant name before they can view the reviews
    - Returns status code 200
  - Restaurant Review Filter https://lioneats.herokuapp.com/rest_info?star=---&name=---
    - Displays all reviews (star rating, review, uni) for a specified restaurant at or above the specified number
    - User can select radio button to filter reviews again or select the see all reviews button to see all reviews again
    - The user is directed here when they select a radio button on the restaurant reviews page
    - User must enter a star number before they can view the reviews
    - Returns status code 200
- POST
  - Login https://lioneats.herokuapp.com/login
    - Allows users to login to LionEats client app
    - Assumes user logs in with a string username and password
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful login, 500 if failure
    - Failure messages returned if username/password does not exist as an account
    > Example Json Response: {"status_code":"500", "status":"failure", "reason":"wrong password"}
  - Signup https://lioneats.herokuapp.com/signup
    - Allows users to sign up to LionEats client app
    - Assumes user signs up with a string username and password
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful signup, 500 if failure
    - Failure messages returned if username is already linked to an account
    > Example Json Response: {"status_code":"500", "status":"failure", "reason":"account exists"}
  - Add Review https://lioneats.herokuapp.com/addreview
    - Allows users to add reviews to the database
    - Assumes given valid uni
    - Endpoint returns success/failure messages as json through 'response'
    - Returns status code of 200 for successful add, 500 if failure
    - Faiure messages returned if there is already a review left at the restaurant by the username 
    > Example Json Response: {"status_code":"500", "status":"failure", "reason":"already reviewed this restaurant"}
  - Update star and Review https://lioneats.herokuapp.com/update_star_and_review 
    - When the user puts in both the new star and new review and hit submit, he/she will be redirected to the edit review page 
    - returns status code 200 
    - the user has to update both fields because they are required
  - Restaurant Display All https://lioneats.herokuapp.com/rest_display
    - Displays all the restaurants in the database and their average rating
    - The user is directed here when they click the see all restaurants button on the homepage
    - Allows the user to enter a restaurant name to see its reviews
    - Returns status code 200
