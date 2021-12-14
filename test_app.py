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

        assert response_body['status_code'] == str(200)
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

        assert response_body['status_code'] == str(500)
        assert response_body['reason'] == "wrong password"

    ''' Test login endpoint for an account that does not exist '''
    def test_login_invalid_account_not_exist(self):
        url = "https://lioneats.herokuapp.com/login"
        data = {"username": "xyz1234", 'password': "testpwd"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response_body['status_code'] == str(500)
        assert response_body['reason'] == "account not exist"

    ''' Test signup endpoint for happy case '''
    def test_signup_happy(self):
        url = "https://lioneats.herokuapp.com/signup"
        data = {"username": "abc1234", 'password': "pwdtest"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response_body['status_code'] == str(200)
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

        assert response_body['status_code'] == str(500)
        assert response_body['reason'] == "account exists"

    ''' Test addreview endpoint for happy case'''
    def test_addreview_happy(self):
        # valid add review request
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': "Fumo", 'stars': 5, 'review': "Good",
                'user': "dl3410"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['status'] == "success"

    ''' Test addreview endpoint for case when user tries
    to add a review for a restaurant they've already reviewed'''
    def test_addreview_invalid(self):
        # valid add review request
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': "Fumo", 'stars': 5, 'review': "Good",
                'user': "dl3410"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response.status_code == 200

        # try adding a duplicate review
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': "Fumo", 'stars': 5, 'review': "Good",
                'user': "dl3410"}
        response = requests.post(url=url, json=data)
        response_body = response.json()
        assert response_body['status'] == "failure"
        assert response_body['status_code'] == str(500)

    # checks edit review endpoint given the user logged in
    def test_edit_review_logged_in(self):
        url = "https://lioneats.herokuapp.com/editreview"
        data = {"uni": "yy3131"}
        response = requests.post(url=url, json=data)
        response_body = response.json()

        assert response_body['status_code'] == str(200)
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
        assert response_body['status_code'] == str(200)
        assert response_body["status"] == "success"

    # checks edit review search endpoint given an invalid restaurant
    def test_edit_review_search_invalid(self):
        url = "https://lioneats.herokuapp.com/edit_review_search"
        data = {"uni": "yy3131", "res": "random"}
        response = requests.post(url=url, json=data)
        self.assertEqual(response.json()["status"], "failure")
        assert response.json()['status_code'] == str(500)

    # checks update star and review endpoint given both required inputs
    def test_update_star_and_review(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        self.assertEqual(200, response.status_code)
        assert response.json()['status_code'] == str(200)

        url = "https://lioneats.herokuapp.com/update_star_and_review"
        data = {"star": 4, "review": "my go to place", "uni": "yy3131",
                "res": "fumo"}
        response = requests.post(url=url, json=data)
        self.assertEqual(response.status_code, 200)
        assert response.json()['status_code'] == str(200)

    # Checks rest_display endpoint for all restaurants
    def test_rest_display_all_happy(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_display"
        data = {"star": 1}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=['fumo'], Average_Rating=[4])
        assert response_body["res"] == exp_review

    # Checks rest_display endpoint for restaurants above a certain rating
    def test_rest_display_filter_happy(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"
        data = {'restaurant': 'koronet', 'stars': 1, 'review': 'bad food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_display"
        data = {"star": 4}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=['fumo'], Average_Rating=[4])
        assert response_body["res"] == exp_review

    # Checks rest_display endpoint when there are no restaurants
    def test_rest_display_none_happy(self):
        url = "https://lioneats.herokuapp.com/rest_display"
        data = {"star": 1}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=[], Average_Rating=[])
        assert response_body["res"] == exp_review

    # Checks rest_display endpoint for an invalid star rating
    def test_rest_display_filter_invalid(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_display"
        data = {"star": 6}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=[], Average_Rating=[])
        assert response_body["res"] == exp_review

    # Checks rest_info endpoint for all reviews
    def test_rest_info_happy(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"
        data = {'restaurant': 'fumo', 'stars': 1, 'review': 'bad food',
                'user': 'sa3892'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_info"
        data = {'name': 'fumo', 'star': 1}
        response = requests.get(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=['fumo', 'fumo'], Review=['bad food',
                          'good food'], Star_Rating=[1, 4], UNI=['sa3892',
                          'yy3131'])
        assert response_body["res"] == exp_review

    # Checks rest_info endpoint for reviews above a certain rating
    def test_rest_info_filter_happy(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"
        data = {'restaurant': 'fumo', 'stars': 1, 'review': 'bad food',
                'user': 'sa3892'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_info"
        data = {'name': 'fumo', 'star': 4}
        response = requests.get(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=['fumo'], Review=['good food'],
                          Star_Rating=[4], UNI=['yy3131'])
        assert response_body["res"] == exp_review

        url = "https://lioneats.herokuapp.com/rest_info"
        data = {'name': 'fumo', 'star': 5}
        response = requests.get(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=[], Review=[], Star_Rating=[], UNI=[])
        assert response_body["res"] == exp_review

    # Checks rest_info endpoint for restaurant that doesn't exist
    def test_rest_info_invalid(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_info"
        data = {'name': 'koronet', 'star': 1}
        response = requests.get(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=[], Review=[], Star_Rating=[], UNI=[])
        assert response_body["res"] == exp_review

    # Checks rest_info endpoint for star rating that doesn't exist
    def test_rest_info_filter_invalid(self):
        url = "https://lioneats.herokuapp.com/addreview"
        data = {'restaurant': 'fumo', 'stars': 4, 'review': 'good food',
                'user': 'yy3131'}
        response = requests.post(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        url = "https://lioneats.herokuapp.com/rest_info"
        data = {'name': 'fumo', 'star': 6}
        response = requests.get(url=url, json=data)
        assert response.json()['status_code'] == str(200)
        assert response.json()['status'] == "success"

        response_body = response.json()
        exp_review = dict(Name=[], Review=[], Star_Rating=[], UNI=[])
        assert response_body["res"] == exp_review
