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

## CI for Service: Travis CI
  - Click the green check mark at the top of the repo. Click 'Details' next to Travis
    CI. Click 'The build'. Travis CI will open in a new tab.
  - Under 'Job log' shows the CI report. Here you can see Travis runs our unit tests, 
    coverage tool, style checker, and Postman system tests for the service.

## Style Checker: Flake8
  - Report (bugs.txt) is in our repo 

## Coverage Tool: Coverage.py
  - Travis displays the coverage percentage for test_app.py and test_db.py under 'Job log'
  - The folder htmlcov/ in our repo also has test_app.py and test_db.py that you can open 
    on your computer to view the coverage percentages (download repo, run 'coverage html' 
    in terminal and then open up those files in htmlcov folder).

## Bug Finder: SonarCloud
  - Click the green check mark at the top of the repo. Click 'Details' next to SonarCloud
    and then 'View more details on SonarCloud.'

## System Tests for Service:
- Postman was used for testing GET and POST requests. 
  - See the Collections in Postman for our workspace.


## API Documentation:

**Endpoints:** 
- GET
  - Clear https://lioneats.herokuapp.com/clear 
    - Clears and creates tables for storing reviews submitted by users and user accounts 
...

- POST
  - Login https://lioneats.herokuapp.com/login
    - Allows users to login to LionEats client app.
...


----below needs to be updated for heroku----

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
    - User can enter the name of a restaurant they want the edit the review for
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

