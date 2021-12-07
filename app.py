from flask import Flask, render_template, jsonify, request, redirect,\
    url_for, flash, abort
import db
import logging
import secrets

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

'''
Homepage
'''

uni = 'abc1234'


@app.route('/', methods=['GET'])
def index():
    db.clear()
    db.init_db()
    db.insert_dummy_data()
    return render_template('homepage.html', uni=uni)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uni = request.form['username']
        password = request.form['password']
        if db.check_if_uni_exists(uni) is True:
            if db.get_password(uni)[0][0] == password:
                return redirect("http://127.0.0.1:5000/")
            else:
                # flash('Error: Password is wrong, try again.')
                return redirect(url_for('login'))
        else:
            # flash('Error: Account does not exist, please sign up')
            return redirect(url_for('signup'))
    else:
        return render_template('login.html')


''' Example: http://127.0.0.1:5000/login?UNI=abc4321&passcode=cows '''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        uni = request.form['username']
        password = request.form['password']
        if db.check_if_uni_exists(uni) is True:
            print("uni exists already")
            flash('UNI already exists, please login using your existing account!')
            #return redirect(url_for('login'))
        db.add_uni_passcode(uni, password)
        print("added uni and passcode as an account to db")
        # flash('Signup is successful, please login!')
        return redirect(url_for('login'))


'''
Endpoint:  /readreviews?restaurant=___&stars=___
UI:        User fills out a form with their query and presses 'Search' button
Return:    reviews that match that query
'''


@app.route('/readreviews', methods=['GET'])
def read_reviews():
    res_name = request.args.get('restaurant')
    rating = request.args.get('stars')

    # given restaurant
    if res_name != '' and rating == '':
        reviews = db.get_all_reviews_for_restaurant(res_name)
        if len(reviews) > 0:
            return jsonify(restaurant=res_name, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews for that "
                       + "restaurant.")

    # given rating
    elif res_name == '' and rating != '':
        reviews = db.get_all_reviews_given_rating(rating)
        if len(reviews) > 0:
            return jsonify(stars=rating, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews at/above "
                       + "that rating.")

    # given restaurant and rating
    elif res_name != '' and rating != '':
        reviews = db.get_all_reviews_for_rest_given_rating(res_name, rating)
        if len(reviews) > 0:
            return jsonify(restaurant=res_name, stars=rating, reviews=reviews,
                           valid=True, reason="")
        else:
            return jsonify(valid=False, reason="There are no reviews matching "
                           + "your query.")

    # parameters are empty strings
    else:
        return jsonify(valid=False,
                       reason="To read reviews, please make a query.")


'''
Endpoint:  /addreview?restaurant=___&stars=___&review=___&uni=___
UI:        User fills out a form and presses 'Submit Review' button
Adds review to database
'''


@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    res_name = request.args.get('restaurant')
    rating = request.args.get('stars')
    review = request.args.get('review')

    # no parameters
    if res_name is None or rating is None or review is None:
        return jsonify(valid=False,
                       reason="To add a review, please enter all required "
                       + "fields.")

    # add review if not already in db
    result = db.get_review(res_name, uni)
    if result is None:
        row = (res_name, rating, review, uni)
        db.add_review(row)
        return jsonify(valid=True, reason="Successfully added review.")
    else:
        return jsonify(valid=False,
                       reason="You've already reviewed this restaurant.")


'''
Endpoint:  /editreview?restaurant=___&stars=___&review=___&uni=___
UI:         User is already at page pre-populated
            with their original review's data.
User cannot change restaurant or uni value.
They click 'Finish Edit'
Updates review
'''


@app.route('/editreview', methods=['GET', 'POST'])
def edit_review():
    res_name = request.args.get('restaurant')
    rating = request.args.get('stars')
    review = request.args.get('review')
    uni = request.args.get('uni')

    # no parameters
    if res_name is None or rating is None or review is None or uni is None:
        return jsonify(valid=False,
                       reason="To edit a review, please enter all required "
                       + "fields.")

    # update entry in db
    db.edit_review(uni, res_name, rating, review)
    return jsonify(valid=True, reason="Successfully edited review.")


'''
Endpoint:  /allres
UI:         User clicks "show all restaurants button"
'''

# Suggested code for this endpoint

'''
@app.route('/allrest', methods=['GET'])
def display_all_restaurants():
    data = db.get_restaurants_above_ratings(1)
    return jsonify(valid=True, reason="Successfully edited review.")
'''

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
