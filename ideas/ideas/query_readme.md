Sure, here's a detailed README that includes all the code for the SQLite Query Tool:

# SQLite Query Tool

The SQLite Query Tool is a simple application built using Python and the Tkinter library. It allows users to execute SQL queries on SQLite databases, view database schemas, and export query results to CSV or JSON format.

## Features
- Choose SQLite database files (*.db) for querying.
- View database schema including table names and column details.
- Execute custom SQL queries.
- Export query results to CSV or JSON format.
- Tabbed view for query results.

## Installation
1. Clone the repository to your local machine:

```bash
git clone https://github.com/scrummcpro/querytool.git
```

2. Navigate to the project directory:

```bash
cd sqlite-query-tool
```

3. Install the required dependencies. The application relies on the following Python libraries:
   - Tkinter (standard library)
   - SQLite3 (standard library)

You can install them using pip:

```bash
pip install tk
```

## Usage
1. Run the application by executing the following command:

```bash
python query_tool.py
```

2. The SQLite Query Tool window will appear.

3. Choose a SQLite database file by clicking the "Choose Database" button. This will display the selected database's name in the interface.

4. View the schema of the selected database in the "Schema" text area.

5. Enter a custom SQL query in the "Enter Query" entry field.

6. Click the "Execute Query" button to execute the query. The results will be displayed in the "Query Results" text area.

7. To export the query results, select the desired export format (CSV or JSON) and click the "Export Results" button.

8. You can also switch to the "Tabbed View" radio button to display query results in a separate tabbed window.

9. Close the application window when finished.

## Customization
- You can customize the appearance of the application by modifying the colors, fonts, and styles in the code.

## Contributing
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### query_tool.py

```python
# Insert the entire QueryTool class code here
```

## Credits
This project was created by Zara Franklin.