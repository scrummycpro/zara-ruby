Sure, here's a detailed README.md file that includes all the code provided:

```markdown
# Food Logger Application

This is a simple Python application that allows users to log their food intake. The application provides a graphical user interface (GUI) built using the Tkinter library and stores data in an SQLite database.

## Features

- Users can enter their name.
- Users can select multiple food items from a list.
- Users can log their selected food items.
- Data is stored in an SQLite database.
- Pre-defined food items with portion sizes are included.
- Instructions on how to use the application are displayed.

## Requirements

- Python 3
- Tkinter (usually included with Python)
- SQLite (usually included with Python)

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/food-logger.git
cd food-logger
```

2. Run the `food.py` script:

```bash
python3 food.py
```

3. Follow the instructions displayed in the GUI to log your food intake.

## Code Explanation

- `food.py`: This is the main Python script that contains the GUI code and the logic to interact with the SQLite database.
- `meals.db`: This is the SQLite database file that stores the food items and logs.
- `README.md`: This file contains instructions and information about the application.

The `food.py` script contains the following components:

- GUI setup: The Tkinter library is used to create the graphical user interface.
- Database setup: The SQLite database is created with three tables: `foods`, `food_logs`, and `all_foods`. The `foods` table stores the pre-defined food items with portion sizes. The `food_logs` table stores the logs of food intake. The `all_foods` table stores all food items logged by users.
- Functions: 
  - `create_tables()`: This function creates the required tables in the database and inserts pre-defined food items into the `foods` table.
  - `insert_food()`: This function inserts the selected food items into the `food_logs` table and the `all_foods` table.
  - `close_app()`: This function closes the application.
- GUI elements: Entry widgets for entering the user's name, a Listbox widget for selecting food items, Buttons for logging food and closing the application, and Labels for displaying instructions and status messages.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

Feel free to customize the README according to your project's specifics.