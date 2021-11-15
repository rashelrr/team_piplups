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
                    "Junzi";""")
        rows = cur.fetchall()
        self.assertTrue(rows)

        db.add_review(("Junzi", "4", "make a redundant comment",
                       "yy3131"))
        self.conn = sqlite3.connect("Lion_Eats")
        cur = self.conn.cursor()
        cur.execute("""SELECT count(*) from REVIEWS WHERE restaurant_name = 
                    "Junzi";""")
        count = cur.fetchall()
        self.assertEqual(count[0][0], 1)

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