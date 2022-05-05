from shoppingapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)