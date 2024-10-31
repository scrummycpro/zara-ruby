from flask import Flask, render_template, request, redirect, url_for, flash
from googletrans import Translator
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

translator = Translator()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

languages = {
    'he': 'Hebrew',
    'ar': 'Arabic',
    'el': 'Greek',
    'la': 'Latin',
}

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Translation model
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    translated_texts = db.Column(db.PickleType, nullable=False)  # Store translations as a dictionary
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Associate translations with a user

    def __repr__(self):
        return f"<Translation {self.id}>"

# Context processor to inject variables into templates
@app.context_processor
def inject_globals():
    return {
        'languages': languages,
        'current_year': datetime.now().year,
        'current_user': current_user,
    }

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Input validation
        if not username or not password:
            flash('Please enter a username and password.', 'error')
            return redirect(url_for('register'))

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Removed the redirect to allow access to the login page even if already authenticated
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Main translation page
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    translated_texts = {}
    reversed_texts = {}

    if request.method == 'POST':
        # Print form data for debugging
        print("Form data received:", request.form.to_dict())

        # Safely get 'text' from the form data
        text = request.form.get('text', '').strip()
        if not text:
            flash('Please enter text to translate.', 'error')
        else:
            for lang_code, lang_name in languages.items():
                translation = translator.translate(text, dest=lang_code)
                translated_text = translation.text
                translated_texts[lang_name] = translated_text
                reversed_texts[lang_name] = translated_text[::-1]

            # Save to database
            new_translation = Translation(
                original_text=text,
                translated_texts=translated_texts,
                user_id=current_user.id
            )
            db.session.add(new_translation)
            db.session.commit()

    return render_template('index.html', translated_texts=translated_texts, reversed_texts=reversed_texts)

# Recent translations page
@app.route('/recent', methods=['GET'])
@login_required
def recent():
    search_query = request.args.get('search', '').strip()
    if search_query:
        translations = Translation.query.filter(
            Translation.user_id == current_user.id,
            Translation.original_text.contains(search_query)
        ).order_by(Translation.timestamp.desc()).all()
    else:
        translations = Translation.query.filter_by(user_id=current_user.id).order_by(Translation.timestamp.desc()).limit(10).all()
    return render_template('recent.html', translations=translations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
