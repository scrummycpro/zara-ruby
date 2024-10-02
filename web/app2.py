from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file, make_response
from werkzeug.utils import secure_filename
from transformers import MarianMTModel, MarianTokenizer
import os
import csv
from io import StringIO
import sqlite3
from datetime import datetime

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
import logging
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
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Translation App</title>
            <style>
                body {
                    background-color: #fce4ec; /* Light pink */
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: #ffffff; /* White */
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    padding: 30px;
                    border-radius: 10px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                .btn-primary {
                    background-color: #ba68c8; /* Purple */
                    border-color: #ba68c8;
                }
                .btn-primary:hover {
                    background-color: #9c27b0; /* Darker purple */
                    border-color: #9c27b0;
                }
                .alert {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="text-align: center; color: #9c27b0;">Translation App</h1>
                <form action="{{ url_for('translate') }}" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="input_text" style="color: #9c27b0;">Enter text or upload a file:</label>
                        <textarea class="form-control" id="input_text" name="input_text" rows="5">{{ input_text }}</textarea>
                        <input type="file" class="form-control-file mt-3" id="file" name="file">
                    </div>
                    <button type="submit" class="btn btn-primary">Translate</button>
                </form>
                
                {% if translated_text %}
                <div class="mt-5">
                    <h3>Translated Text:</h3>
                    <p>{{ translated_text }}</p>
                    <h3>Reversed Text:</h3>
                    <p>{{ reversed_text }}</p>
                    <p style="color: #9c27b0;">Translated on: {{ timestamp }}</p>
                </div>
                {% endif %}
                
                {% with messages = get_flashed_messages() %}
                {% if messages %}
                <div class="alert alert-info">
                    {% for message in messages %}
                    <p>{{ message }}</p>
                    {% endfor %}
                </div>
                {% endif %}
                {% endwith %}
            </div>
        </body>
        </html>
    ''')

@app.route('/recent_translations')
def recent_translations():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_text, translated_text FROM translations ORDER BY id DESC LIMIT 10')
    translations = cursor.fetchall()
    conn.close()
    
    html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Recent Translations</title>
            <style>
                body {
                    background-color: #fce4ec; /* Light pink */
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: #ffffff; /* White */
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    padding: 30px;
                    border-radius: 10px;
                }
                .translation-item {
                    margin-bottom: 20px;
                    padding: 20px;
                    border: 1px solid #e1bee7; /* Light purple */
                    background-color: #ffffff; /* White */
                    box-shadow: 0 0 5px rgba(0,0,0,0.1);
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="text-align: center; color: #9c27b0;">Recent Translations</h1>
                <div class="translation-list">
    '''

    for input_text, translated_text in translations:
        html += '''
            <div class="translation-item">
                <h3 style="color: #9c27b0;">Input Text:</h3>
                <p>{{ input_text }}</p>
                <h3 style="color: #9c27b0;">Translated Text:</h3>
                <p>{{ translated_text }}</p>
            </div>
        '''

    html += '''
                </div>
            </div>
        </body>
        </html>
    '''

    return html

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

