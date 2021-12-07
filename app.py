import os
from flask import Flask, render_template, jsonify, request, redirect,\
    url_for, flash
import db
import logging

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')
app = Flask(__name__, template_folder=tmpl_dir)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

'''
Homepage
'''

global_uni = ''


@app.route('/', methods=['GET'])
def index():
    global global_uni
    db.clear()
    db.init_db()
    db.insert_dummy_data()
    return render_template('homepage.html', uni=global_uni)


'''
Endpoint:  /home
UI:         User clicks "log in" after putting in the right credentials
Purpose:    Leads the logged-in user to their home page
'''


@app.route('/home', methods=['GET'])
def home():
    global global_uni
    return render_template('homepage_logged_in.html', uni=global_uni)


'''
Endpoint:  /login
UI:         User clicks "login" button on homepage
Purpose:    Allows user to log in 
            (if not registered, will lead to signup page)
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uni = request.form['username']
        password = request.form['password']
        if db.check_if_uni_exists(uni) is True:
            if db.get_password(uni)[0][0] == password:
                global global_uni
                global_uni = uni
                return redirect("http://127.0.0.1:5000/home")
            else:
                flash('Error: Password is wrong, try again.')
                return redirect(url_for('login'))
        else:
            flash('Error: Account does not exist, please sign up')
            return redirect(url_for('signup'))
    else:
        return render_template('login.html')


'''
Endpoint:  /signup
UI:         User clicks "sign up" on homepage
Purpose:    Allows the user to sign up for a new account
'''


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
            return redirect(url_for('login'))
        db.add_uni_passcode(uni, password)
        print("added uni and passcode as an account to db")
        flash('Signup is successful, please login!')
        return redirect(url_for('login'))


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
    else:
        # add review if not already in db
        result = db.get_review(res_name, global_uni)
        if result is None:
            row = (res_name, rating, review, global_uni)
            db.add_review(row)
            return jsonify(valid=True, reason="Successfully added review.")
        else:
            return jsonify(valid=False,
                           reason="You've already reviewed this restaurant.")


@app.route('/preaddreview', methods=['GET', 'POST'])
def pre_add_review():
    return render_template("add_review.html")


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
Endpoint:  /preeditreview
UI:         User clicks "edit review" on homepage
Purpose:    displays all the reviews made by the logged-in user
            and allows the user to search for a specific review
'''


@app.route('/preeditreview', methods=['GET', 'POST'])
def pre_edit_review():
    global global_uni
    if global_uni == '':
        return redirect(url_for('login'))
    result = db.get_review_uni(global_uni)
    for k, v in result.items():
        rows = len(v)
    return render_template('edit_review.html', context=result,
                           keys=list(result.keys()), rows=rows,
                           uni=global_uni)


'''
Endpoint:  /edit_review_search
UI:         User clicks submit button at edit_review page
Purpose:    searches for a restaurant review made by the current user
'''


@app.route('/edit_review_search', methods=['GET'])
def edit_review_search():
    pass


'''
Endpoint:  /rest_display_all
UI:         User clicks "show all restaurants button"
Purpose:    Display all restaurants and average rating
'''


@app.route('/rest_display_all', methods=['GET', 'POST'])
def rest_display_all():
    result = db.get_restaurants_above_ratings(1)
    for key, value in result.items():
        rows = len(value)
    return render_template("rest_display.html", context=result,
                           keys=list(result.keys()), rows=rows)


# Display restaurants that users filter by average star rating
@app.route('/rest_display_star_filter', methods=['GET', 'POST'])
def rest_display_star_filter():
    star = request.form['star']
    result = db.get_restaurants_above_ratings(star)
    for key, value in result.items():
        rows = len(value)
    return render_template("rest_display.html", context=result,
                           keys=list(result.keys()), rows=rows)


# Display reveiws for restaurant that users filter by name
@app.route('/rest_info', methods=['GET'])
def rest_info():
    name = request.args.get('name')
    result = db.get_all_reviews_for_restaurant(name)
    for key, value in result.items():
        rows = len(value)
    return render_template("rest_info.html", context=result,
                           keys=list(result.keys())[1:], rows=rows)


# Display reviews for restaurant that users filter by star
@app.route('/rest_info_star_filter', methods=['GET', 'POST'])
def rest_info_star_filter():
    star = request.form['star']
    name = request.referrer.split('=')[1]
    result = db.get_all_reviews_for_rest_given_rating(name, star)
    for key, value in result.items():
        rows = len(value)
    return render_template("rest_info.html", context=result,
                           keys=list(result.keys())[1:], rows=rows)


@app.route('/back_home')
def back_home():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
