"""
ADNM-4 - Adjustment Disorder New Module 4 (Ultra Brief)
שאלון הפרעת הסתגלות מקוצר
Ben-Ezra et al. (2018)

4 items, Likert 1-4
No reversed items
Scoring: Sum of all items (range 4-16)
Cutoff >= 9 suggests adjustment disorder (ICD-11 criteria)
"""

NAME = "שאלון הפרעת הסתגלות מקוצר (ADNM-4)"
CODE = "ADNM-4"

INSTRUCTIONS = """חשוב/י בבקשה על האירוע המלחיץ ביותר שחווית במהלך השנה האחרונה וענה/י על השאלות הבאות באופן הכנה ביותר שאת/ה יכול/ה."""

SCALE_LABELS = {
    1: "אף פעם",
    2: "לעיתים רחוקות",
    3: "לפעמים",
    4: "לעיתים קרובות",
}

ITEMS = [
    {"number": 1, "text": "האירוע המלחיץ מעסיק מאוד את מחשבותיי והדבר מעיק עליי מאוד"},
    {"number": 2, "text": "מאז האירוע המלחיץ, אני מתקשה להתרכז בדברים מסוימים"},
    {"number": 3, "text": "אני נזכר/ת כל הזמן באירוע המלחיץ ואינני יכול/ה לעשות דבר כדי לעצור זאת"},
    {"number": 4, "text": "בעקבות המאורע המלחיץ, אין לי חשק ללכת לעבודה או לבצע את הפעולות הנחוצות בחיי היומיום"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    Calculate ADNM-4 score.
    responses: dict mapping item number (int) -> raw score (int, 1-4)
    Returns dict with total sum, severity, and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "4-16",
    }

    if total < 9:
        results["severity"] = "מתחת לסף"
        results["interpretation"] = "רמת הסתגלות מתחת לסף הקליני (ציון < 9)"
    else:
        results["severity"] = "סיכון קליני"
        results["interpretation"] = "דגל אדום: ציון מעל סף קליני להפרעת הסתגלות (ציון ≥ 9, קריטריוני ICD-11)"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 1,
    "scale_max": 4,
    "score": score,
}
