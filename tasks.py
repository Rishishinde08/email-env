from grader import grade_easy, grade_medium, grade_hard

def easy_spam_detection(predicted, expected):
    return grade_easy(predicted, expected)

def medium_classification(predicted, expected):
    return grade_medium(predicted, expected)

def hard_classification(predicted, expected):
    return grade_hard(predicted, expected)

TASKS = {
    "easy_spam_detection": easy_spam_detection,
    "medium_classification": medium_classification,
    "hard_classification": hard_classification,
}