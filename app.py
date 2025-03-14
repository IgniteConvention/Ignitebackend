from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        school_id INTEGER,
        FOREIGN KEY (school_id) REFERENCES schools (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Call the database initialization
init_db()

# Define routes
@app.route('/')
def home():
    return "Welcome to the Ignite Student Convention API!"

@app.route('/add_school', methods=['POST'])
def add_school():
    data = request.json
    name = data.get('name')
    address = data.get('address')

    if not name or not address:
        return jsonify({'error': 'Name and address are required'}), 400

    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schools (name, address) VALUES (?, ?)', (name, address))
    conn.commit()
    conn.close()

    return jsonify({'message': 'School added successfully'}), 200

@app.route('/get_schools', methods=['GET'])
def get_schools():
    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schools')
    schools = cursor.fetchall()
    conn.close()

    return jsonify(schools)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    school_id = data.get('school_id')

    if not name or not school_id:
        return jsonify({'error': 'Name and school ID are required'}), 400

    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, school_id) VALUES (?, ?)', (name, school_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student added successfully'}), 200

@app.route('/get_students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    return jsonify(students)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    event_type = data.get('type')

    if not name or not category or not event_type:
        return jsonify({'error': 'Name, category, and type are required'}), 400

    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (name, category, type) VALUES (?, ?, ?)', (name, category, event_type))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Event added successfully'}), 200

@app.route('/get_events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('ignite_convention.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()

    return jsonify(events)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
