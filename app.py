from flask import Flask, jsonify, request
import db
import logging


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

'''
Homepage
'''


@app.route('/', methods=['GET'])
def index():
    db.clear()
    db.init_db()
    # db.insert_dummy_data()
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

    # given restaurant
    if res_name is not None and rating is None:
        reviews = db.get_all_reviews_for_restaurant(res_name)
        if len(reviews) > 0:
            return jsonify(restaurant=res_name, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews for that "
                       + "restaurant.")

    # given rating
    elif res_name is None and rating is not None:
        reviews = db.get_all_reviews_given_rating(rating)
        if len(reviews) > 0:
            return jsonify(stars=rating, reviews=reviews, valid=True,
                           reason="")
        return jsonify(valid=False, reason="There are no reviews at/above "
                       + "that rating.")

    # given restaurant and rating
    elif res_name is not None and rating is not None:
        reviews = db.get_all_reviews_for_rest_given_rating(res_name, rating)
        if len(reviews) > 0:
            return jsonify(restaurant=res_name, stars=rating, reviews=reviews,
                           valid=True, reason="")
        else:
            return jsonify(valid=False, reason="There are no reviews matching "
                           + "your query.")

    # no parameters
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
    uni = request.args.get('uni')

    # no parameters
    if res_name is None or rating is None or review is None or uni is None:
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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
