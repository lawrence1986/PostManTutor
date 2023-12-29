from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

CORS(app)

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    github_url = db.Column(db.String(100), nullable=True)
    endpoint_url = db.Column(db.String(100), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to return my information
@app.route('/about', methods=['GET'])
def about():
    my_info = {
        'name': 'Lawrence Maduabuchi',
        'github_url': 'https://github.com/lawrence1986',
        'gender': 'Male',
    }
    return jsonify(my_info), 200

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_all_data():
    all_data = UserData.query.all()
    data_list = []
    for data in all_data:
        data_list.append({
            'id': data.id,
            'name': data.name,
            'endpoint_url': data.endpoint_url,
            'github_url': data.github_url,
            'created_at': data.createdAt,
            'updated_at': data.updatedAt
        })
    return jsonify(data_list)

# Endpoint to get data by ID
@app.route('/data/<int:data_id>', methods=['GET'])
def get_data(data_id):
    data = UserData.query.get_or_404(data_id)
    return jsonify({
        'id': data.id,
        'name': data.name,
        'endpoint_url': data.endpoint_url,
        'github_url': data.github_url,
        'created_at': data.createdAt,
        'updated_at': data.updatedAt
    })

# Endpoint to create new data
@app.route('/data', methods=['POST'])
def create_data():
    request_data = request.get_json()

    required_fields = ['name', 'endpoint_url', 'github_url']
    if not all(field in request_data for field in required_fields):
        return jsonify({'message': 'invalid data'}), 400

    new_data = UserData(
        name=request_data['name'],
        endpoint_url=request_data.get('endpoint_url', ''),
        github_url=request_data.get('github_url', '')
    )
    db.session.add(new_data)
    db.session.commit()

    return jsonify({'message': 'Data created successfully'}), 201

# # Endpoint to update data
# @app.route('/data/<int:data_id>', methods=['PUT'])
# def update_data(data_id):
#     data = UserData.query.get_or_404(data_id)
#     request_data = request.get_json()
#     data.name = request_data.get('name', data.name)
#     data.endpoint_url = request_data.get('endpoint_url', data.endpoint_url)
#     data.github_url = request_data.get('github_url', data.github_url)
#     db.session.commit()
#     return jsonify({'message': 'Data updated successfully'})

# # Endpoint to delete data
# @app.route('/data/<int:data_id>', methods=['DELETE'])
# def delete_data(data_id):
#     data = UserData.query.filter_by(id=data_id).first()
#     if data is None:
#         return jsonify({'message': 'Data not found'}), 404
#     db.session.delete(data)
#     db.session.commit()
#     return jsonify({'message': 'Data deleted successfully'})
#just for testing

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=False, port=5004)
