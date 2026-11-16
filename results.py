DEFAULT_SUBJECTS = ("Mathematics", "English Language", "Physics", "Chemistry", "Biology")


def calculate_total(scores):
    """Calculates the total score across all recorded subjects."""
    if not scores:
        return 0.0
    return round(sum(scores.values()), 2)


def calculate_average(scores):
    """Calculates the average score across all recorded subjects."""
    if not scores:
        return 0.0
    return round(sum(scores.values()) / len(scores), 2)


def assign_grade(average):
    """Assigns a letter grade and remark based on average score."""
    if average >= 75:
        return "A", "Distinction"
    elif average >= 65:
        return "B", "Very Good"
    elif average >= 50:
        return "C", "Credit"
    elif average >= 40:
        return "D", "Pass"
    else:
        return "F", "Fail"


def evaluate_student(student):
    """Returns a summary tuple/dict of total, average, grade, and remark for a student."""
    total = calculate_total(student.scores)
    average = calculate_average(student.scores)
    grade, remark = assign_grade(average) if student.scores else ("N/A", "No Scores Recorded")
    return {
        "total": total,
        "average": average,
        "grade": grade,
        "remark": remark,
    }


def get_class_statistics(students):
    """Computes highest average, lowest average, and overall class average."""
    scored_students = [s for s in students if s.scores]
    if not scored_students:
        return None

    averages = [(s, calculate_average(s.scores)) for s in scored_students]
    highest_student, highest_avg = max(averages, key=lambda item: item[1])
    lowest_student, lowest_avg = min(averages, key=lambda item: item[1])
    class_avg = round(sum(avg for _, avg in averages) / len(averages), 2)

    return {
        "total_evaluated": len(scored_students),
        "highest_student": highest_student,
        "highest_avg": highest_avg,
        "lowest_student": lowest_student,
        "lowest_avg": lowest_avg,
        "class_average": class_avg,
    }
