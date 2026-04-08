from grader import grade

TASKS = {
    "easy_spam_detection": {
        "input": "Win a FREE iPhone now!!!",
        "expected": "spam",
        "grader": grade
    },
    "medium_classification": {
        "input": "Meeting at 5 PM today",
        "expected": "urgent",
        "grader": grade
    },
    "hard_classification": {
        "input": "Lunch tomorrow?",
        "expected": "normal",
        "grader": grade
    }
}