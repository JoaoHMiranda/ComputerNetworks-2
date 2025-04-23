import os
import sqlite3
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB_PATH = os.getenv('DB_PATH', 'devices.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            traffic REAL NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()

init_db()

def to_dict(row):
    status = 'Normal' if row['traffic'] < 50 else 'Alto'
    return {
        'id': row['id'],
        'ip': row['ip'],
        'name': row['name'],
        'traffic': row['traffic'],
        'status': status
    }

@app.route('/devices', methods=['GET'])
def list_devices():
    db = get_db()
    rows = db.execute('SELECT * FROM devices').fetchall()
    return jsonify([to_dict(r) for r in rows]), 200

@app.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json() or {}
    ip = data.get('ip')
    name = data.get('name')
    traffic = data.get('traffic')
    if not ip or not name or traffic is None:
        return jsonify({'error': 'IP, name and traffic are required'}), 400
    db = get_db()
    # Verifica unicidade do IP
    if db.execute('SELECT 1 FROM devices WHERE ip = ?', (ip,)).fetchone():
        return jsonify({'error': 'IP already registered'}), 400
    try:
        db.execute(
            'INSERT INTO devices (ip, name, traffic) VALUES (?, ?, ?)',
            (ip, name.strip(), float(traffic))
        )
        db.commit()
        row = db.execute('SELECT * FROM devices WHERE id = last_insert_rowid()').fetchone()
        return jsonify(to_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'IP must be unique'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    db = get_db()
    cur = db.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({'error': 'Device not found'}), 404
    return jsonify({'message': 'Device removed'}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))