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
    return render_template('homepage.html', uni=global_uni)


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
            return redirect(url_for('home'))
        elif r_json['status'] == "wrong password":
            flash('Wrong password, try again.')
            return redirect(url_for('login'))
        else:
            flash('Account does not exist, please sign up')
            return redirect(url_for('signup'))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
