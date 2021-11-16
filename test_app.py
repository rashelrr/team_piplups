import unittest
import app
import requests


class Test_TestApp(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')

    def test_index_check_status_code_equals_200(self):
        url = "http://127.0.0.1:5000/"
        response = requests.get(url)
        assert response.status_code == 200

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

    def test_read_reviews_invalid_restaurant(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=dunkin"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()
        assert response_body["restaurant"] == "dunkin"

        assert response_body["reviews"] == []


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

    def test_read_reviews_invalid_rating(self):
        url = "http://127.0.0.1:5000/readreviews?stars=6"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = []
        assert response_body["reviews"] == exp_reviews

    def test_read_reviews_invalid_type_rating(self):
        url = "http://127.0.0.1:5000/readreviews?stars=hello"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Rating must be an integer."


    def test_read_reviews_happy_given_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=fumo&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        exp_reviews = [['fumo', 5, 'Great pasta', 'mg4145'],
                       ['fumo', 3, 'mediocre sandwich', 'rdr2139']]
        assert response_body["reviews"] == exp_reviews

    def test_read_reviews_invalid_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=mcdonalds&stars=3"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["reviews"] == []

    def test_read_reviews_invalid_rest_and_rating(self):
        url = "http://127.0.0.1:5000/readreviews?restaurant=&stars="
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Invalid query. Please enter at leastone field."


    def test_edit_review_happy(self):
        url = "http://127.0.0.1:5000/editreview?restaurant=fumo&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is True
        assert response_body["reason"] == "Successfully edited review."

    def test_edit_review_invalid(self):
        url = "http://127.0.0.1:5000/editreview?restaurant=&stars=3&review=meh&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. Please enter all fields."
    
    def test_add_review_happy(self):
        url = "http://127.0.0.1:5000/addreview?restaurant=dunkin&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is True
        assert response_body["reason"] == "Successfully added review."


    def test_add_review_invalid(self):
        url = "http://127.0.0.1:5000/addreview?restaurant=fumo&stars=5&review=AMAZING!&uni=rdr2139"
        response = requests.get(url)

        assert response.status_code == 200
        response_body = response.json()

        assert response_body["valid"] is False
        assert response_body["reason"] == "Error. You have already reviewed thisrestaurant."
