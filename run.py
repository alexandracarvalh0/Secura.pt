from app import create_app

# Instantiate the application via the factory function
app = create_app()

if __name__ == '__main__':
    # Start the development server locally
    app.run(debug=True, host='127.0.0.1', port=5000)