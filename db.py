import sqlite3
from sqlite3 import Error
import csv

def init_db():
    # creates tables REVIEWS and UNI
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
        print('Database Online, tables created')
    except Error as e:
        print(e)

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
        cur.execute("SELECT * FROM REVIEWS WHERE restaurant_name=?", (res_name,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get reviews for a restaurant')
        return rows

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
def get_all_reviews_for_restaurant_given_rating(res_name, rating):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("SELECT * FROM REVIEWS where restaurant_name=? AND star >=?", (res_name, rating,))
        rows = cur.fetchall()
        conn.commit()
        print('Database Online, get reviews for a restaurant at/above a rating')
        return rows
    except Error as e:
        print(e)
        return None

    finally:
        if conn:    
            conn.close()

### currently unused!
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
        print('Database Online, get reviews above restaurant\'s average rating rating')
        return rows
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
def edit_review(UNI, res_name, new_rating, new_review):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute("update REVIEWS set star = ?, review = ? where UNI = ? and restaurant_name = ?",
                    (new_rating, new_review, UNI, res_name,))
        conn.commit()
        print('Database Online, review edited')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

'''
row: tuple (restaurant_name, star, review, UNI)
Adds new review to database
'''
def add_review(row):
    conn = None
    try:
        conn = sqlite3.connect('Lion_Eats')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO REVIEWS (restaurant_name, star, review, UNI) VALUES (?, ?, ?, ?)", row)
        conn.commit()
        print('Database Online, review added')
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
