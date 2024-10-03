from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from googletrans import Translator
import sqlite3
import csv
import io
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions
translator = Translator()

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (create table)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            translated_text TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for the main translation page
@app.route('/', methods=['GET', 'POST'])
def translate():
    translated_text = ""
    if request.method == 'POST':
        text_to_translate = request.form['text']
        translated = translator.translate(text_to_translate, dest='el')  # Translate to Greek
        translated_text = translated.text

        # Insert the original and translated text into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (text, translated_text) VALUES (?, ?)', (text_to_translate, translated_text))
        conn.commit()
        conn.close()

    return render_template('index.html', translated_text=translated_text)

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['logged_in'] = True
            return redirect(url_for('transactions'))
        else:
            flash('Invalid Credentials')
    
    return render_template('login.html')

# Route for sign-up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        # After sign-up, redirect to the login page
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Route to view recent transactions (requires login)
@app.route('/transactions')
@login_required
def transactions():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('transactions.html', transactions=transactions)

# Route to download transactions as CSV
@app.route('/download_csv')
@login_required
def download_csv():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()

    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the CSV headers
    writer.writerow(['ID', 'Original Text', 'Translated Text'])

    # Write the data rows
    for transaction in transactions:
        writer.writerow([transaction['id'], transaction['text'], transaction['translated_text']])

    output.seek(0)

    # Send the CSV file as a response
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='transactions.csv'  # Correct usage of 'download_name'
    )

# Initialize the database on startup
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
