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
        print(response)
        assert response.status_code == 200
