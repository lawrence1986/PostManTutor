from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/about', methods=['GET'])
def about():
    info = {
        'name': 'Lawrence',
        'gender': 'Male',
        'github_url': 'https://github.com/lawrence1986/',
        'description': 'A simple API endpoint with basic info.',
        'author': 'Lawrence Maduabuchi',
    }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True, port=5004)

