import re
from datetime import datetime


class Student:
    """Represents a student and their academic records."""

    def __init__(self, student_id, full_name, student_class, gender, dob, scores=None, last_updated=None):
        self.student_id = student_id.strip().upper()
        self.full_name = full_name.strip().title()
        self.student_class = student_class.strip().upper()
        self.gender = gender.strip().capitalize()
        self.dob = dob.strip()
        self.scores = scores if scores is not None else {}
        self.last_updated = last_updated if last_updated else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def validate_student_id(student_id):
        """Validates Student ID format (e.g., STU-001 or NH2026001)."""
        pattern = r"^[A-Za-z0-9-]{3,15}$"
        return bool(re.match(pattern, student_id.strip()))

    @staticmethod
    def validate_dob(dob_str):
        """Validates Date of Birth format (YYYY-MM-DD)."""
        try:
            datetime.strptime(dob_str.strip(), "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def update_scores(self, new_scores):
        """Updates subject scores and refreshes timestamp."""
        self.scores.update(new_scores)
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the Student object into a dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "student_class": self.student_class,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Student object from a dictionary."""
        return cls(
            student_id=data["student_id"],
            full_name=data["full_name"],
            student_class=data["student_class"],
            gender=data["gender"],
            dob=data["dob"],
            scores=data.get("scores", {}),
            last_updated=data.get("last_updated"),
        )

    def __str__(self):
        return f"[{self.student_id}] {self.full_name} | Class: {self.student_class} | Gender: {self.gender} | DOB: {self.dob}"
