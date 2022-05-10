from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from shoppingapp import db, bcrypt
from shoppingapp.models import Consumer, Product
from datetime import datetime, timedelta


@app.route('/')
# @app.route('/index')
# @app.route('/home')
def home():
    BOOK_REQUESTS = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'name': f'New Age Earbud',
        'description': f'Tested and Trusted',
        'price': 20.0,
        'image': "https://github.com/jamesconfy/1"
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        'name': f'New Age Charger',
        'description': f'Tested but Not Trusted',
        'price': 10.0,
        'image': "https://github.com/jamesconfy/2"
    }
}
    return jsonify(BOOK_REQUESTS)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        firstName = request.form['first name']
        lastName = request.form['last name']
        password = request.form['password']
        address = request.form['address']
        if address is None:
            address = ''
        phoneNumber = request.form['username']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        consumer = Consumer(username=username, email=email, password=hashed_password,
                            address=address, phoneNumber=phoneNumber, firstName=firstName, lastName=lastName)
        db.session.add(consumer)
        db.session.commit()

        return jsonify(data=consumer), 200


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        remember = request.form['remember me']
        consumer = Consumer.query.filter_by(username=user).first(
        ) if not None else Consumer.query.filter_by(email=user).first()

        if consumer and bcrypt.check_password_hash(consumer.password, password):
            login_user(consumer, remember=remember)

        return jsonify('Successful')


@app.route('/products')
def products():
    products = Product.query.order_by(Product.dateCreated.desc()).all()
    listOfProduct = {}
    for product in products:
        newObj = {
            'Description': product.description,
            'Image': product.image,
            'Price': product.price
        }

        listOfProduct[product.name] = newObj
    return jsonify(data=listOfProduct) if listOfProduct else jsonify('No product yet.')


@app.route('/products/<int:product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id)
    newObj = {
        'Name': product.name,
        'Description': product.description,
        'Image': product.image,
        'Date Created': product.dateCreated
    }

    return jsonify(newObj)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('Logout, Successful')