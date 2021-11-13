import sqlite3
from sqlite3 import Error
import csv

# creates tables REVIEWS and UNI

def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        conn.execute("""CREATE TABLE IF NOT EXISTS REVIEWS(restaurant_name TEXT NOT NULL, 
                    star INT NOT NULL,
                    review TEXT NOT NULL, 
                    UNI varchar(7) NOT NULL,
                    PRIMARY KEY(restaurant_name, UNI));""")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS UNI(UNI varchar(7) NOT NULL, PRIMARY KEY(UNI))""")
        cur = conn.cursor()
        
        reviews_file = open("review.csv")
        rows = csv.reader(reviews_file)
        cur.executemany("INSERT INTO REVIEWS VALUES (?, ?, ?, ?)", rows)

        #uni_file = open("uni.csv")
        #rows = csv.reader(uni_file)
        #cur.executemany("INSERT INTO REVIEWS VALUES (?)", rows)

        conn.commit()
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


# find all review by a certain restaurant name 
def get_review_by_name(resName):
    # will return review or None if db fails
    # 1. specific restaurant
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS WHERE restaurant_name=?", (resName,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get all reviews of a restaurant')
        return rows

    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()

# given a rating, return all reviews above that rating 
def get_all_reviews_above_rating(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where star >= ?", (rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get all reviews above a rating')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:    
            conn.close()
        

def get_all_above_rating_res(rating, resName):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where star >=? AND restaurant_name=?", rating, resName)
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get all reviews above a rating')
        return rows
    except Error as e:
        print(e)
        return None


# given a rating, compute and average rating for each restaurant and return restaurant_name + star for the restaurants above that rating 
def get_restaurants_above_ratings(rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("with avg_table as \
            (select restaurant_name, avg(star) as avg_star_rating from REVIEWS group by restaurant_name) \
                select * from avg_table where avg_star_rating >= ?", (rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get all reviews above restaurant\'s average rating rating')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()

# given UNI and restaurant name, update the table with a new star and a new review for that row 
def edit_review(UNI, rest_name, new_star, new_review):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("update REVIEWS set star = ?, review = ? where UNI = ? and restaurant_name = ?",
                    new_star, new_review, UNI, rest_name)
        conn.commit()
        print('Database Online, edit review')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

# add review takes in a tuple (restaurant_name, star, review, UNI) and add it to the database 
def add_review(row):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO REVIEWS (restaurant_name, star, review, UNI) VALUES (?, ?, ?, ?)", row)
        conn.commit()
        print('Database Online, add a review')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

# clears both tables 
def clear():
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
