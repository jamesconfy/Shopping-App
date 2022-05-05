from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from shoppingapp import db, bcrypt
from shoppingapp.models import Consumer, Producer, Product

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    products = Product.query.all()
    listOfProduct = {}
    for product in products:
        newObj = {
                    'Description': product.description,
                    'Image': product.image
                  }

        listOfProduct[product.name] = newObj
    return listOfProduct if listOfProduct else jsonify('Empty')

@app.route('/register-user', methods=['POST', 'GET'])
def registerConsumer():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        if address is None:
            address = ''
        phoneNumber = request.form['username']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        consumer = Consumer(username=username, email=email, password=hashed_password, address=address, phoneNumber=phoneNumber)
        db.session.add(consumer)
        db.session.commit()

        return jsonify('Successful')

    return jsonify({
        'username': 'Your Username',
        'email': 'Your Email',
        'password': 'Your Password',
        'address': 'Your House Address',
        'phone number': 'Your Phone Number',
    })

@app.route('/login-user', methods=['POST', 'GET'])
def loginConsumer():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        remember = request.form['remember me']
        consumer = Consumer.query.filter_by(username=user).first() if not None else Consumer.query.filter_by(email=user).first()

        if consumer and bcrypt.check_password_hash(consumer.password, password):
            login_user(consumer, remember=remember)

        return jsonify('Successful')

    return jsonify({
        'user': 'Username or Email',
        'password': 'Password',
        'remember me': 'True or False'
    })

@app.route('/register-seller', methods=['POST', 'GET'])
def registerProducer():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        office = request.form['office']
        phoneNumber = request.form['phone number']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        producer = Producer(username=username, email=email, password=hashed_password, office=office, phoneNumber=phoneNumber)
        db.session.add(producer)
        db.session.commit()

        return jsonify('Successful')

    return jsonify({
        'username': 'Your Username',
        'email': 'Your Email',
        'password': 'Your Password',
        'address': 'Your House Address',
        'phone number': 'Your Phone Number',
    })

@app.route('/login-seller', methods=['POST', 'GET'])
def loginProducer():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        remember = request.form['remember me']
        producer = Producer.query.filter_by(username=user).first() if not None else Producer.query.filter_by(email=user).first()

        if producer and bcrypt.check_password_hash(producer.password, password):
            login_user(producer, remember=remember)

        return jsonify('Successful')

    return jsonify({
        'user': 'Username or Email',
        'password': 'Password',
        'remember me': 'True or False'
    })

@app.route('/add-product', methods=['POST', 'GET'])
@login_required
def addProduct():
    producer = Producer.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        if current_user.id == producer.id:
    
            name = request.form['name']
            description = request.form['description']
            image = request.form['image']
            price = request.form['price']

            product = Product(name=name, description=description, image=image, price=price, user_id=current_user.id)
            db.session.add(product)
            db.session.commit()

            return jsonify('Successful')
        else:
            return jsonify('You have to be a producer to be able to add products')

    return jsonify({
        'name': 'Product Name',
        'description': 'Product Description',
        'image': 'Product Image',
        'price': 'Price'
    })

@app.route('/products')
def products():
    products = Product.query.order_by(Product.dateCreated.desc()).all()
    listOfProduct = {}
    for product in products:
        newObj = {
                    'Description': product.description,
                    'Image': product.image
                  }

        listOfProduct[product.name] = newObj
    return listOfProduct if listOfProduct else jsonify('No product yet.')

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