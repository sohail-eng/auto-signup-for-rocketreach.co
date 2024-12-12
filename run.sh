#!/bin/bash

# Get the Python file in the current directory
PYTHON_FILE=$(ls *.py | head -n 1)

# Check if a Python file exists
if [ -z "$PYTHON_FILE" ]; then
  echo "No Python file found in the current directory."
  exit 1
fi

# Run the Python script
echo "Running $PYTHON_FILE..."
python3 "$PYTHON_FILE"
