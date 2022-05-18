from flask import current_app as app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from shoppingapp import db, bcrypt
from shoppingapp.models import Producer, Product

"""
@api [get] /
description: Returns all list of books
parameters:
    - (query) name {string} Name of book
responses:
    200:
        description: It works!
        content:
            application/json:
                schema:
                    properties:
                        id:
                            type: object
                            required:
                                - name
                                - description
                                - price
                                - image
                            properties:
                                name:
                                    type: string
                                description:
                                    type: string
                                price:
                                    type: integer
                                    format: int64
                                image:
                                    type: string  
"""
@app.route('/')
def home():
    return jsonify('Getting started')

"""
@api [get] /register
summary: Check the state of the api.
description: Shows if the server is running or not.
responses:
    200:
        description: OK, the server is running.
    404:
        description: Not Found.
    500:
        description: We are having server issues, don't mind us, lol x.
"""
"""
@api [post] /register
summary: Register user
description: A route to register user
requestBody:
    description: Input your credentials to be registered.
    content:
        application/json:
            schema:
                required:
                    - username
                    - email
                    - password
                    - first name
                    - last name
                properties:
                    username:
                        type: string
                        example: Mr Shameless
                    email:
                        type: string
                        format: email
                        example: testing@demo.com
                    password:
                        type: string
                        format: password
                        example: thatisme
                    first name:
                        type: string
                        example: Confidence
                    last name:
                        type: string
                        example: James
                    office:
                        type: string
                        example: 35 Oba Akinloye Close, Oral Estate, Lekki, Lagos
responses:
    200:
        description: OK
        content:
            application/json:
                schema:  
                    type: string 
"""
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        if request.is_json:
            json = request.json
            firstName = json.get('first name')
            lastName = json.get('last name')
            username = json.get('username')
            email = json.get('email')
            office = json.get('office')
            phoneNumber = json.get('phone number')
            password = json.get('password')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        else:
            return 'Content-Type not supported!'

        producer = Producer(username=username, email=email, password=hashed_password,
                            office=office, phoneNumber=phoneNumber, firstName=firstName, lastName=lastName)
        db.session.add(producer)
        db.session.commit()

        return jsonify(producer.__repr__()), 200

    return jsonify('Here We Go')


"""
@api [get] /login
summary: Check state of API.
description: Check if the server is running.
responses:
    200:
        description: OK, the server is running.
    404:
        description: Not Found
    500:
        description: We are having server issues, don't mind us, lol x.
"""
"""
@api [post] /login
summary: Login.
description: Provide your credentials to access the service.
requestBody:
    description: Login details
    content:
        application/json:
            schema:
                required:
                    - username or email
                    - password
                    - remember me
                properties:
                    username or email:
                        type: string
                        example: Mr Shameless or testing@demo.com
                    password:
                        type: string
                        format: password
                        example: thatisme
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: integer
                    format: int32
    400:
        description: Not Found
    500:
        description: Server issues
"""
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        if request.is_json:
            user = request.json.get('username or email')
            password = request.json.get('password')
            remember = True
            producer = Producer.query.filter_by(username=user).first()
            
            if producer is None:
                producer = Producer.query.filter_by(email=user).first()

            if producer and bcrypt.check_password_hash(producer.password, password):
                login_user(producer, remember=remember)

                return jsonify(producer.id)
            else:
                return jsonify('Username/Email or Password is incorrect')

    return jsonify('You need to login first')

"""
@api [get] /products
summary: Get all products
description: Get all products in the catalog
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            name:
                                type: string
                            description:
                                type: string
                            image:
                                type: string
                            price:
                                type: number
                                format: float
                            date created:
                                type: string
                                format: date
"""
"""
@api [post] /products
summary: Create a product.
description: Add product to catalog
requestBody:
    description: Provide product name, description, price and image to add it to catalog.
    content:
        application/json:
            schema:
                required:
                    - name
                    - description
                    - price
                    - image
                properties:
                    name:
                        type: string
                        example: New Age Powerbank.
                    description:
                        type: string
                        example: Lasts very long.
                    price:
                        type: number
                        format: float
                        example: 20000.00
                    image:
                        type: string
                        example: https://www-konga-com-res.cloudinary.com/w_auto,f_auto,fl_lossy,dpr_auto,q_auto/media/catalog/product/A/A/194438_1634339558.jpg
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            name:
                                type: string
                            description:
                                type: string
                            price:
                                type: integer
                                format: int32
                            image:
                                type: string

"""
@app.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        products = Product.query.order_by(Product.dateCreated.desc()).all()
        listOfProduct = []
        for product in products:
            newObj = {
                'Name': product.name,
                'Description': product.description,
                'Price': product.price,
                'Image': product.image,
                'Date Created': product.dateCreated,
                'Producer': f'{product.producer.firstName} {product.producer.lastName}'
            }

            listOfProduct.append(newObj)
        return jsonify(data=listOfProduct) if listOfProduct else jsonify('No product yet.')

    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.is_json:
                name = request.json.get('name')
                description = request.json.get('description')
                price = request.json.get('price')
                image = request.json.get('image')

                product = Product(name=name, description=description, price=price, image=image, user_id=current_user.id)
                db.session.add(product)
                db.session.commit()

                return jsonify(product.__repr__())
        else:
            return jsonify('You have to be logged in to add a product.')

