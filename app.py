from flask import Flask, render_template, request, redirect, jsonify
from flask import make_response
from json import dumps
import db
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


'''
Implement the '/' endpoint
Method Type: GET
Intial Webpage for restaurants initialized
'''


@app.route('/')
def index():
    db.init_db()
    return 'Server initialized!'


'''
Implement '/readreviews' endpoint
Method Type: POST
'''


@app.route('/readreviews', methods=['GET'])
def read_reviews_restaurant():

    res_name = request.args.get('resName')
    reviews = db.get_review_by_name(res_name)

    return jsonify(restaurant_name=res_name, reviews=reviews)


'''
Implement localhost:5000/readreviews?resName=val1&stars=val2' endpoint
Method Type: POST
'''


@app.route('/readreviews', methods=['GET'])
def star_reviews():

    stars = request.args.get('stars')
    star_reviews = db.get_all_reviews_above_rating(stars)

    return jsonify(reviews=star_reviews)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')