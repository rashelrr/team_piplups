import unittest
import requests


class test_test_app(unittest.TestCase):

    def setUp(self):
        print('setUp')
        # clear databases
        url = "https://lioneats.herokuapp.com/clear"
        requests.get(url)

    def tearDown(self):
        print('tearDown')
        # clear databases
        url = "https://lioneats.herokuapp.com/clear"
        requests.get(url)

    ''' Test login endpoint for happy case '''
    def test_login_happy(self):
        # first add an account
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "hda0101", 'password': "testpwd"}
        response = requests.post(url=url, json=data)

        assert response.status_code == 200

        # log in
        url = "https://lioneats.herokuapp.com/login"
        data = {"username": "hda0101", 'password': "testpwd"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "success"

    ''' Test login endpoint for wrong password given'''
    def test_login_invalid_wrong_pwd(self):
        # first add an account
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "abc1234", 'password': "testpwd"}
        response = requests.post(url=url, json=data)

        assert response.status_code == 200

        # now try logging in with incorrect password
        url = "https://lioneats.herokuapp.com/login"
        data = {"username": "abc1234", 'password': "idek"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "wrong password"

    ''' Test login endpoint for an account that does not exist '''
    def test_login_invalid_account_not_exist(self):
        url = "https://lioneats.herokuapp.com/login"
        data = {"username": "xyz1234", 'password': "testpwd"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "account not exist"

    ''' Test signup endpoint for happy case '''
    def test_signup_happy(self):
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "abc1234", 'password': "pwdtest"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "success"

    ''' Test signup endpoint for account that already exists '''
    def test_signup_invalid_account_exists(self):
        # add account
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "jdi8367", 'password': "greenapples"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200

        # attempt signup with previous account
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "jdi8367", 'password': "greenapples"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "account exists"

    # checks edit review endpoint given the user logged in
    def test_edit_review_logged_in(self):
        url = "https://lioneats.herokuapp.com/editreview"
        data = {"uni": "yy3131"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response_body["status"] == "success"

    # checks edit review search endpoint given a valid restaurant
    def test_edit_review_search_valid(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        self.assertEqual(200, response.status_code)
        url = "https://lioneats.herokuapp.com/edit_review_search"
        data = {"uni": "yy3131", "res": "fumo"}
        response = requests.post(url=url, json=data)
        response_body = response.json()
        assert response_body["status"] == "success"

    # checks edit review search endpoint given an invalid restaurant
    def test_edit_review_search_invalid(self):
        url = "https://lioneats.herokuapp.com/edit_review_search"
        data = {"uni": "yy3131", "res": "random"}
        response = requests.post(url=url, json=data)
        self.assertEqual(response.json()["status"], "fail")

    # checks update star and review endpoint given both required inputs
    def test_update_star_and_review(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        self.assertEqual(200, response.status_code)

        url = "https://lioneats.herokuapp.com/update_star_and_review"
        data = {"star": 4, "review": "my go to place", "uni": "yy3131",
                "res": "fumo"}
        response = requests.post(url=url, json=data)
        self.assertEqual(response.status_code, 200)

    ''' ############ BELOW: TO FIX ############ '''

    '''


    # checks edit review endpoint given invalid parameters
    # aka updated review has empty parameters
    def test_edit_review_invalid(self):
        url = "http://127.0.0.1:5000/editreview"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        reason = "To edit a review, please enter all required fields."
        assert response_body["reason"] == reason

    # Checks readreviews endpoint if given a valid restaurant name
    def test_read_reviews_happy_given_restaurant(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=fumo"
        response = requests.get(url)

        assert response.status_code == 200

        response_body = response.json()
        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['fumo', 3, 'mediocre sandwich', 'rdr2139'],
                       ['fumo', 2, 'good pizza', 'yy3131']]
        assert response_body["valid"] is True
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews endpoint if given an invalid restaurant name
    # aka restaurant does not exist in db
    def test_read_reviews_invalid_restaurant(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=dunkin"
        response = requests.get(url)

        assert response.status_code == 200

        response_body = response.json()
        assert response_body["valid"] is False
        reason = "There are no reviews for that restaurant."
        assert response_body["reason"] == reason

    # Checks readreviews endpoint if given a valid rating
    def test_read_reviews_happy_given_rating(self):
        url = "http://127.0.0.1:5000/readreviews?stars=4"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['koronet', 4, 'huge slices', 'mg4145'],
                       ['koronet', 5, 'best pizza ever', 'rdr2139'],
                       ['koronet', 5, 'constant craving', 'yy3131'],
                       ['nussbaum', 4, 'friendly staff', 'mg4145'],
                       ['nussbaum', 5, 'good drinks', 'sa3892'],
                       ['panda express', 4, 'good but expensive', 'dl3410'],
                       ['panda express', 5, 'good service', 'mg4145'],
                       ['panda express', 5, 'great noodles', 'sa3892']]
        assert response_body["valid"] is True
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews endpoint if given an invalid rating
    # aka no reviews in db so no reviews match the query
    def test_read_reviews_invalid_rating(self):
        db.clear()
        db.init_db()
        url = "http://127.0.0.1:5000/readreviews?stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        reason = "There are no reviews at/above that rating."
        assert response_body["reason"] == reason

    # Checks readreviews function if given a valid rest/rating
    def test_read_reviews_happy_given_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=fumo&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['fumo', 3, 'mediocre sandwich', 'rdr2139']]
        assert response_body["valid"] is True
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews function if given an invalid rest/rating
    # aka query does not exist in database
    def test_read_reviews_invalid_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=mcdonalds&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        reason = "There are no reviews matching your query."
        assert response_body["reason"] == reason

    # checks add review endpoint given valid parameters
    def test_add_review_happy(self):
        url = ("http://127.0.0.1:5000/addreview?"
               + "restaurant=dunkin&stars=5&review=AMAZING!&uni=rdr2139")
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is True
        assert response_body["reason"] == "Successfully added review."

    # checks add review endpoint given invalid parameters
    # aka user already reviewed restaurant and thus cannot
    # add review to db
    def test_add_review_already_reviewed(self):
        url = ("http://127.0.0.1:5000/addreview?"
               + "restaurant=fumo&stars=5&review=AMAZING!&uni=rdr2139")

        print(">>>", url)
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        reason = "You've already reviewed this restaurant."
        assert response_body["reason"] == reason

    # checks add review endpoint given invalid parameters
    # aka empty parameters
    def test_add_review_invalid(self):
        url = "http://127.0.0.1:5000/addreview"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        reason = "To add a review, please enter all required fields."
        assert response_body["reason"] == reason'''
