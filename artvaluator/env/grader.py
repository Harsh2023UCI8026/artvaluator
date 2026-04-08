# env/grader.py

def grade_easy(platforms):
    return 1.0 if len(platforms) >= 2 else 0.5


def grade_medium(text):
    return min(1.0, len(text.split()) / 80)


def grade_hard(predicted, true):
    error = abs(predicted - true)
    return max(0, 1 - error / true)