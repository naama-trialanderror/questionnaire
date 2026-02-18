"""
STO - Subjective Traumatic Outlook
שאלון תפיסה סובייקטיבית של הטראומה
Palgi et al. (2017; 2018)

5 items, Likert 1-5
No reversed items
Scoring: Sum of all items (range 5-25)
Cutoff >= 14 suggests high probability of PTSD (PCL-5 based)
Cutoff >= 13 suggests PTSD per ICD-11 criteria
"""

NAME = "שאלון תפיסה סובייקטיבית של הטראומה (STO)"
CODE = "STO"

INSTRUCTIONS = """השאלות שלפניך מתארות תחושות ומחשבות שאנשים חשים לפעמים כאשר הם מסתכלים לאחור על אירוע קשה/טראומטי שעברו. אנא ציין/י באיזו מידה משפטים אלו מתארים בצורה טובה את האופן בו את/ה תופס/ת את מצבך כיום בהקשר לאירוע הקשה ביותר שעברת."""

SCALE_LABELS = {
    1: "כלל לא",
    2: "במידה מועטה",
    3: "במידה בינונית",
    4: "במידה רבה",
    5: "במידה רבה מאוד",
}

ITEMS = [
    {"number": 1, "text": "האם בהסתכלות על מצבך את/ה חש/ה שאת/ה סובל/ת מטראומה נפשית?"},
    {"number": 2, "text": "האם בהסתכלות לאחור את/ה יכול/ה לראות קו שבר העובר בין החיים לפני האירוע הטראומטי והחיים אחריו?"},
    {"number": 3, "text": "האם את/ה חש/ה כי האירוע הטראומטי שולט בחייך?"},
    {"number": 4, "text": "האם במקביל לתפקוד היום יומי שלך, קיים אצלך עולם פנימי פגוע שלא יחלים לעולם מהטראומה?"},
    {"number": 5, "text": "האם את/ה חש/ה, כי אף אחד לא יכול להבין באמת מה את/ה עובר/ת מאז הטראומה?"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    Calculate STO score.
    responses: dict mapping item number (int) -> raw score (int, 1-5)
    Returns dict with total sum and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "5-25",
    }

    if total >= 14:
        results["severity"] = "גבוה"
        results["interpretation"] = (
            "ציון מעל סף קליני (≥14): הסתברות גבוהה ל-PTSD על בסיס PCL-5. "
            "ציון זה גם עולה על סף ה-ICD-11 (≥13) לאבחנת PTSD (Palgi et al., 2017; 2018)"
        )
    elif total >= 13:
        results["severity"] = "בינוני-גבוה"
        results["interpretation"] = (
            "ציון מעל סף קליני (≥13): מרמז על PTSD על פי קריטריונים של ICD-11 "
            "(Palgi et al., 2017; 2018)"
        )
    elif total >= 9:
        results["severity"] = "בינוני"
        results["interpretation"] = "תפיסה סובייקטיבית בינונית של טראומה, מתחת לסף הקליני"
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = "תפיסה סובייקטיבית נמוכה של טראומה"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 1,
    "scale_max": 5,
    "score": score,
}
