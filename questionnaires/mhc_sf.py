"""
MHC-SF - Mental Health Continuum Short Form
שאלון רצף הבריאות הנפשית המקוצר
Lamers et al. (2011), Hebrew: Shrira et al. (2016)

14 items, Likert 1-6
Subscales: Emotional (1-3), Social (4-8), Psychological (9-14)
Scoring: Mean per subscale and total
"""

NAME = "שאלון רצף הבריאות הנפשית המקוצר (MHC-SF)"
CODE = "MHC-SF"

INSTRUCTIONS = """קרא את ההגדים הבאים וסמן עד כמה הרגשת בחודש האחרון את תחושות/תיאורים אלו."""

SCALE_LABELS = {
    1: "בכלל לא",
    2: "פעם או פעמיים בכל החודש",
    3: "פעם בשבוע",
    4: "פעמיים או שלוש בשבוע",
    5: "כמעט כל יום",
    6: "כל יום",
}

ITEMS = [
    {"number": 1, "text": "הרגשתי מסופק/ת מחיי"},
    {"number": 2, "text": "הרגשתי שמח/ה"},
    {"number": 3, "text": "הרגשתי עניין בחיים"},
    {"number": 4, "text": "הרגשתי שיש לי משהו חשוב לתרום לחברה"},
    {"number": 5, "text": "הרגשתי שייך/ת לקהילה בה אני חי/ה (לקבוצה חברתית, לשכונה שלי, לעיר שלי)"},
    {"number": 6, "text": "הרגשתי שהחברה בה אנו חיים הופכת למקום טוב יותר לאנשים"},
    {"number": 7, "text": "חשבתי שאנשים הם בבסיסם טובים"},
    {"number": 8, "text": "הדרך בה מתנהלת החברה שלנו נראתה הגיונית בעיניי"},
    {"number": 9, "text": "אהבתי את רוב הצדדים של אישיותי"},
    {"number": 10, "text": "הייתי טוב/ה בארגון כל המחויבויות של חיים היום יום"},
    {"number": 11, "text": "הרגשתי שיש לי קשרים חמים ומלאי אמון עם אחרים"},
    {"number": 12, "text": "הרגשתי שחוויתי חוויות שהביאו אותי לצמוח ולהפוך לאדם טוב יותר"},
    {"number": 13, "text": "הרגשתי בטוח/ה לחשוב ולהביע את רעיונותיי ודעותיי"},
    {"number": 14, "text": "הרגשתי שלחיי יש משמעות ומטרה"},
]

REVERSED_ITEMS = []

SUBSCALES = {
    "רווחה נפשית רגשית": [1, 2, 3],
    "רווחה נפשית חברתית": [4, 5, 6, 7, 8],
    "רווחה נפשית פסיכולוגית": [9, 10, 11, 12, 13, 14],
}


def score(responses):
    """
    Calculate MHC-SF scores.
    responses: dict mapping item number (int) -> raw score (int, 1-6)
    Returns dict with subscale means, total mean, and interpretation.
    """
    results = {"subscales": {}}

    all_scores = []
    for subscale_name, item_numbers in SUBSCALES.items():
        values = [responses[i] for i in item_numbers]
        mean = sum(values) / len(values)
        results["subscales"][subscale_name] = round(mean, 2)
        all_scores.extend(values)

    total_mean = sum(all_scores) / len(all_scores)
    results["total"] = round(total_mean, 2)

    if total_mean >= 5:
        results["interpretation"] = "רווחה נפשית גבוהה יחסית לכלל האוכלוסייה"
    elif total_mean >= 4:
        results["interpretation"] = "רווחה נפשית ממוצעת – רוב האנשים חווים תחושות רווחה בין פעם בשבוע לפעמיים-שלוש בשבוע"
    elif total_mean >= 3:
        results["interpretation"] = "רווחה נפשית מתחת לממוצע"
    else:
        results["interpretation"] = "רווחה נפשית נמוכה יחסית לכלל האוכלוסייה"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 1,
    "scale_max": 6,
    "score": score,
}
