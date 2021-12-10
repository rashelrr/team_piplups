import unittest
import db
import sqlite3


class Test_TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect("Lion_Eats")

    def test_add_uni_passcode(self):
        # add first account
        db.clear()
        db.init_db()
        db.add_uni_passcode('yy3131', 'Ye010730')
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from UNI WHERE UNI =
                    "yy3131";""")
        rows = cur.fetchall()
        self.assertTrue(rows)

        # should not be able to add redundant accounts
        db.add_uni_passcode('yy3131', '010730')
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT count(*) from UNI WHERE UNI =
                    "yy3131";""")
        rows = cur.fetchall()
        self.assertEqual(rows[0][0], 1)

        # should not be able to add empty UNI (empty account name)
        db.add_uni_passcode('', '010730')
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT count(*) from UNI WHERE UNI =
                    "";""")
        rows = cur.fetchall()
        self.assertEqual(rows[0][0], 0)

        # should not be able to add empty password (empty account name)
        db.add_uni_passcode('dl3410', '')
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT count(*) from UNI WHERE UNI =
                    "dl3410";""")
        rows = cur.fetchall()
        self.assertEqual(rows[0][0], 0)

    def test_get_password(self):
        db.clear()
        db.init_db()
        db.add_uni_passcode('dl3410', 'daeun4200')
        result = db.get_password('dl3410')
        self.assertEqual(result[0][0], 'daeun4200')

        # getting a password when the UNI does not exist
        result = db.get_password('yy3131')
        self.assertFalse(result)

    def test_check_if_uni_exists(self):
        db.clear()
        db.init_db()
        db.add_uni_passcode('dl3410', 'daeun4200')
        result = db.check_if_uni_exists('dl3410')
        self.assertEqual(result, True)

        # try to find a user that does not exist
        result = db.check_if_uni_exists('yy3131')
        self.assertEqual(result, False)

    def test_add_review(self):
        # normal add review
        db.clear()
        db.init_db()
        db.add_review(("Junzi", 3, "good food and great service",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "junzi";""")
        rows = cur.fetchall()
        self.assertTrue(rows)

        # add a review that already exists (UNI and res_name already in db)
        db.add_review(("Junzi", 4, "make a redundant comment",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "junzi" and star = "4";""")
        row = cur.fetchall()
        self.assertFalse(row)

    def test_edit_review(self):
        # normal edit review
        db.clear()
        db.init_db()
        db.add_review(("Junzi", 4, "make a redundant comment",
                       "YY3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT star from REVIEWS WHERE restaurant_name =
                    "junzi";""")
        star = cur.fetchall()
        self.assertEqual(star[0][0], 4)
        db.edit_review("yy3131", "Junzi", 5, "I love Junzi")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT star from REVIEWS WHERE restaurant_name =
                    "junzi";""")
        star = cur.fetchall()
        self.assertEqual(star[0][0], 5)

        # editing a review that does not exist yet
        db.edit_review("yy3131", "fumo", 3, "fumo is my fav italian place")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "fumo";""")
        row = cur.fetchall()
        self.assertFalse(row)

        # editing a review with incorrect order of information as parameter
        db.edit_review("yy3131", "Junzi", "I hate junzi", 1)
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "junzi" and star = 1;""")
        row = cur.fetchall()
        self.assertFalse(row)

    def test_delete_review(self):
        # normal delete review
        db.clear()
        db.init_db()
        db.add_review(("Junzi", 3, "good food and great service",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "junzi";""")
        row = cur.fetchall()
        self.assertTrue(row)
        db.delete_review("YY3131", "JUNZI")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "junzi";""")
        row = cur.fetchall()
        self.assertFalse(row)

        # delete a row that does not exist
        db.delete_review("YY3131", "MAGIC TEA")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name =
                    "magic tea";""")
        row = cur.fetchall()
        self.assertFalse(row)

    def test_get_restaurants_above_ratings(self):
        db.clear()
        db.init_db()
        db.add_review(("Shake Shack", 3, "good food and great service",
                       "yy3131"))
        db.add_review(("Shake Shack", 5, "good food and great service",
                       "dl3410"))
        db.add_review(("Ferris", 3, "good food and great service",
                       "yy3131"))

        rows = db.get_restaurants_above_ratings("5")
        self.assertFalse(rows['Name'])

        db.add_review(("Shake Shack", 5, "amazing!",
                      "mg4145"))
        rows = db.get_restaurants_above_ratings("4")
        self.assertTrue(rows['Name'])

    def test_get_all_reviews_for_restaurant(self):
        db.clear()
        db.init_db()
        self.conn = sqlite3.connect("Lion_Eats")

        db.add_review(("Junzi", 3, "good food and great service", "yy3131"))

        # normal get
        rows = db.get_all_reviews_for_restaurant("junzi")
        self.assertTrue(rows['Name'])

        # get reviews for restaurant that doesn't exist
        rows = db.get_all_reviews_for_restaurant("magic tea")
        self.assertFalse(rows['Name'])

        # get reviews for blank restaurant
        rows = db.get_all_reviews_for_restaurant("")
        self.assertFalse(rows['Name'])

    
    def test_get_all_reviews_given_rating(self):
        db.clear()
        db.init_db()
        self.conn = sqlite3.connect("Lion_Eats")

        db.add_review(("junzi", 5, "good food and great service",
                      "yy3131"))
        # normal get
        rows = db.get_all_reviews_given_rating(5)
        self.assertTrue(rows)

    def test_get_all_reviews_for_rest_given_rating(self):
        db.clear()
        db.init_db()
        self.conn = sqlite3.connect("Lion_Eats")
        db.add_review(("junzi", 3, "good food and great service",
                      "yy3131"))

        # normal get
        rows = db.get_all_reviews_for_rest_given_rating("junzi", "3")
        self.assertTrue(rows['Name'])

        # get reviews with incomplete information
        rows = db.get_all_reviews_for_rest_given_rating("", "3")
        self.assertFalse(rows['Name'])

        # get reviews with no information
        rows = db.get_all_reviews_for_rest_given_rating("", "")
        self.assertFalse(rows['Name'])

        # get reviews for rating that doesn't exist (ex. the restaurant given
        # has no reviews above 4 stars)
        rows = db.get_all_reviews_for_rest_given_rating("junzi", "4")
        self.assertFalse(rows['Name'])

    def test_get_review_uni(self):
        db.clear()
        db.init_db()
        self.conn = sqlite3.connect("Lion_Eats")
        
        db.add_review(("Koronets", 3, "good food and great service", "dl3410"))

        # uni that doesn't exist
        rows = db.get_review_uni("eeee")
        self.assertFalse(rows['Name'])

        # review that does exist
        rows = db.get_review_uni("dl3410")
        self.assertTrue(rows['Name'])

        def test_get_review_uni_res(self):
            db.clear()
            db.init_db()
            self.conn = sqlite3.connect("Lion_Eats")

            db.add_review(("Koronets", 3, "good food and great service", "dl3410"))

            # normal get
            rows = db.get_review_uni_res("Koronets", "dl3410")
            self.assertTrue(rows)

            # uni that doesn't exist
            rows = db.get_review_uni_res("Koronets", "sa3892")
            self.assertFalse(rows)

            # restaurant that doesn't exist
            rows = db.get_review_uni_res("fumo", "dl3410")
            self.assertFalse(rows)

            # uni and restaurant that don't exist
            rows = db.get_review_uni_res("fumo", "sa3892")
            self.assertFalse(rows)

            # fields are empty
            rows = db.get_review_uni_res("", "dl3410")
            self.assertFalse(rows)
            rows = db.get_review_uni_res("Koronets", "")
            self.assertFalse(rows)
