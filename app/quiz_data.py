

QUIZ_QUESTIONS = {
    1: [
        {
            "id": 1,
            "text": "Vaginal bleeding?",
            "options": [
                {"label": "No", "value": 0},
                {"label": "Heavy", "value": 3}
            ]
        },
        {
            "id": 2,
            "text": "Severe abdominal pain?",
            "options": [
                {"label": "No", "value": 0},
                {"label": "Severe", "value": 3}
            ]
        },
        # Add more trimester 1 questions here
    ],
    2: [
        # Questions for trimester 2
    ],
    3: [
        # Questions for trimester 3
    ]
}

def calculate_risk(trimester: int, answers: dict) -> int:
    """
    Calculate risk score based on trimester and answers.

    :param trimester: trimester number (1, 2, or 3)
    :param answers: dict mapping question id to selected option value
    :return: total risk score
    """
    questions = QUIZ_QUESTIONS.get(trimester, [])
    total_score = 0
    for q in questions:
        qid = q["id"]
        val = answers.get(str(qid)) or answers.get(qid)
        if val is not None:
            total_score += int(val)
    return total_score
