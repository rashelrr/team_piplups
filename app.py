import json
from flask import Flask, render_template, jsonify, request, redirect,\
    url_for, flash
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
    db.clear()
    db.init_db()
    db.insert_dummy_data()
    return "Welcome to the LionEats API!"


'''
Clear database
'''

'''
@app.route('/clear', methods=['GET'])
def clear():
    db.clear()
    db.init_db()'''


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
            return jsonify(status="success")
        else:
            # wrong password
            return jsonify(status="wrong password")
    else:
        return jsonify(status="account not exist")


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
        return jsonify(status="account exists")
    else:
        # successful sign up
        db.add_uni_passcode(uni, password)
        return jsonify(status="success")


''' ############ BELOW: TO FIX ############ '''


'''
Adds review to database
'''


@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    name = request.form['restaurant']
    star = request.form['stars']
    comment = request.form['review']
    uni = request.form['user']
    
    result = db.get_review_uni_res(name, uni)
    if len(result) == 0:
        row = (name, star, comment, uni)
        db.add_review(row)
        flash("Successfully added review.")
        data = json.stringify({'res_name':name, 'rating':star, 'review':comment, 'method':"POST", 'status':"success"})
        return jsonify(data)
    else:
        data = json.stringify({'res_name':name, 'rating':star, 'review':comment, 'method':"POST", 'status':"error"})
        return jsonify(data)

'''
Endpoint:  /editreview?restaurant=___&stars=___&review=___&uni=___
UI:         User is already at page pre-populated
            with their original review's data.
            Allows user to search for a review and update that
'''

er_html = 'edit_review.html'
@app.route('/editreview', methods=['POST'])
def edit_review():
    user = request.get_json(force=True)
    UNI = user["uni"]
    result = db.get_review_uni(UNI)
    for k, v in result.items():
        rows = len(v)
    return jsonify(res=result, num_rows=rows)
    return render_template(er_html, context=result,
                           keys=list(result.keys()), rows=rows,
                           uni=UNI)


'''
Endpoint:  /edit_review_search
UI:         User clicks submit button at edit_review page
Purpose:    searches for a restaurant review made by the current user
'''


@app.route('/edit_review_search', methods=['GET'])
def edit_review_search():
    global global_uni
    global global_res
    name = request.args.get('name')
    if db.get_review_uni_res(name, global_uni) == []:
        flash("Uni and Restaurant pair does not exist, try again")
        result = db.get_review_uni(global_uni)
        for k, v in result.items():
            rows = len(v)
        return render_template(er_html, context=result,
                               keys=list(result.keys()), rows=rows,
                               uni=global_uni)
    global_res = name
    rows = db.get_review_uni_res(global_res, global_uni)
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
    return render_template("edit_review_search.html", context=result,
                           keys=list(result.keys())[1:], rows=rows,
                           uni=global_uni)


'''
Endpoint:  /update_star_and_review
UI:         User clicks submit button on edit_review_search page
Purpose:    allows the user to update the new star and review
'''


@app.route('/update_star_and_review', methods=['GET', 'POST'])
def update_star_and_review():
    star = request.form['star']
    review = request.form['review']
    db.edit_review(global_uni, global_res, star, review)
    result = db.get_review_uni(global_uni)
    for k, v in result.items():
        rows = len(v)
    return render_template(er_html, context=result,
                           keys=list(result.keys()), rows=rows,
                           uni=global_uni)

'''
Endpoint:  /rest_display
UI:         User clicks "show all restaurants" button or user checks 
            radio button and clicks "filter" button
Purpose:    Display all restaurants and average rating
'''


@app.route('/rest_display', methods=['GET', 'POST'])
def rest_display():
    user = request.get_json(force=True)
    star = user['star']
    result = db.get_restaurants_above_ratings(star)
    for key, value in result.items():
        rows = len(value)
    return jsonify(status=result, rows=rows)


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
    return jsonify(status=result, rows=rows)


'''
Endpoint:  /back_home
UI:         User clicks the "go back home" button
Purpose:    Redirects the user back to the home page
'''


@app.route('/back_home')
def back_home():
    return redirect('/home')


if __name__ == '__main__':
    app.run(debug=True)

'''if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')'''
