from flask import Flask, render_template, request, redirect, jsonify, make_response
from json import dumps
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

'''
Implement '/readreviews' endpoint
Method Type: POST
'''

@app.route('/readreviews', methods=['GET'])
def read_reviews_restaurant():

    res_name = request.args.get('resName')
    reviews = db.get_review_by_name(res_name)

    return jsonify(restaurant_name=res_name, reviews=reviews)
 






if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')