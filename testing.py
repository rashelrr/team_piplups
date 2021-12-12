from flask import Flask, jsonify, json, request, redirect, url_for, flash
import requests
import db
app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uni = request.form['username']
        password = request.form['password']

        url = 'https://rashelserver.herokuapp.com/login'
        data = {"name": uni, 'password': password}
        response = requests.post(url=url, json=data)

        flash(response.text)
        return jsonify(response.text)
    else:
        flash("this is a get request")
        return jsonify(method="GET", status="success")



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
