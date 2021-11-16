import unittest
import app
import requests


class Test_TestApp(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    '''Tests / endpoint, checks status code is 200'''
    def test_index_check_status_code_equals_200(self):
        url = "http://127.0.0.1:5000/"
        response = requests.get(url)
        assert response.status_code == 200

    # Checks readreviews function if given a valid restaurant name
    def test_read_reviews_happy_given_restaurant(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=fumo"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()
        assert response_body["restaurant"] == "fumo"

        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['fumo', 3, 'mediocre sandwich', 'rdr2139'],
                       ['fumo', 2, 'good pizza', 'yy3131']]
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews function if given an invalid restaurant name
    # aka name does not exist in db
    def test_read_reviews_invalid_restaurant(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=dunkin"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()
        assert response_body["restaurant"] == "dunkin"

        assert response_body["reviews"] == []

    # Checks readreviews function if given a valid rating
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
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews function if given an invalid rating
    # aka invalid int for stars rating (range allowed is 1-5)
    def test_read_reviews_invalid_rating(self):
        url = "http://127.0.0.1:5000/readreviews?stars=6"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = []
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews function if given an invalid type for rating
    # as it should be an int
    def test_read_reviews_invalid_type_rating(self):
        url = "http://127.0.0.1:5000/readreviews?stars=hello"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Rating must be an integer."

    # Checks readreviews function if given a valid rest/rating
    def test_read_reviews_happy_given_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=fumo&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['fumo', 3, 'mediocre sandwich', 'rdr2139']]
        assert response_body["reviews"] == exp_reviews

    # Checks readreviews function if given an invalid rest/rating
    # aka restaurant does not exist in database
    def test_read_reviews_invalid_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=mcdonalds&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["reviews"] == []

    # Checks readreviews function if given an invalid rest/rating
    # aka empty parameters
    def test_read_reviews_invalid_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=&stars="
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Invalid query. Please enter at least one field."

    # checks edit review endpoint given valid parameters
    def test_edit_review_happy(self):
        url = "http://127.0.0.1:5000/editreview?restaurant=fumo&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is True
        assert response_body["reason"] == "Successfully edited review."

    # checks edit review endpoint given invalid parameters
    # aka some parameters empty
    def test_edit_review_invalid(self):
        url = "http://127.0.0.1:5000/editreview?restaurant=fumo&stars=&review=meh&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Please enter all fields."

    # checks add review endpoint given valid parameters
    def test_add_review_happy(self):
        url = "http://127.0.0.1:5000/addreview?restaurant=dunkin&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is True
        assert response_body["reason"] == "Successfully added review."

    # checks add review endpoint given invalid parameters
    # aka user already reviewed restaurant and thus cannot 
    # add review to db
    def test_add_review_invalid(self):
        url = "http://127.0.0.1:5000/addreview?restaurant=fumo&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. You have already reviewed this restaurant."
