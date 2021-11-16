import unittest
import db
import sqlite3


class Test_TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect("Lion_Eats")

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

        # add a review with star rating bigger than 5
        db.add_review(("Magic Tea", 9, "expensive price",
                       "dl3410"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "magic tea";""")
        row = cur.fetchall()
        self.assertFalse(row)

        # add a review with incomplete information 
        db.add_review(("Fumo", 5))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "fumo";""")
        row = cur.fetchall()
        self.assertFalse(row)

        # add a blank review 
        db.clear()
        db.init_db()
        db.add_review("")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS;""")
        rows = cur.fetchall()
        self.assertFalse(rows)

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

        # editing a review with a star rating bigger than 5
        db.edit_review("yy3131", "Junzi", 10, "Junzi the best")
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

    def test_get_review(self):
        db.clear()
        db.init_db()

        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        
        db.add_review(("Koronets", 3, "good food and great service",
                     "dl3410"))

        #review that doesn't exist
        row = db.get_review("aaaa", "eeee")
        self.assertFalse(row)

        #review that does exist
        row2 = db.get_review("koronets", "dl3410")
        #self.assertTrue(row2)

    def test_get_restaurants_above_ratings(self):
        db.clear()
        db.init_db()
        db.add_review(("Shake Shack", 3, "good food and great service",
                    "yy3131"))
        db.add_review(("Shake Shack", 3, "good food and great service",
                    "dl3410"))
        db.add_review(("Ferris", 3, "good food and great service",
                    "yy3131"))
      
        rows = db.get_restaurants_above_ratings("5")
        self.assertFalse(rows)

        db.add_review(("Shake Shack", 5, "amazing!",
                    "mg4145"))
        rows = db.get_restaurants_above_ratings(2)
        self.assertTrue(rows)
