import os
from flask import Flask, render_template, request, redirect,\
    url_for, flash
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


'''Homepage'''


@app.route('/', methods=['GET'])
def index():
    global global_uni
    return render_template('homepage.html', uni='')


'''
Endpoint:  /login
UI:         User clicks "login" button on homepage
Purpose:    Allows user to log in
            (if not registered, will lead to signup page)
'''


@app.route('/home', methods=['GET'])
def home():
    global global_uni
    return render_template('homepage_logged_in.html', uni=global_uni)


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


@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    if request.method == 'GET':
        res_name = request.args.get('restaurant')
        rating = request.args.get('stars')
        review = request.args.get('review')

        url = 'https://lioneats.herokuapp.com/addreview'
        data = {"restaurant": res_name, 'stars': rating, 'review': review, 'user': global_uni}
        response = requests.post(url=url, json=data)

        # r_json = response.json()
        if 'json' in response.headers.get('Content-Type'):
            r_json = response.json()
        else:
            print('Response is not in JSON format')
            r_json = 'spam'

        if r_json['status'] == 500:
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
    url = 'https://lioneats.herokuapp.com/preaddreview'
    data = {'username': global_uni}
    response = requests.post(url=url, json=data)

    if 'json' in response.headers.get('Content-Type'):
        r_json = response.json()
    else:
        print('Response is not in JSON format')
        r_json = 'spam'
        
    if r_json['status'] == "500":
        return render_template("add_review.html", uni=global_uni)
    else:
        flash("Please Log in")
        return redirect(url_for('login'))


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
            return redirect(url_for('login'))
        else:
            flash('Account already exists, please log in')
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')


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
    # program never gets past this so don't mind the stuff below
    if r_json['status'] == "success":
        flash('Shit worked')
        return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
