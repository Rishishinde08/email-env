# tasks.py

from grader import grade_easy, grade_medium, grade_hard

TASKS = [
    {
        "name": "easy_spam_detection",
        "input": "Win a FREE iPhone now!!!",
        "expected": "spam",
        "grader": grade_easy
    },
    {
        "name": "medium_classification",
        "input": "Meeting at 5 PM today",
        "expected": "urgent",
        "grader": grade_medium
    },
    {
        "name": "hard_classification",
        "input": "Lunch tomorrow?",
        "expected": "normal",
        "grader": grade_hard
    }
]