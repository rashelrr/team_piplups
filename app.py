import os
from flask import Flask, render_template, jsonify, request, redirect
import db
import logging

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
    if res_name != ''  and rating == '':
        reviews = db.get_all_reviews_for_restaurant(res_name)
        if len(reviews) > 0:
            return jsonify(restaurant=res_name, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews for that "
                       + "restaurant.")

    # given rating
    elif res_name == ''  and rating != '':
        reviews = db.get_all_reviews_given_rating(rating)
        if len(reviews) > 0:
            return jsonify(stars=rating, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews at/above "
                       + "that rating.")

    # given restaurant and rating
    elif res_name != ''  and rating != '':
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


# Display all restaurants and average rating
@app.route('/rest_display_all', methods=['GET', 'POST'])
def rest_display_all():
    result = db.get_restaurants_above_ratings(1)
    for key, value in result.items():
         rows = len(value)
    return render_template("rest_display.html", context=result, keys=list(result.keys()), rows=rows)


# Display restaurants that users filter by average star rating
@app.route('/rest_display_star_filter', methods=['GET', 'POST'])
def rest_display_star_filter():
    star = request.form.getlist('star')
    result = dict(Name=[], Average_Rating=[])
    for s in star:
        result.update(db.get_restaurants_above_ratings(s))
    for key, value in result.items():
         rows = len(value)
    return render_template("rest_display.html", context=result, keys=list(result.keys()), rows=rows)


# Display reveiws for restaurant that users filter by name
@app.route('/rest_info', methods=['GET', 'POST'])
def rest_info():
    name = request.args.get('name')
    result = db.get_all_reviews_for_restaurant(name)
    for key, value in result.items():
         rows = len(value)
    return render_template("rest_info.html", context=result, keys=list(result.keys())[1:], rows=rows)

# the problem is there is no memory so this function has no idea 
# what the name of the restaurant is
# Display reviews for restaurant that users filter by star
@app.route('/rest_info_star_filter', methods=['GET', 'POST'])
def rest_info_star_filter():
    star = request.form.getlist('star')
    name = request.referrer.split('=')[1]
    result = dict(Name=[], Star_Rating=[], Review=[], UNI=[])
    for s in star:
        result.update(db.get_all_reviews_for_rest_given_rating(name, s))
    for key, value in result.items():
         rows = len(value)
    return render_template("rest_info.html", context=result, keys=list(result.keys())[1:], rows=rows)


@app.route('/back_home')
def back_home():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
