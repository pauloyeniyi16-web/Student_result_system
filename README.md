# Student Result Management System

A console-based Python application developed to manage student academic records, subject scores, grade computations, class rankings, and persistent JSON storage.

## Features
- **Student Management:** Register, view, search (by ID or name), update, and delete student records with input validation.
- **Score & Result Management:** Record or update scores for at least 5 subjects, compute total and average scores, assign letter grades (`A`–`F`), and generate individual report cards.
- **Reporting & Class Analysis:** Rank students by average score, sort alphabetically by name, calculate class statistics (highest, lowest, and class average), and export reports to `.txt` files.
- **Data Persistence:** Automatically saves and loads student data from `data/students.json` with error handling for missing or corrupted files.

## Project Structure
```text
student_result_system/
├── main.py                 # Entry point and interactive CLI menu
├── student.py              # Student class, regex validation, and serialization
├── results.py              # Total, average, grading, and class statistics logic
├── storage.py              # JSON file reading, writing, and directory management
├── reports.py              # Report card formatting, broadsheets, and file export
├── data/
│   └── students.json       # Persistent JSON database (pre-populated with sample data)
├── reports_output/         # Directory where exported .txt reports are saved
└── README.md               # Project documentation
```

## How to Run (VS Code or IntelliJ IDEA)
1. Extract the `student_result_system` folder from the ZIP archive.
2. Open the `student_result_system` folder in **VS Code** or **IntelliJ IDEA**.
3. Ensure Python 3.8+ is selected as your project interpreter (uses only Python Standard Library modules—no `pip install` required).
4. Open `main.py` and click **Run** (or run `python main.py` in the integrated terminal).
