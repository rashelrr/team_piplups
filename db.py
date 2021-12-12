import sqlite3
from sqlite3 import Error
import csv


def init_db():
    # creates tables REVIEWS and UNI: which store reviews and user accounts
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
        conn.commit()
        print('Database Online, tables created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


# inserts dummy data for testing purposes only
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
        print('Database Online, get password given uni')
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
        uni = str(uni)
        cur.execute("SELECT * FROM UNI where UNI = ?", (uni.lower(),))
        rows = cur.fetchall()
        if rows is None or len(rows) == 0:
            print("Uni not found in db, signup is allowed.")
            return False
        print("Error: Uni found, please log in.")
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
            print("Error: uni field is empty")
            return Error
        if password is None or password == "":
            print("Error: password is empty")
            return Error
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        if check_if_uni_exists(uni) is True:
            print("Uni exists, cannot add account")
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
Returns   all reviews for a specific restaurant as a dictionary
'''


def get_all_reviews_for_restaurant(res_name):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS")
        rows = cur.fetchall()
        name = []
        star = []
        review = []
        uni = []
        for r in rows:
            if r[0] == res_name.lower():
                name.append(r[0])
                star.append(r[1])
                review.append(r[2])
                uni.append(r[3])
        conn.commit()
        print('Database Online, get reviews for a restaurant')
        return dict(Name=name, Star_Rating=star, Review=review, UNI=uni)

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
rating: int
rows:   list of tuples: [ (entire review 1), (entire review 2), ... ]
Returns all reviews at and above a star rating
'''


def get_all_reviews_given_rating(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where star >= ?", (rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get reviews at and above a rating')
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
Returns all reviews for a restaurant at/above a star rating in dictionary form
'''


def get_all_reviews_for_rest_given_rating(res_name, rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where restaurant_name=?\
            AND star >=?", (res_name.lower(), rating,))
        rows = cur.fetchall()
        name = []
        star = []
        review = []
        uni = []
        for r in rows:
            name.append(r[0])
            star.append(r[1])
            review.append(r[2])
            uni.append(r[3])

        conn.commit()
        print('Database Online, get reviews for a restaurant at\
              above a rating')
        return dict(Name=name, Star_Rating=star, Review=review, UNI=uni)

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
rating: int
Given a rating, get average rating for each restaurant
and return those with an avg rating >= rating as a dictionary
'''


def get_restaurants_above_ratings(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("with avg_table as (select restaurant_name, avg(star) as\
            avg_star_rating from REVIEWS group by restaurant_name)\
                select * from avg_table")
        rows = cur.fetchall()
        name = []
        star = []
        for r in rows:
            if r[1] >= int(rating):
                name.append(r[0])
                star.append(r[1])
        conn.commit()
        print('Database Online, get restaurants with avg rating at/above '
              'given rating')
        return dict(Name=name, Average_Rating=star)
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
res_name, uni: string
row: a review
Returns review that matches the res_name and uni
'''


def get_review_uni_res(res_name, uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where restaurant_name=? AND UNI=?",
                    (res_name.lower(), uni))
        rows = cur.fetchall()
        print('Database Online, get review given a uni and restaurant')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
    res_name, uni: string
    row: the review column
    Returns only the review column that matches the res_name and uni
'''


def get_only_review_uni_res(res_name, uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT review FROM REVIEWS where restaurant_name=? \
                    AND UNI=?", (res_name.lower(), uni))
        rows = cur.fetchall()
        print('Database Online, get review column given a uni and restaurant')
        return rows[0][0]
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
    res, uni: string
    ans: star rating given a restaurant and uni
    Returns the star rating given a restaurant and uni
'''


def get_star_uni_res(uni, res):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT star FROM REVIEWS where UNI=? and \
                    restaurant_name=?", (uni, res.lower()))
        ans = cur.fetchall()
        return ans[0][0]
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
    res_name, uni: string
    rows: all reviews given a uni
    Returns all reviews that matches the uni
'''


def get_review_uni(uni):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where UNI=?",
                    (uni, ))
        rows = cur.fetchall()
        conn.commit()
        name = []
        star = []
        review = []
        uni = []
        for r in rows:
            name.append(r[0])
            star.append(r[1])
            review.append(r[2])
            uni.append(r[3])
        print('Database Online, get review given a uni')
        return dict(Name=name, Star_Rating=star, Review=review, UNI=uni)
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
UNI, res_name, new_review:  string
new_star:                   int
Updates a single review in database
'''


def edit_review(uni, res_name, new_rating, new_review):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        lower_uni = uni.lower()
        lower_res_name = res_name.lower()
        cur.execute("update REVIEWS set star = ?, review = ? where UNI = ? and\
            restaurant_name = ?",
                    (new_rating, new_review, lower_uni, lower_res_name))
        conn.commit()
        print('Database Online, edited review')
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
        print('Database Online, added review')
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
