from student import Student
from results import DEFAULT_SUBJECTS, get_class_statistics
from storage import load_students, save_students
from reports import format_report_card, format_broadsheet, export_report_to_file


def find_student_by_id(students, student_id):
    target = student_id.strip().upper()
    for student in students:
        if student.student_id == target:
            return student
    return None


def add_student_ui(students):
    print("
--- REGISTER NEW STUDENT ---")
    while True:
        student_id = input("Enter Student ID (e.g., STU-001): ").strip().upper()
        if not Student.validate_student_id(student_id):
            print("Invalid ID format. Use 3-15 alphanumeric characters or hyphens.")
            continue
        if find_student_by_id(students, student_id):
            print("A student with this ID already exists.")
            continue
        break

    full_name = input("Enter Full Name: ").strip()
    while not full_name:
        full_name = input("Full Name cannot be empty. Enter Full Name: ").strip()

    student_class = input("Enter Class/Form (e.g., SS2A): ").strip()
    while not student_class:
        student_class = input("Class cannot be empty. Enter Class/Form: ").strip()

    gender = input("Enter Gender (Male/Female): ").strip().capitalize()
    while gender not in ("Male", "Female", "M", "F"):
        gender = input("Please enter Male or Female: ").strip().capitalize()
    if gender == "M":
        gender = "Male"
    elif gender == "F":
        gender = "Female"

    while True:
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        if Student.validate_dob(dob):
            break
        print("Invalid date format. Please use YYYY-MM-DD (e.g., 2008-05-14).")

    new_student = Student(student_id, full_name, student_class, gender, dob)
    students.append(new_student)
    save_students(students)
    print(f"Student '{new_student.full_name}' registered successfully!")


def view_all_students_ui(students):
    print("
--- ALL REGISTERED STUDENTS ---")
    if not students:
        print("No students registered yet.")
        return
    for idx, student in enumerate(students, start=1):
        print(f"{idx}. {student}")


def search_student_ui(students):
    print("
--- SEARCH STUDENT ---")
    query = input("Enter Student ID or Name to search: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    matches = [
        s for s in students
        if query in s.student_id.lower() or query in s.full_name.lower()
    ]
    if not matches:
        print("No matching student found.")
    else:
        print(f"Found {len(matches)} matching record(s):")
        for s in matches:
            print("  ->", s)


def update_student_ui(students):
    print("
--- UPDATE STUDENT INFORMATION ---")
    student_id = input("Enter Student ID to update: ").strip()
    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    print(f"Editing: {student}")
    print("Leave field blank to keep current value.")

    new_name = input(f"Full Name [{student.full_name}]: ").strip()
    if new_name:
        student.full_name = new_name.title()

    new_class = input(f"Class/Form [{student.student_class}]: ").strip()
    if new_class:
        student.student_class = new_class.upper()

    new_gender = input(f"Gender [{student.gender}]: ").strip().capitalize()
    if new_gender in ("Male", "Female"):
        student.gender = new_gender

    new_dob = input(f"Date of Birth [{student.dob}]: ").strip()
    if new_dob:
        if Student.validate_dob(new_dob):
            student.dob = new_dob
        else:
            print("Invalid DOB format ignored; keeping previous DOB.")

    save_students(students)
    print("Student record updated successfully.")


def delete_student_ui(students):
    print("
--- DELETE STUDENT RECORD ---")
    student_id = input("Enter Student ID to delete: ").strip()
    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    confirm = input(f"Are you sure you want to delete {student.full_name} ({student.student_id})? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student record deleted.")
    else:
        print("Deletion cancelled.")


def record_or_update_scores_ui(students):
    print("
--- RECORD / UPDATE SUBJECT SCORES ---")
    student_id = input("Enter Student ID: ").strip()
    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    print(f"Recording scores for: {student.full_name} ({student.student_id})")
    print("Default subjects:", ", ".join(DEFAULT_SUBJECTS))
    use_custom = input("Do you want to enter custom subject names instead? (y/n): ").strip().lower()

    subjects = []
    if use_custom == "y":
        print("Enter at least 5 subject names (type 'done' when finished):")
        while True:
            subj = input(f"Subject {len(subjects) + 1}: ").strip().title()
            if subj.lower() == "done":
                if len(subjects) >= 5:
                    break
                print(f"You must enter at least 5 subjects (currently {len(subjects)}).")
                continue
            if subj and subj not in subjects:
                subjects.append(subj)
    else:
        subjects = list(DEFAULT_SUBJECTS)

    new_scores = {}
    for subj in subjects:
        existing = student.scores.get(subj)
        prompt = f"Enter score for {subj} (0-100)" + (f" [Current: {existing}]: " if existing is not None else ": ")
        while True:
            raw = input(prompt).strip()
            if raw == "" and existing is not None:
                new_scores[subj] = existing
                break
            try:
                val = float(raw)
                if 0 <= val <= 100:
                    new_scores[subj] = round(val, 2)
                    break
                print("Score must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numeric score.")

    student.update_scores(new_scores)
    save_students(students)
    print("Scores saved successfully!")


def display_report_card_ui(students):
    print("
--- INDIVIDUAL STUDENT REPORT CARD ---")
    student_id = input("Enter Student ID: ").strip()
    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    report = format_report_card(student)
    print("
" + report)
    save_opt = input("
Save this report card to a text file? (y/n): ").strip().lower()
    if save_opt == "y":
        path = export_report_to_file(report, f"report_card_{student.student_id}.txt")
        if path:
            print(f"Report saved to: {path}")


def reporting_menu_ui(students):
    while True:
        print("
--- REPORTING & CLASS ANALYSIS ---")
        print("1. View All Results (Sorted by Average: Highest to Lowest)")
        print("2. View All Results (Sorted Alphabetically by Name)")
        print("3. View Class Statistics Summary")
        print("4. Export Full Class Broadsheet to Text File")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            print("
" + format_broadsheet(students, sort_by="average"))
        elif choice == "2":
            print("
" + format_broadsheet(students, sort_by="name"))
        elif choice == "3":
            stats = get_class_statistics(students)
            if not stats:
                print("No student scores recorded yet to compute statistics.")
            else:
                print("
--- CLASS STATISTICS ---")
                print(f"Students Evaluated : {stats['total_evaluated']}")
                print(f"Class Average      : {stats['class_average']:.2f}%")
                print(f"Highest Score Avg  : {stats['highest_avg']:.2f}% ({stats['highest_student'].full_name})")
                print(f"Lowest Score Avg   : {stats['lowest_avg']:.2f}% ({stats['lowest_student'].full_name})")
        elif choice == "4":
            broadsheet = format_broadsheet(students, sort_by="average")
            path = export_report_to_file(broadsheet)
            if path:
                print(f"Broadsheet report exported to: {path}")
        elif choice == "5":
            break
        else:
            print("Invalid option. Please choose 1-5.")


def main():
    students = load_students()
    print("=====================================================")
    print("   NEW HORIZON STUDENT RESULT MANAGEMENT SYSTEM")
    print("=====================================================")

    while True:
        print("
MAIN MENU:")
        print("1. Register New Student")
        print("2. View All Registered Students")
        print("3. Search Student (by ID or Name)")
        print("4. Update Student Information")
        print("5. Delete Student Record")
        print("6. Record / Update Subject Scores")
        print("7. View Individual Student Report Card")
        print("8. Class Reports, Ranking & Statistics")
        print("9. Exit")

        choice = input("
Enter your choice (1-9): ").strip()

        try:
            if choice == "1":
                add_student_ui(students)
            elif choice == "2":
                view_all_students_ui(students)
            elif choice == "3":
                search_student_ui(students)
            elif choice == "4":
                update_student_ui(students)
            elif choice == "5":
                delete_student_ui(students)
            elif choice == "6":
                record_or_update_scores_ui(students)
            elif choice == "7":
                display_report_card_ui(students)
            elif choice == "8":
                reporting_menu_ui(students)
            elif choice == "9":
                save_students(students)
                print("All records saved. Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
        except Exception as e:
            print(f"[Unexpected Error] An error occurred: {e}")


if __name__ == "__main__":
    main()
