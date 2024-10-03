Here’s a sample **README.md** file for your Flask translation application:

---

# Flask Greek Translator App

## Overview

This is a simple web application built with Flask that allows users to input sentences in English and get them translated into Greek. The application also stores the original and translated sentences in a SQLite database. Users can view the most recent translations in a luxury-styled list, and download them as a CSV file.

### Key Features:
- **Sentence Translation**: Translates sentences from English to Greek using Google Translate API.
- **User Authentication**: Users must sign up and log in to view or download their translation history.
- **Transaction History**: Displays the last 10 translation transactions.
- **Download as CSV**: Users can download all transactions in CSV format.
- **Modern UI**: The app features a moving gradient background and luxury design.
  
## Installation

### Prerequisites
- Python 3.x installed on your system.
- Flask and its dependencies (`Flask`, `sqlite3`, `googletrans`).

### Setup Instructions

1. Clone this repository or download the files.
   
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory.

   ```bash
   cd flask-greek-translator
   ```

3. Install the required Python dependencies.

   ```bash
   pip install Flask googletrans==4.0.0-rc1
   ```

4. Run the Flask application.

   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

### Sign Up and Login
1. Start by signing up for an account on the `/signup` page.
2. After successfully signing up, log in using the `/login` page.
3. Once logged in, you can access the translator and transaction history.

### Translate a Sentence
1. Enter an English sentence on the homepage.
2. Click "Translate" to get the translated sentence in Greek.
3. The translation will be stored in the database for future reference.

### View Transaction History
1. After logging in, navigate to the `/transactions` page.
2. You will see a luxury-styled list of the 10 most recent translations.
3. Use the "Download as CSV" button to export the translations to a CSV file.

## Project Structure

```
/flask-greek-translator
    ├── app.py                  # Main application logic
    ├── transactions.db          # SQLite database (auto-created)
    ├── templates/
    │     ├── index.html         # Homepage (translation form)
    │     ├── login.html         # Login page
    │     ├── signup.html        # Signup page
    │     └── transactions.html  # Transaction history page
    └── README.md                # Project documentation
```

## Technologies Used

- **Flask**: Web framework for Python.
- **SQLite**: Lightweight database for transaction storage.
- **Googletrans**: Python API for Google Translate.
- **Bootstrap**: For responsive and modern UI design.
- **HTML/CSS**: For structure and styling.

## Known Issues
- Make sure that you have a stable internet connection for the Google Translate API to work.

## Future Enhancements
- Add password hashing for secure user authentication.
- Add more languages for translation.
- Implement user-specific translation histories.

## License
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

You can adjust the content based on your specific needs or add more details if necessary.