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
        return jsonify(error="Invalid query. Please enter at least one field.")
 
'''
Endpoint:  /addreview?restaurant=___&stars=___&review=___&uni=___
UI:        User fills out a form and presses 'Submit Review' button
Returns:   jsonify
'''
@app.route('/addreview', methods=['GET','POST'])
def add_review():
    res_name = request.args.get('restaurant')
    rating = request.args.get('stars')
    review = request.args.get('review')
    uni = request.args.get('uni')

    # TODO: make sure that none of the strings are empty!
    parameters = [res_name, rating, review, uni]
    for e in parameters:
        if e is None:
            return jsonify(error="Invalid submission. Please enter all fields.")

    # TODO (for db team): check that res_name+uni is not already in database
        # if in db, print error message here
        # otherwise, put in db (code below)

    row = (res_name, rating, review, uni)
    db.add_review(row)
    return jsonify(error="Successfully added review.")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
