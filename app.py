from flask import Flask, render_template, request, redirect, jsonify, make_response
from json import dumps
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

'''
Homepage
'''
@app.route('/', methods=['GET'])
def index():
    db.clear()
    db.init_db()
    return 'Server Works!'


'''
Endpoint:  /readreviews?restaurant=___&stars=___
UI:        User fills out a form with their query and presses 'Search' button
Return:    reviews that match that query
'''
@app.route('/readreviews', methods=['GET'])
def read_reviews():
    res_name = request.args.get('restaurant')
    rating = request.args.get('stars')

    # query: all reviews for a specific restaurant
    if res_name is not None and rating is None:     
        reviews = db.get_all_reviews_for_restaurant(res_name)
        return jsonify(restaurant=res_name, reviews=reviews)
    # query: all reviews at/above a specific rating
    elif res_name is None and rating is not None:   
        reviews = db.get_all_reviews_given_rating(rating)
        return jsonify(reviews=reviews)
    # query: all reviews for a specific restaurant at/above a specific rating
    elif res_name is not None and rating is not None:   
        reviews = db.get_all_reviews_for_restaurant_given_rating(res_name, rating) 
        return jsonify(restaurant=res_name, reviews=reviews)
    # error: empty parameters
    else: 
        return jsonify(valid=False, reason="Error. Invalid query. Please enter at least one field.")


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
    uni = request.args.get('uni')

    res_name.lower()
    uni.lower()

    # make sure no empty fields
    parameters = [res_name, rating, review, uni]
    for e in parameters:
        if e is None:
            return jsonify(valid=False, reason="Error. Invalid submission. Please enter all fields.")

    # Add review if not already in db
    rev = db.get_review(res_name, uni)  # review or none
    if rev is None:
        row = (res_name, rating, review, uni)
        db.add_review(row)
        return jsonify(valid=True, reason="Successfully added review.")
    else:
        return jsonify(valid=False, reason="Error. You have already reviewed this restaurant.")        



'''
Endpoint:  /editreview?restaurant=___&stars=___&review=___&uni=___
UI:        User is already at page pre-populated with their original review's data. 
User cannot change restaurant or uni value.
They click 'Finish Edit'
Updates review
'''
@app.route('/editreview', methods=['GET','POST'])
def edit_review():
    new_res_name = request.args.get('restaurant')
    new_rating = request.args.get('stars')
    new_review = request.args.get('review')
    uni = request.args.get('uni')

    # make sure no empty fields
    parameters = [new_res_name, new_rating, new_review, uni]
    for e in parameters:
        if e is None:
            return jsonify(valid=False, reason="Error. Invalid edit. Please enter all fields.")

    # update entry in db
    db.edit_review(uni, new_res_name, new_rating, new_review)
    return jsonify(valid=True, reason="Successfully edited review.")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
