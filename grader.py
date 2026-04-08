def grade_easy(predicted, expected):
    return 0.8 if predicted == expected else 0.2

def grade_medium(predicted, expected):
    return 0.85 if predicted == expected else 0.3

def grade_hard(predicted, expected):
    return 0.9 if predicted == expected else 0.4