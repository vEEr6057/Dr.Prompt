from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import schedule
import time
from threading import Thread
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT  # Claude API import
import os

app = Flask(__name__)

# Set up Claude API key (use your actual API key from Anthropic)
anthropic = Anthropic(api_key="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")

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT,
            specialty TEXT,
            location TEXT,
            hospital TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to interact with Claude's AI for generating responses
def get_ai_response(message):
    # Use Claude to generate a response
    completion = anthropic.completions.create(
        prompt=f"{HUMAN_PROMPT} {message} {AI_PROMPT}",
        max_tokens_to_sample=100
    )
    return completion['completion'].strip()

# Serve the HTML file
@app.route('/')
def serve_html():
    return send_from_directory('static', 'index.html')

# Serve JavaScript and CSS
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Handle favicon request to avoid 404
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Route to schedule doctor visit
@app.route('/schedule_visit', methods=['POST'])
def schedule_visit():
    data = request.json
    doctor = data['doctor']
    rep_availability = data['availability']

    # Suggest optimal visit time logic (simplified)
    suggestion = f"I recommend visiting {doctor['name']} at {doctor['location']} on {rep_availability['date']} at {rep_availability['time']}."

    return jsonify({'suggestion': suggestion})

# Route to add a doctor to the database
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    data = request.json
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO doctors (name, specialty, location, hospital, contact)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['specialty'], data['location'], data['hospital'], data['contact']))
    conn.commit()
    conn.close()
    return jsonify({"status": "Doctor added successfully"})

# Route to get doctor details and suggest appointment
@app.route('/get_doctor_details', methods=['POST'])
def get_doctor_details():
    name = request.json['name']
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute("SELECT * FROM doctors WHERE name=?", (name,))
    doctor = c.fetchone()
    conn.close()

    if doctor:
        doctor_info = {
            "name": doctor[1],
            "specialty": doctor[2],
            "location": doctor[3],
            "hospital": doctor[4],
            "contact ": doctor[5]
        }
        return jsonify(doctor_info)
    else:
        return jsonify({"error": "Doctor not found"}), 404

# Function to handle reminders and notifications
def reminder_handler():
    schedule.every().day.at("09:00").do(send_reminders)

    while True:
        schedule.run_pending()
        time.sleep(60)

def send_reminders():
    # Logic to send reminders (placeholder)
    print("Sending reminders...")

# Start reminder thread
reminder_thread = Thread(target=reminder_handler)
reminder_thread.start()

if __name__ == '__main__':
    init_db()
    conn = sqlite3.connect('doctors.db')
    c = conn.cursor()
    c.execute("INSERT INTO doctors VALUES (NULL, 'show doctor available ',NULL, 'all are being scheduled please wait' , NULL, NULL)")
    c.execute("INSERT INTO doctors VALUES (NULL, 'when will be my meeting then ',NULL, ' soon we will inform you about it as of now you are on waitlist' , NULL, NULL)")
    conn.commit()
    conn.close()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
