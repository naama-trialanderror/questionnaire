"""
GAD-7 - Generalized Anxiety Disorder 7-Item Scale
שאלון לאבחון חרדה כללית – 7 פריטים
Robert et al. (2007)

7 items, Likert 0-3
No reversed items
Scoring: Sum of all items (range 0-21)
"""

NAME = "שאלון לאבחון חרדה כללית (GAD-7)"
CODE = "GAD-7"

INSTRUCTIONS = """במהלך השבועיים האחרונים, באיזו תדירות היית מוטרד מכל אחת מהבעיות הבאות:"""

SCALE_LABELS = {
    0: "כלל לא",
    1: "כמה ימים",
    2: "יותר ממחצית הימים",
    3: "כמעט כל יום",
}

ITEMS = [
    {"number": 1, "text": "הרגשתי עצבני, חרד או מתוח מאוד"},
    {"number": 2, "text": "לא הייתי מסוגל להפסיק לדאוג או לשלוט בדאגה"},
    {"number": 3, "text": "הייתי מודאג יותר מדי בנוגע לדברים שונים"},
    {"number": 4, "text": "התקשיתי להירגע"},
    {"number": 5, "text": "הייתי כל כך חסר מנוחה שהיה לי קשה לשבת מבלי לנוע"},
    {"number": 6, "text": "הייתי מתעצבן או מתרגז בקלות"},
    {"number": 7, "text": "פחדתי כאילו משהו נורא עלול לקרות"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    Calculate GAD-7 score.
    responses: dict mapping item number (int) -> raw score (int, 0-3)
    Returns dict with total sum and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "0-21",
    }

    if total < 10:
        results["interpretation"] = "רמת חרדה מתחת לסף הקליני"
        results["severity"] = "מתחת לסף"
    elif total <= 14:
        results["interpretation"] = "דגל צהוב: סיכון להפרעת חרדה כללית (ציון ≥10)"
        results["severity"] = "בינוני"
    else:
        results["interpretation"] = "דגל אדום: סיכון גבוה להפרעת חרדה כללית (ציון ≥15)"
        results["severity"] = "חמור"

    if total >= 10:
        results["clinical_note"] = "ציון גבוה יכול לשקף גם הפרעות חרדה נוספות כגון הפרעת פניקה, חרדה חברתית או PTSD. יש חשיבות לראיון מלא של ההפרעה"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 0,
    "scale_max": 3,
    "score": score,
}
