import random
import time
import sqlite3
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Paystack secret key (replace with your own from https://dashboard.paystack.com/)
SECRET_KEY = "sk_test_xxxxxxxxxxxxxxxxxxxxx"

# ----------------------
# Token Generator Logic
# ----------------------
def generate_token(meter_number, amount):
    random.seed(int(time.time()))
    return str(random.randint(100000, 999999))

# ----------------------
# Home Page
# ----------------------
@app.route('/')
def home():
    return render_template('index.html')

# ----------------------
# Paystack Payment Verification
# ----------------------
@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    data = request.get_json()
    reference = data['reference']
    meter_number = data['meter_number']
    amount = float(data['amount'])

    headers = {
        "Authorization": f"Bearer {SECRET_KEY}"
    }

    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    result = response.json()

    if result['status'] and result['data']['status'] == 'success':
        token = generate_token(meter_number, amount)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Save to SQLite DB
        conn = sqlite3.connect('tokens.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tokens
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      meter_number TEXT,
                      amount REAL,
                      token TEXT,
                      timestamp TEXT)''')
        c.execute("INSERT INTO tokens (meter_number, amount, token, timestamp) VALUES (?, ?, ?, ?)",
                  (meter_number, amount, token, timestamp))
        conn.commit()
        conn.close()

        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Payment verification failed'}), 400

# ----------------------
# Run Server
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)