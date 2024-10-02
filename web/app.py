import logging
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response
from werkzeug.utils import secure_filename
from transformers import MarianMTModel, MarianTokenizer
import os
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ensure the notes upload folder exists
app.config['NOTES_FOLDER'] = 'notes_uploads'
if not os.path.exists(app.config['NOTES_FOLDER']):
    os.makedirs(app.config['NOTES_FOLDER'])

# Reduce verbosity
logging.basicConfig(level=logging.ERROR)

# Load the MarianMT model and tokenizer for English to Hebrew translation
model_name = "Helsinki-NLP/opus-mt-en-he"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_to_hebrew(text, model, tokenizer):
    # Encode the input text
    inputs = tokenizer.encode(text, return_tensors="pt", truncation=True, padding=True)
    
    # Generate translation
    outputs = model.generate(inputs, max_length=512, num_beams=5, early_stopping=True)
    
    # Decode the generated text
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

def remove_unwanted_phrases(text, phrases):
    for phrase in phrases:
        text = text.replace(phrase, "")
    return text

def reverse_text(text):
    return text[::-1]

def save_to_database(input_text, translated_text, reversed_text, timestamp, db_path="translations.db"):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            translated_text TEXT,
            reversed_text TEXT,
            timestamp TEXT
        )
    ''')

    # Insert the data into the database
    cursor.execute('''
        INSERT INTO translations (input_text, translated_text, reversed_text, timestamp) VALUES (?, ?, ?, ?)
    ''', (input_text, translated_text, reversed_text, timestamp))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def save_note_to_database(note_text, image_filename, timestamp, db_path="translations.db"):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_text TEXT,
            image_filename TEXT,
            timestamp TEXT
        )
    ''')

    # Insert the data into the database
    cursor.execute('''
        INSERT INTO notes (note_text, image_filename, timestamp) VALUES (?, ?, ?)
    ''', (note_text, image_filename, timestamp))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            translated_text TEXT,
            reversed_text TEXT,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_text TEXT,
            image_filename TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form.get('input_text', '')
    file = request.files.get('file')

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        with open(file_path, 'r') as f:
            input_text = f.read()

    if not input_text:
        flash('Please enter text or upload a file')
        return redirect(url_for('index'))

    # Translate the text to Hebrew
    translated_text = translate_to_hebrew(input_text, model, tokenizer)

    # Remove unwanted phrases
    unwanted_phrases = ["his"]
    translated_text = remove_unwanted_phrases(translated_text, unwanted_phrases)

    # Reverse the translated text
    reversed_text = reverse_text(translated_text)

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Save the translated text and additional data to the SQLite database
    save_to_database(input_text, translated_text, reversed_text, timestamp)

    return render_template('index.html', input_text=input_text, translated_text=translated_text, reversed_text=reversed_text, timestamp=timestamp)

@app.route('/recent_translations')
def recent_translations():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_text, translated_text FROM translations ORDER BY id DESC LIMIT 10')
    translations = cursor.fetchall()
    conn.close()
    return render_template('recent_translations.html', translations=translations)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('translations.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT input_text, translated_text FROM translations 
            WHERE input_text LIKE ? OR translated_text LIKE ?
        ''', ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
        conn.close()
    return render_template('search.html', query=query, results=results)

@app.route('/export_recent')
def export_recent():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_text, translated_text FROM translations ORDER BY id DESC LIMIT 10')
    translations = cursor.fetchall()
    conn.close()
    return export_to_csv(translations, 'recent_translations.csv')

@app.route('/export_search', methods=['POST'])
def export_search():
    query = request.form['query']
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT input_text, translated_text FROM translations 
        WHERE input_text LIKE ? OR translated_text LIKE ?
    ''', ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()
    return export_to_csv(results, 'search_results.csv')

def export_to_csv(data, filename):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Input Text', 'Translated Text'])
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={filename}"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        note_text = request.form['note_text']
        file = request.files.get('file')
        image_filename = None
        if file:
            image_filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['NOTES_FOLDER'], image_filename)
            file.save(file_path)
        timestamp = datetime.now().isoformat()
        save_note_to_database(note_text, image_filename, timestamp)
        flash('Note saved successfully!')
        return redirect(url_for('notes'))
    
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT note_text, image_filename, timestamp FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)

@app.route('/notes_uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['NOTES_FOLDER'], filename))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)