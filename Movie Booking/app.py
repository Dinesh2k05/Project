from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import urllib.parse
from pymongo import MongoClient
import certifi
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'


username = "Dinesh"
password = "Dkimp2005"
database_name = "cluster0"


encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)


connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.mongodb.net/{database_name}?retryWrites=true&w=majority"
client = MongoClient('mongodb+srv://Dinesh:Dkimp2005@cluster0.hlwz20a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Select database and collection
db = client[database_name]
users_collection = db["users"]
seats_collection = db["seats"]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['logged_in'] = True
            session['username'] = username  # Ensure this is set
            return redirect(url_for('movie_page'))
        else:
            error_message = "Incorrect username or password. Please try again."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username already exists
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            error_message = "Username already exists. Please choose a different one."
            return render_template('register.html', error_message=error_message)

        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the user in the database
        users_collection.insert_one({"username": username, "password": hashed_password, "email": email})

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Handle password reset logic here
        # For example, send a password reset link via email
        return redirect(url_for('login'))  # Redirect after processing
    return render_template('forgot_password.html')  # Render a page with a password reset form


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

        total_amount = len(response['booked']) * 200  # Assuming each ticket costs 200
        return jsonify({
            'status': 'success',
            'redirect_url': url_for('transaction_page', date=date, time=time, seats=','.join(response['booked']), amount=total_amount)
        })
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

@app.route('/transaction')
def transaction_page():
    if 'logged_in' in session:
        date = request.args.get('date')
        time = request.args.get('time')
        seats = request.args.get('seats')
        amount = request.args.get('amount')
        return render_template('transaction.html', date=date, time=time, seats=seats, amount=amount)
    return redirect(url_for('index'))

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'logged_in' in session:
        return render_template('confirmbooking.html')
    return redirect(url_for('index'))

@app.route('/orderhistory')
def order_history():
    # Define the date-time keys you want to fetch
    date_time_keys = [
        '11-11:00', '11-02:00', '11-06:00', '11-10:00',
        '12-11:00', '12-02:00', '12-06:00', '12-10:00',
        '13-11:00', '13-02:00', '13-06:00', '13-10:00',
        '14-11:00', '14-02:00', '14-06:00', '14-10:00'
    ]
    
    remaining_seats = []
    
    # Fetch seat details for each date-time key
    for key in date_time_keys:
        seat_data = seats_collection.find_one({"key": key})
        if seat_data:
            remaining_seats.append({
                "key": seat_data['key'],  # Date-Time key
                "booked_seats": [seat for seat, status in seat_data['seats'].items() if status == 'booked'],
                "available_seats": [seat for seat, status in seat_data['seats'].items() if status == 'available']
            })

    return render_template('orderhistory.html', remaining_seats=remaining_seats)




if __name__ == '__main__':
    app.run(debug=True)