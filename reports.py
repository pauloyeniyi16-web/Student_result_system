import os
from datetime import datetime
from results import evaluate_student, get_class_statistics


def format_report_card(student):
    """Generates a formatted individual student report card string."""
    eval_data = evaluate_student(student)
    lines = [
        "=" * 55,
        "          STUDENT ACADEMIC REPORT CARD",
        "=" * 55,
        f"Student ID   : {student.student_id}",
        f"Full Name    : {student.full_name}",
        f"Class / Form : {student.student_class}",
        f"Gender       : {student.gender}",
        f"Date of Birth: {student.dob}",
        f"Last Updated : {student.last_updated}",
        "-" * 55,
        f"{'SUBJECT':<30} {'SCORE':>10} {'GRADE':>10}",
        "-" * 55,
    ]

    if not student.scores:
        lines.append("No subject scores recorded yet.")
    else:
        for subject, score in student.scores.items():
            subj_grade = (
                "A" if score >= 75 else
                "B" if score >= 65 else
                "C" if score >= 50 else
                "D" if score >= 40 else "F"
            )
            lines.append(f"{subject:<30} {score:>10.2f} {subj_grade:>10}")

    lines.extend([
        "-" * 55,
        f"Total Score  : {eval_data['total']:.2f}",
        f"Average Score: {eval_data['average']:.2f}%",
        f"Final Grade  : {eval_data['grade']} ({eval_data['remark']})",
        "=" * 55,
    ])
    return "
".join(lines)


def format_broadsheet(students, sort_by="average"):
    """Generates a formatted broadsheet listing all students."""
    if not students:
        return "No student records available."

    if sort_by == "name":
        sorted_students = sorted(students, key=lambda s: s.full_name.lower())
    else:
        sorted_students = sorted(
            students,
            key=lambda s: evaluate_student(s)["average"],
            reverse=True
        )

    header = (
        "=" * 82 + "
"
        f"{'RANK':<6} {'ID':<12} {'FULL NAME':<24} {'CLASS':<8} {'TOTAL':>8} {'AVG (%)':>9} {'GRADE':>7}
"
        + "-" * 82
    )
    rows = [header]

    for idx, student in enumerate(sorted_students, start=1):
        ev = evaluate_student(student)
        rows.append(
            f"{idx:<6} {student.student_id:<12} {student.full_name[:23]:<24} "
            f"{student.student_class:<8} {ev['total']:>8.2f} {ev['average']:>8.2f}% {ev['grade']:>6}"
        )

    rows.append("=" * 82)
    stats = get_class_statistics(students)
    if stats:
        rows.extend([
            "CLASS PERFORMANCE SUMMARY:",
            f"  Students Evaluated : {stats['total_evaluated']}",
            f"  Class Average      : {stats['class_average']:.2f}%",
            f"  Highest Average    : {stats['highest_avg']:.2f}% ({stats['highest_student'].full_name})",
            f"  Lowest Average     : {stats['lowest_avg']:.2f}% ({stats['lowest_student'].full_name})",
            "=" * 82,
        ])
    return "
".join(rows)


def export_report_to_file(content, filename=None):
    """Saves a text report to the reports_output directory."""
    os.makedirs("reports_output", exist_ok=True)
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_report_{timestamp}.txt"

    filepath = os.path.join("reports_output", filename)
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return filepath
    except OSError as e:
        print(f"[Error] Could not export report: {e}")
        return None
