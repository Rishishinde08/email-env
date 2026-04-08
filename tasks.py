def grade_easy(predicted, expected):
    return 0.8 if predicted == expected else 0.2

def grade_medium(predicted, expected):
    return 0.85 if predicted == expected else 0.3

def grade_hard(predicted, expected):
    return 0.9 if predicted == expected else 0.4


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