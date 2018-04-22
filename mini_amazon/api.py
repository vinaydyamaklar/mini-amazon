from mini_amazon.models.product import Product
from mini_amazon.models.user import User
from flask import Flask, render_template, send_from_directory, request


from mini_amazon import app

user_model = User()
product_model = Product()


@app.route("/mini-amazon", methods=['GET', 'POST'])
def load_product():
    matches = product_model.get_all_products()
    return render_template("index.html", results=matches)


@app.route("/mini-amazon/ulogin", methods=['GET', 'POST'])
def load_login():
    return send_from_directory("mini_amazon/static", "login.html")


@app.route("/mini-amazon/authenticate-login", methods=['GET','POST'])
def login_authenticate():
    uname = request.form['uname']
    pwd = request.form['password']
    user = user_model.authenticate_user(uname, pwd)

    if user is None:
        print("None")
        return send_from_directory("mini_amazon/static", "login.html")
    else:
        matches = product_model.get_all_products()
        print(matches)
        return render_template("index.html", results=matches, uname='vinay')
