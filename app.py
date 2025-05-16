from flask import Flask, render_template, request, jsonify
import hashlib
import time
import sqlite3
import requests

app = Flask(__name__)

# DB setup (only run once to initialize if needed)
def init_db():
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meter_number TEXT,
                    amount REAL,
                    token TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# Token generator
def generate_token(meter_number, amount):
    raw_data = f"{meter_number}{amount}{time.time()}"
    token = hashlib.sha256(raw_data.encode()).hexdigest()[:10].upper()
    return token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy_token', methods=['POST'])
def buy_token():
    meter_number = request.form['meter_number']
    amount = float(request.form['amount'])

    token = generate_token(meter_number, amount)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Save to DB
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute("INSERT INTO tokens (meter_number, amount, token, timestamp) VALUES (?, ?, ?, ?)",
              (meter_number, amount, token, timestamp))
    conn.commit()
    conn.close()

    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(debug=True)
