import os
from flask import Flask, render_template, request, redirect,\
    url_for, flash, jsonify
import logging
import requests

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')
app = Flask(__name__, template_folder=tmpl_dir)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
global_uni = ''
global_res = ''
er_html = 'edit_review.html'

'''Homepage'''


@app.route('/', methods=['GET'])
def index():
    global global_uni
    return render_template('homepage.html', uni='')


@app.route('/home', methods=['GET'])
def home():
    global global_uni
    return render_template('homepage_logged_in.html', uni=global_uni)



'''
Endpoint:  /login
UI:         User clicks "login" button on homepage
Purpose:    Allows user to log in
            (if not registered, will lead to signup page)
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uni = request.form['username']
        password = request.form['password']

        url = 'https://lioneats.herokuapp.com/login'
        data = {"username": uni, 'password': password}
        response = requests.post(url=url, json=data)

        r_json = response.json()
        if r_json['status'] == "success":
            global global_uni
            global_uni = uni
            return redirect(url_for('home'))
        elif r_json['status'] == "wrong password":
            flash('Wrong password, try again.')
            return redirect(url_for('login'))
        else:
            flash('Account does not exist, please sign up')
            return redirect(url_for('signup'))
    else:
        return render_template('login.html')


'''
/signup
Allows users to sign up
'''


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uni = request.form['username']
        password = request.form['password']

        url = 'https://lioneats.herokuapp.com/signup'
        data = {"username": uni, 'password': password}
        response = requests.post(url=url, json=data)

        r_json = response.json()
        if r_json['status'] == "success":
            flash('Signed up successfully, please log in')
            return render_template('login.html') # redirect(url_for('login'))
        else:
            flash('Account already exists, please log in')
            return render_template('login.html') # redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    if request.method == 'GET':
        res_name = request.args.get('restaurant')
        rating = request.args.get('stars')
        review = request.args.get('review')

        url = 'https://lioneats.herokuapp.com/addreview'
        data = {'restaurant': res_name, 'stars': rating, 'review': review, 'user': global_uni}
        response = requests.post(url=url, json=data)

        r_json = response.json()
        if 'json' in response.headers.get('Content-Type'):
            r_json = response.json()
        else:
            print('Response is not in JSON format')
            r_json = 'spam'

        if r_json['status'] == "success":
            flash("Successfully added review.")
            return redirect(url_for('pre_add_review'))
        else:
            flash("You've already reviewed this restaurant. You can only " +
                  "submit one review per restaurant. You can edit your " +
                  "previous review from the homepage by clicking the 'Edit " +
                  " Review' button.")
            return redirect(url_for('pre_add_review'))


@app.route('/preaddreview', methods=['GET', 'POST'])
def pre_add_review():
    if global_uni == '':
        return redirect(url_for('login'))
    return render_template("add_review.html", uni=global_uni)


'''
Endpoint:  /editreview?restaurant=___&stars=___&review=___&uni=___
UI:         User is already at page pre-populated
            with their original review's data.
            Allows user to search for a review and update that
'''


@app.route('/editreview', methods=['GET', 'POST'])
def edit_review():
    global global_uni
    if global_uni == '':
        return redirect(url_for('login'))
    url = 'https://lioneats.herokuapp.com/editreview'
    data = {"uni": global_uni}
    response = requests.post(url=url, json=data)
    r_json = response.json()
    return render_template(er_html, context=r_json["res"],
                           keys=list(r_json["res"].keys()),
                           rows=r_json["num_rows"],
                           uni=global_uni)


'''
Endpoint:  /edit_review_search
UI:         User clicks submit button at edit_review page
Purpose:    searches for a restaurant review made by the current user
'''


@app.route('/edit_review_search', methods=['GET', 'POST'])
def edit_review_search():
    if request.method == 'GET':
        global global_res
        name = request.args.get('name')
        print(name)

        url = 'https://lioneats.herokuapp.com/edit_review_search'
        data = {"uni": global_uni, "res": name, "global_res": global_res}
        response = requests.post(url=url, json=data)

        r_json = response.json()
        if r_json["status"] == "fail":
            flash("You haven't reviewed this restaurant. Please try again.")
            return render_template(er_html, context=r_json["res"],
                                   keys=list(r_json["res"].keys()),
                                   rows=r_json["num_rows"],
                                   uni=global_uni)
        else:
            global_res = r_json["global_restaurant"]
            return render_template("edit_review_search.html", context=r_json["res"],
                                    keys=list(r_json["res"].keys()),
                                    rows=r_json["num_rows"],
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
    url = 'https://lioneats.herokuapp.com/update_star_and_review'
    data = {"star": star, "review": review, "uni": global_uni,
            "res": global_res}
    response = requests.post(url=url, json=data)
    r_json = response.json()
    return render_template(er_html, context=r_json["res"],
                           keys=list(r_json["res"].keys()),
                           rows=r_json["num_rows"],
                           uni=global_uni)


@app.route('/rest_display', methods=['GET', 'POST'])
def rest_display():
    if request.method == 'GET':
        star = request.args.get('star')
    else:
        star = 1
    url = "https://lioneats.herokuapp.com/rest_display"
    data = {'star': star}
    response = requests.post(url=url, json=data)
    r_json = response.json()
    # print(r_json)
    result = r_json['status']
    rows = r_json['rows']
    return render_template("rest_display.html", context=result,
                           keys=list(result.keys()), rows=rows)


@app.route('/rest_info', methods=['GET'])
def rest_info():
    name = request.args.get('name')
    star = request.args.get('star')
    url = "https://lioneats.herokuapp.com/rest_info"
    data = {'name': name, 'star': star}
    response = requests.get(url=url, json=data)
    r_json = response.json()
    # print(r_json)
    result = r_json['status']
    rows = r_json['rows']
    return render_template("rest_info.html", context=result,
                           keys=list(result.keys()), rows=rows)


@app.route('/back_home')
def back_home():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
