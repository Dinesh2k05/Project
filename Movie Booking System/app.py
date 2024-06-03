from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import urllib.parse
from pymongo import MongoClient
import certifi

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# MongoDB credentials
username = "Dinesh"
password = "Dkimp2005"
database_name = "cluster0"

# Encode username and password
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Construct the connection string
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.mongodb.net/{database_name}?retryWrites=true&w=majority"
client = MongoClient('mongodb+srv://Dinesh:Dkimp2005@cluster0.hlwz20a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Select database and collection
db = client[database_name]
users_collection = db["users"]
seats_collection = db["seats"]

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({"username": username})
        if user and user['password'] == password:
            session['logged_in'] = True
            return redirect(url_for('movie_page'))
        else:
            error_message = "Incorrect username or password. Please try again."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    if users_collection.find_one({"username": username}):
        flash('Username already exists. Please choose a different one.')
        return redirect(url_for('index'))
    
    users_collection.insert_one({"username": username, "email": email, "password": password})
    flash('Registration successful! Please login.')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    if 'logged_in' in session:
        selected_seats = request.json.get('selected_seats', [])
        date = request.json.get('date')
        time = request.json.get('time')
        key = f"{date}-{time}"

        seats = seats_collection.find_one({"key": key})
        if not seats:
            seats = {"key": key, "seats": {str(i): 'available' for i in range(1, 100)}}
            seats_collection.insert_one(seats)
        
        response = {'status': 'success', 'booked': [], 'already_booked': []}
        for seat in selected_seats:
            seat = str(seat)
            if seats['seats'].get(seat) == 'available':
                seats['seats'][seat] = 'booked'
                response['booked'].append(seat)
            else:
                response['already_booked'].append(seat)

        seats_collection.update_one({"key": key}, {"$set": {"seats": seats['seats']}})
        return jsonify(response)
    return redirect(url_for('index'))

@app.route('/movies')
def movie_page():
    if 'logged_in' in session:
        return render_template('movies.html')
    return redirect(url_for('index'))

@app.route('/book1')
def seat_booking1():
    if 'logged_in' in session:
        return render_template('book1.html')
    return redirect(url_for('index'))

@app.route('/book2')
def seat_booking2():
    if 'logged_in' in session:
        return render_template('book2.html')
    return redirect(url_for('index'))

@app.route('/book3')
def seat_booking3():
    if 'logged_in' in session:
        return render_template('book3.html')
    return redirect(url_for('index'))

@app.route('/book4')
def seat_booking4():
    if 'logged_in' in session:
        return render_template('book4.html')
    return redirect(url_for('index'))

@app.route('/seats', methods=['GET'])
def get_seats():
    if 'logged_in' in session:
        date = request.args.get('date')
        time = request.args.get('time')
        key = f"{date}-{time}"
        seats = seats_collection.find_one({"key": key})
        if not seats:
            seats = {str(i): 'available' for i in range(1, 100)}
        else:
            seats = seats['seats']
        return jsonify(seats)
    return redirect(url_for('index'))

@app.route('/initialize_seats', methods=['POST'])
def initialize_seats():
    # Initialize seat availability for a specific date and time
    date = request.form['date']
    time = request.form['time']
    key = f"{date}-{time}"

    if seats_collection.find_one({"key": key}):
        flash('Seats already initialized for this date and time.')
    else:
        seats_collection.insert_one({"key": key, "seats": {str(i): 'available' for i in range(1, 100)}})
        flash('Seats initialized successfully.')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
