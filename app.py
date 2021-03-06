from flask import Flask, jsonify, request
import db
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


'''
Homepage for API
'''


@app.route('/', methods=['GET'])
def index():
    db.init_db()  # create databases if not already created
    return "Welcome to the LionEats API!"


'''
Clear database
'''


@app.route('/clear', methods=['GET'])
def clear():
    db.clear()
    db.init_db()


'''
Endpoint:  /login
Purpose:    Determines if user can log in
'''


@app.route('/login', methods=['POST'])
def login():
    user = request.get_json(force=True)
    uni = user['username']
    password = user['password']

    if db.check_if_uni_exists(uni) is True:
        if db.get_password(uni)[0][0] == password:
            # successfully logged in
            return jsonify(status_code="200", status="success")
        else:
            # wrong password
            return jsonify(status_code="500", status="failure",
                           reason="wrong password")
    else:
        return jsonify(status_code="500", status="failure",
                       reason="account not exist")


'''
Endpoint:  /signup
Purpose:    Allows the user to sign up for a new account
'''


@app.route('/signup', methods=['POST'])
def signup():
    user = request.get_json(force=True)
    uni = user['username']
    password = user['password']

    if db.check_if_uni_exists(uni) is True:
        # failed sign up
        return jsonify(status_code="500", status="failure",
                       reason="account exists")
    else:
        # successful sign up
        db.add_uni_passcode(uni, password)
        return jsonify(status_code="200", status="success")


'''
Endpoint:   /addreview
Purpose:     Adds review to database
'''


@app.route('/addreview', methods=['POST'])
def add_review():
    entry = request.get_json(force=True)
    name = entry['restaurant']
    star = entry['stars']
    comment = entry['review']
    uni = entry['user']

    result = db.get_review_uni_res(name, uni)
    if len(result) == 0:
        row = (name, star, comment, uni)
        db.add_review(row)
        return jsonify(status_code="200", status="success")
    else:
        return jsonify(status_code="500", status="failure",
                       reason="already reviewed this restaurant")


'''
Endpoint:  /editreview
UI:         User is already at page pre-populated
            with their original review's data.
            Allows user to search for a review and update that
'''


@app.route('/editreview', methods=['POST'])
def edit_review():
    user = request.get_json(force=True)
    UNI = user["uni"]
    result = db.get_review_uni(UNI)
    for k, v in result.items():
        rows = len(v)
    return jsonify(status_code="200", status="success", res=result,
                   num_rows=rows)


'''
Endpoint:  /edit_review_search
UI:         User clicks submit button at edit_review page
Purpose:    searches for a restaurant review made by the current user
'''


@app.route('/edit_review_search', methods=['POST'])
def edit_review_search():
    data = request.get_json(force=True)
    UNI = data["uni"]
    name = data["res"]
    if db.get_review_uni_res(name, UNI) == []:
        result = db.get_review_uni(UNI)
        for k, v in result.items():
            rows = len(v)
        return jsonify(status_code="500", status="failure", num_rows=rows,
                       res=result, reason="never reviewed this restaurant")

    rows = db.get_review_uni_res(name, UNI)
    name = []
    star = []
    review = []
    uni = []
    for r in rows:
        name.append(r[0])
        star.append(r[1])
        review.append(r[2])
        uni.append(r[3])
    result = dict(Name=name, Star_Rating=star, Review=review, UNI=uni)
    for key, value in result.items():
        rows = len(value)
    return jsonify(status_code="200", status="success", num_rows=rows,
                   res=result, global_restaurant=name)


'''
Endpoint:  /update_star_and_review
UI:         User clicks submit button on edit_review_search page
Purpose:    allows the user to update the new star and review
'''


@app.route('/update_star_and_review', methods=['POST'])
def update_star_and_review():
    data = request.get_json(force=True)
    star = data["star"]
    review = data["review"]
    global_uni = data["uni"]
    global_res = data["res"]
    db.edit_review(global_uni, global_res, star, review)
    result = db.get_review_uni(global_uni)
    for k, v in result.items():
        rows = len(v)
    return jsonify(status_code="200", status="success", res=result,
                   num_rows=rows)


'''
Endpoint:  /rest_display
UI:         User clicks "show all restaurants" button or user checks
            radio button and clicks "filter" button
Purpose:    Display all restaurants and average rating
'''


@app.route('/rest_display', methods=['POST'])
def rest_display():
    user = request.get_json(force=True)
    star = user['star']
    result = db.get_restaurants_above_ratings(star)
    for key, value in result.items():
        rows = len(value)
    return jsonify(status_code="200", status="success", res=result, rows=rows)


'''
Endpoint:  /rest_info
UI:         User enters the name of a restaurant and clicks the "view"
            button, or user checks radio button and clicks "filter"
            button, or user clicks "see all reviews" button
Purpose:    Display reviews for a restaurant; either all reviews or
            only reviews over are over checked number
'''


@app.route('/rest_info', methods=['GET'])
def rest_info():
    user = request.get_json(force=True)
    star = user['star']
    name = user['name']
    if star:
        result = db.get_all_reviews_for_rest_given_rating(name, star)
    else:
        result = db.get_all_reviews_for_restaurant(name)
    for key, value in result.items():
        rows = len(value)
    return jsonify(status_code="200", status="success", res=result, rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
