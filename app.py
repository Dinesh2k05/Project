from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from pymongo import MongoClient
import urllib.parse

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# MongoDB configuration
username = "Dinesh"
password = "Dkimp@2005"
database_name = "cluster0"

encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.mongodb.net/{database_name}?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db = client[database_name]
events_collection = db["events"]

# Example data structure for seat availability
seats_data = {
    '11-11:00': {i: 'available' for i in range(1, 100)},
    '11-02:00': {i: 'available' for i in range(1, 100)},
    '12-11:00': {i: 'available' for i in range(1, 100)},
    # Add more as needed
}

# Example booked seats
seats_data['11-11:00'][1] = 'booked'
seats_data['11-11:00'][2] = 'booked'
seats_data['12-11:00'][3] = 'booked'

# Define users with username and password pairs
users = {
    'user1': 'password1',
    'user2': 'password2',
    # Add more users as needed
}

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
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('movie_page'))
        else:
            error_message = "Incorrect username or password. Please try again."
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Add your registration logic here
    # For example, save the user details to the database
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

        if key not in seats_data:
            seats_data[key] = {i: 'available' for i in range(1, 100)}
        
        response = {'status': 'success', 'booked': [], 'already_booked': []}

        for seat in selected_seats:
            if seats_data[key].get(seat) == 'available':
                seats_data[key][seat] = 'booked'
                response['booked'].append(seat)
            else:
                response['already_booked'].append(seat)

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
        return jsonify(seats_data.get(key, {i: 'available' for i in range(1, 100)}))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
