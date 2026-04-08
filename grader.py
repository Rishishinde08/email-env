def grade(predicted, expected):
    if predicted == expected:
        return 0.9
    elif predicted in ["spam", "urgent", "normal"]:
        return 0.5
    return 0.1