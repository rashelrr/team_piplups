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
UI:        User fills out a form with their query 
Returns:   reviews that match that query
'''
@app.route('/readreviews', methods=['GET'])
def read_reviews_restaurant():
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
        return jsonify(error="No parameters for query were entered.")
 
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
