"""Exercises: ORM fundamentals.

Implement the TODO functions. Autograder will test them.
"""

from __future__ import annotations

from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.flask_orm.extensions import db
from src.flask_orm.models import Student, Grade


def create_student(name: str, email: str) -> Student:
    student = Student(name=name, email=email)
    db.session.add(student)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("email must be unique")
    return student


def find_student_by_email(email: str) -> Optional[Student]:
    return Student.query.filter_by(email=email).first()



def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    grade = Grade(student_id=student_id, assignment_id=assignment_id, score=score)
    db.session.add(grade)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("grade for this student and assignment already exists")
    return grade


def average_percent(student_id: int) -> float:
    avg_score = db.session.query(func.avg(Grade.score)).filter_by(student_id=student_id).scalar()
    if avg_score is None:
        return 0.0
    return float(avg_score)
