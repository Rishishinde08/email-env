def grade_easy(predicted, expected):
    if predicted == expected:
        return 0.8
    return 0.2

def grade_medium(predicted, expected):
    if predicted == expected:
        return 0.85
    return 0.3

def grade_hard(predicted, expected):
    if predicted == expected:
        return 0.9
    return 0.4