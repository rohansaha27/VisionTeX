from flask import Flask, jsonify, request

# Create the Flask app instance
app = Flask(__name__)

# Define a simple route
@app.route('/')
def home():
    return "Hello, Flask!"

# Example of a route to return JSON data
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
