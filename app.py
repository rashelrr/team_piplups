from flask import Flask, render_template, request, redirect, jsonify, make_response
from json import dumps
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/', methods=['GET'])
def index():
    db.clear()
    db.init_db()
    return 'Server Works!'


@app.route('/readreviews', methods=['GET'])
def read_reviews_restaurant():
    res_name = request.args.get('resName')
    rating = request.args.get('stars')

    if res_name is not None and rating is None:     # query: all reviews for a specific rest.
        reviews = db.get_review_by_name(res_name)
        return jsonify(resName=res_name, reviews=reviews)
    elif res_name is None and rating is not None:   # query: all reviews above a certain rating
        reviews = db.get_all_reviews_above_rating(rating)
        return jsonify(reviews=reviews)
    elif res_name is not None and rating is not None:   # query: all reviews for a spec. restaurant above a certain rating
        #reviews = db.get_all_reviews_by_name_and_above_rating(res_name, rating) TO DO: add this func to db.py
        #return jsonify(resName=res_name, reviews=reviews)
        pass
    else: # error: no parameters passed in
        return jsonify(resName = "", reviews="")
 
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
