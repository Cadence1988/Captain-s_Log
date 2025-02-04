from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///captains_log.db'  # Fixed typo here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Initialize the database
db = SQLAlchemy(app)

# Database model for logs
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Fixed typo in default

# Route to add a new log entry
@app.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    task = data.get('task', '')

    if not task:
        return jsonify({'error': 'Task is required'}), 400
    
    log = Log(task=task)
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Log added successfully', 'log': {'id': log.id, 'task': log.task}}), 201

# Route to get all logs
@app.route('/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    logs_list = [{'id': log.id, 'task': log.task, 'timestamp': log.timestamp} for log in logs]

    return jsonify(logs_list), 200

# Route to search logs by keyword
@app.route('/logs/search', methods=['GET'])
def search_logs():
    query = request.args.get('query', '')
    if query:
        logs = Log.query.filter(Log.task.ilike(f'%{query}%')).all()
        logs_list = [{'id': log.id, 'task': log.task, 'timestamp': log.timestamp} for log in logs]
        return jsonify(logs_list), 200
    else:
        return jsonify({'error': 'Query parameter is required'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
