import unittest
import db
import sqlite3


class Test_TestDB(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect("Lion_Eats")

    def test_add_review(self):
        db.clear()
        db.init_db()
        db.add_review(("Junzi", "3", "good food and great service",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "junzi";""")
        rows = cur.fetchall()
        self.assertTrue(rows)

        db.add_review(("Junzi", "4", "make a redundant comment",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "junzi" and star = "4";""")
        row = cur.fetchall()
        self.assertFalse(row)

        db.add_review(("Magic Tea", "9", "expensive price",
                       "dl3410"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "magic tea";""")
        row = cur.fetchall()
        self.assertFalse(row)

        db.add_review(("Fumo", "5"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS WHERE restaurant_name = 
                    "fumo";""")
        row = cur.fetchall()
        self.assertFalse(row)

        db.clear()
        db.init_db()
        db.add_review("")
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT * from REVIEWS;""")
        rows = cur.fetchall()
        self.assertFalse(rows)

    # def test_get_all_reviews_for_restaurant(self):
    #     db.init_db()
    #     db.get_all_reviews_for_restaurant()