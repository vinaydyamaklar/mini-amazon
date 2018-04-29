from mini_amazon.models.product import Product
from mini_amazon.models.user import User
from bson.objectid import ObjectId
from flask import Flask, render_template, send_from_directory, request


from mini_amazon import app

user_model = User()
product_model = Product()


@app.route("/mini-amazon", methods=['GET', 'POST'])
def load_product():
    matches = product_model.get_all_products()
    return render_template("index.html", results=matches, user='')


@app.route("/mini-amazon/search", methods=['GET', 'POST'])
def search_by_name():
    if request.method == 'POST':
        prd_name = request.form['product_name']
        print(prd_name)
        matches = product_model.search_by_name(prd_name)
        search_result = ''
        if len(matches) < 1:
            search_result = 'Ooops...!, No Results found'
        return render_template("index.html", results=matches, search_result=search_result)


@app.route("/mini-amazon/ulogin", methods=['GET', 'POST'])
def load_login():
    return render_template("login.html")


@app.route("/mini-amazon/authenticate-login", methods=['GET','POST'])
def login_authenticate():
    if request.form['op_type'] == 'login':
        uname = request.form['uname']
        pwd = request.form['password']
        user = user_model.authenticate_user(uname, pwd)

        if user is None:
            return render_template("login.html", login_msg="Invalid Username/Password")
        else:
            matches = product_model.get_all_products()
            u = user_model.search_by_uname(uname)
            return render_template("index.html", results=matches, user=u)
    elif request.form['op_type'] == 'signup':
        pass


@app.route("/mini-amazon/add-to-cart", methods=['POST'])
def add_to_cart():
    prd_id = request.form.get('hdn_prd_id', None)
    user_id = request.form.get('hdn_user_id', None)
    uname = request.form.get('hdn_user_name', None)
    matches = product_model.get_all_products()
    if user_id is None or user_id == '':
        return render_template("index.html", results=matches, user='', cart_msg='Please login then add it to  Cart')
    else:
        is_success = user_model.add_product_to_cart(user_id, prd_id)
        u = user_model.search_by_id(user_id)
        if is_success:
            return render_template('index.html',
                                   results=matches,
                                   user=u, cart_msg='Product Added successfully')
        else:
            return render_template('index.html',
                                   results=matches,
                                   user=u, cart_msg='Product is already added to your cart..!')


@app.route("/miniamazon/cart", methods=['POST'])
def show_cart():
    user_id = request.form.get('user_id_with_cart', None)
    matches = product_model.get_all_products()
    if user_id is None or user_id == '':
        return render_template("index.html", results=matches, user='', cart_msg='Please login then add it to  Cart')
    else:
        u = user_model.search_by_id(user_id)
        total = 0
        product_ids = user_model.get_products_from_userid(u.get('_id'))
        products_in_cart = [product_model.search_by_id(prod_id) for prod_id in product_ids]
        for product in products_in_cart:
            total += product['price']
        return render_template('cart.html', products=products_in_cart, user=u, total=total)


@app.route("/miniamazon/delete-from-cart", methods=['POST','GET'])
def remove_from_cart():
    user_id = request.form.get('user_id',None)
    product_id = request.form.get('product_id', None)
    u = user_model.search_by_id(user_id)
    product_ids = user_model.get_products_from_userid(u.get('_id'))
    products_in_cart = []
    total = 0
    if ObjectId(product_id)  not in product_ids:
        products_in_cart = [product_model.search_by_id(prod_id) for prod_id in product_ids]
    else:
        user_model.remove_product_from_cart(user_id, product_id)
        product_ids = user_model.get_products_from_userid(u.get('_id'))
        products_in_cart = [product_model.search_by_id(prod_id) for prod_id in product_ids]
    for product in products_in_cart:
        total += product['price']
    return render_template('cart.html', products=products_in_cart, user=u, total=total)
