#!/bin/bash

# Function to generate story from API and store in SQLite
generate_and_store_story() {
    local prompt="$1"

    # Default prompt if not provided
    if [ -z "$prompt" ]; then
        prompt="Write me a 500 word story about a witch that eats children."
    fi

    # API request and capture response
    response=$(curl -s -X POST http://localhost:11434/api/generate \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"llama3\", \"prompt\": \"$prompt\", \"stream\": false}")  

    # Extract story from response
    story=$(echo "$response" | jq -r '.response')

    # Get current timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # SQLite database file
    database_file="stories.db"

    # Check if database file exists; create if not
    if [ ! -f "$database_file" ]; then
        sqlite3 "$database_file" <<EOF
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    story_text TEXT
);
EOF
    fi

    # Escape single quotes in story text for SQL insertion
    story_escaped=$(echo "$story" | sed "s/'/''/g")

    # SQL command to insert the story into the database
    sql_command="INSERT INTO stories (timestamp, story_text) VALUES ('$timestamp', '$story_escaped');"

    # Execute SQL command using sqlite3
    echo "$sql_command" | sqlite3 "$database_file"
}

# Call the function with or without prompt argument
generate_and_store_story "$@"

