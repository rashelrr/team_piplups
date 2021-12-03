import sqlite3
from sqlite3 import Error
import csv


def init_db():
    # creates tables REVIEWS and UNI
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        conn.execute("""CREATE TABLE IF NOT EXISTS \
            REVIEWS(restaurant_name TEXT NOT NULL,
                    star INT NOT NULL,
                    review TEXT NOT NULL,
                    UNI varchar(7) NOT NULL,
                    PRIMARY KEY(restaurant_name, UNI));""")
        conn.execute("""CREATE TABLE IF NOT EXISTS UNI(UNI varchar(7) NOT NULL,\
            passcode TEXT NOT NULL, \
            PRIMARY KEY(UNI))""")

        # cur = conn.cursor()
        # reviews_file = open("review.csv")
        # rows = csv.reader(reviews_file)
        # cur.executemany("INSERT INTO REVIEWS VALUES (?, ?, ?, ?)", rows)
        #  uni_file = open("uni.csv")
        #  rows = csv.reader(uni_file)
        #  cur.executemany("INSERT INTO REVIEWS VALUES (?)", rows)
        conn.commit()
        print('Database Online, tables created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


# inserts dummy data for testing
def insert_dummy_data():
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        reviews_file = open("review.csv")
        rows = csv.reader(reviews_file)
        cur.executemany("INSERT INTO REVIEWS VALUES (?, ?, ?, ?)", rows)
        reviews_file.close()
        conn.commit()
        print('Database Online, dummy data added')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
uni: UNI
rows:     passcode
Returns   passcode given a UNI
'''


def get_password(uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT passcode FROM UNI where UNI = ?", (uni.lower(),))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get passcode given a UNI')
        return rows

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
uni: UNI
Returns   False if user does not exist, True if user exists
'''


def check_if_uni_exists(uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM UNI where UNI = ?", (uni.lower(),))
        rows = cur.fetchall()
        if rows is None or len(rows) == 0:
            print("UNI not found, signup is allowed.")
            return False
        print("UNI found, please log in.")
        return True

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
uni: UNI
password: password to add
Returns   the new row added, error if uni exists already
'''


def add_uni_passcode(uni, password):
    conn = None
    try:
        if uni is None or uni == "":
            print("Error: adding a blank UNI")
            return Error
        if password is None or password == "":
            print("Error: cannot add blank password")
            return Error
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        if check_if_uni_exists(uni) is True:
            print("UNI exists, cannot add")
            return Error
        cur.execute("INSERT INTO UNI (UNI, passcode) VALUES\
                (?, ?)", (uni.lower(), password))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, new account added')
        return rows

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
res_name: string
rows:     list of tuples: [ (entire review 1), (entire review 2), ... ]
Returns   all reviews for a specific restaurant
'''


def get_all_reviews_for_restaurant(res_name):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS")
        rows = cur.fetchall()
        result = []
        for r in rows:
            if r[0] == res_name.lower():
                result.append(r)
        conn.commit()
        print('Database Online, get reviews for a restaurant')
        return result

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
rating: int
rows:   list of tuples: [ (entire review 1), (entire review 2), ... ]
Returns all reviews at/above a star rating
'''


def get_all_reviews_given_rating(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where star >= ?", (rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get reviews at/above a rating')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
res_name: string
rating:   int
rows:     list of tuples: [ (entire review 1), (entire review 2), ... ]
Returns all reviews for a restaurant at/above a star rating
'''


def get_all_reviews_for_rest_given_rating(res_name, rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where restaurant_name=?\
            AND star >=?", (res_name.lower(), rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get reviews for a restaurant at\
              above a rating')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()

# currently unused!
# given a rating, compute and average rating for each restaurant
# and return restaurant_name + star for the restaurants above that rating


def get_restaurants_above_ratings(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("with avg_table as (select restaurant_name, avg(star) as\
            avg_star_rating from REVIEWS group by restaurant_name)\
                select * from avg_table")
        rows = cur.fetchall()
        result = []
        for r in rows:
            if r[1] >= int(rating):
                result.append(r[0])
        conn.commit()
        print('Database Online, get reviews above restaurant\'s average '
              + 'rating')
        return result
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
    res_name, uni: string
    row: an entire review
    Returns review that matches the res_name and uni
'''


def get_review(res_name, uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where restaurant_name=? AND UNI=?",
                    (res_name.lower(), uni))
        row = cur.fetchone()
        conn.commit()
        print('Database Online, get review')
        return row
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
UNI, res_name, new_review:  string
new_star:                   int
uni and res_name are lowercased before adding update
Updates a single review in database
'''


def edit_review(UNI, res_name, new_rating, new_review):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        lower_UNI = UNI.lower()
        lower_res_name = res_name.lower()
        cur.execute("update REVIEWS set star = ?, review = ? where UNI = ? and\
            restaurant_name = ?",
                    (new_rating, new_review, lower_UNI, lower_res_name))
        conn.commit()
        print('Database Online, review edited')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
row: tuple (restaurant_name, star, review, UNI)
uni and restaurant name are lowercased before inserting
Adds new review to database
'''


def add_review(row):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        new_row = (row[0].lower(), row[1], row[2], row[3].lower())
        cur.execute(
            "INSERT INTO REVIEWS (restaurant_name, star, review, UNI) VALUES\
                (?, ?, ?, ?)", new_row)
        conn.commit()
        print('Database Online, review added')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Given UNI and restaurant name, delete review from database
'''


def delete_review(UNI, res_name):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        new_UNI = UNI.lower()
        new_res_name = res_name.lower()
        cur.execute(
            """DELETE FROM REVIEWS where UNI = ? and restaurant_name = ?""",
            (new_UNI, new_res_name))
        conn.commit()
        print('Database Online, review deleted')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def clear():
    # clears both tables
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        conn.execute("DROP TABLE IF EXISTS REVIEWS")
        conn.execute("DROP TABLE IF EXISTS UNI")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