"""
@api [get] /products/{productId}
summary: Get product.
description: Supply an id to view a particular product.
parameters:
    - (path) productId* {integer:int32} ID of book
responses:
    200:
        description: It works!
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        name:
                            type: string
                        description:
                            type: string
                        price:
                            type: integer
                            format: int32
                        image:
                            type: string 
"""
"""
@api [patch] /products/{productId}
summary: Update product
description: Provide your parameters to update your product
parameters:
    - (path) productId* {integer:int32} Product ID
requestBody:
    description: Products name, description, price and image
    content:
        application/json:
            schema:
                properties:
                    name:
                        type: string
                    description:
                        type: string
                    price:
                        type: number
                        format: float
                    image:
                        type: string
"""
"""
@api [delete] /products/{productId}
summary: Delete product.
description: Delete a specific product.
parameters:
    - (path) productId* {integer:int32} Delete a product
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: string
"""
@app.route('/products/<int:product_id>', methods=['GET', 'PATCH', 'DELETE'])
def product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        newObj = {
        'Name': product.name,
        'Description': product.description,
        'Image': product.image,
        'Price': product.price,
        'Date Created': product.dateCreated,
        'Producer': f'{product.producer.firstName} {product.producer.lastName}'
        }

        return jsonify(newObj)

    if request.method == 'PATCH':
        if current_user.is_authenticated: 
            if current_user == product.producer:
                if request.is_json:
                    name = request.json.get('name')
                    description = request.json.get('description')
                    price = request.json.get('price')
                    image = request.json.get('image')

                    if name:
                        product.name = name
                    if description:
                        product.description = description
                    if price:
                        product.price = price
                    if image:
                        product.image =  image

                    db.session.commit()
                    return jsonify(product.__repr__())
            else:
                return jsonify('You did not create this product.')
        else:
            return jsonify('You have to be logged in to edit a product.')

    if request.method == 'DELETE':
        if current_user ==  product.producer:
            db.session.delete(product)
            db.session.commit()
            return jsonify('Successful')
        else:
            return jsonify('You cannot delete others product')
            

"""
@api [get] /users
summary: List All Users.
description: Get list of all users in a name and address format.
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            name:
                                type: string
                            office:
                                type: string
"""
@app.route('/users')
def users():
    users = Producer.query.order_by(Producer.dateCreated.desc()).all()
    listOfUser = []
    for user in users:
        newObj = {
            "Name": f'{user.firstName} {user.lastName}',
           # "Username": user.username,
           # "Email": user.email,
           # "Password": user.password,
            "Office": user.office,
        }

        listOfUser.append(newObj)

    return jsonify(listOfUser) if listOfUser else jsonify('No user currently, go ahead and register.')

"""
@api [get] /users/{userId}
summary: Get User.
description: Get a particular user.
parameters:
    - (path) userId* {integer:int32} User ID
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        name:
                            type: string
                        username:
                            type: string
                        email:
                            type: string
                        office:
                            type: string
"""
"""
@api [put] /users/{userId}
parameters:
    - (path) userId* {string} User ID
requestBody:
    description: Update information for current user.
    content:
        application/json:
            schema:
                type: object
                properties:
                    first name:
                        type: string
                    last name:
                        type: string
                    username:
                        type: string
                    email:
                        type: string
                    office:
                        type: string
                    phone number:
                        type: string
"""
"""
@api [delete] /users/{userId}
summary: Delete User.
description: Provide id to delete a user.
parameters:
    - (path) userId* {integer:int32} User ID
responses:
    200:
        description: OK
        content:
            application/json:
                schema:
                    type: string
"""
@app.route('/users/<int:user_id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def user(user_id):
    user = Producer.query.get_or_404(user_id)
    if request.method == 'GET':
        newObj = {
            "Name": f'{user.firstName} {user.lastName}',
            "Username": user.username,
            "Email": user.email,
            "Office": user.office,
        }

        return jsonify(newObj)

    if request.method == 'PATCH':
        if current_user == user:
            if request.is_json:
                firstName = request.json.get('first name')
                if firstName:
                    user.firstName = firstName

                lastName = request.json.get('last name')
                if lastName:
                    user.lastName = lastName

                username = request.json.get('username')
                if username and Producer.query.filter_by(username=username).first() is None:
                    user.username = username

                email = request.json.get('email')
                if email:
                    user.email = email

                office = request.json.get('office')
                if office:
                    user.office = office

                phoneNumber = request.json.get('phone number')
                if phoneNumber and Producer.query.filtery_by(phoneNumber=phoneNumber).first() is None:
                    user.phoneNumber = phoneNumber

                db.session.commit()
                return jsonify(user.__repr__())

        else:
            return jsonify('You cannot update another user profile')

    if request.method == 'DELETE':
        if current_user == user:
            db.session.delete(user)
            logout_user()
            db.session.commit()
            return jsonify('Successful')

        else:
            return jsonify("You are not authorized to delete others account.")

"""
@api [get] /logout
summary: Logout.
description: End the session and logout of the server.
responses:
    200:
        description: OK
"""
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('Logout, Successful')