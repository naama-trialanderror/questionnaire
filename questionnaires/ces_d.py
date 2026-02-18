"""
CES-D - Center for Epidemiologic Studies Depression Scale
שאלון להערכת דיכאון
Radloff (1977), Hebrew: Shmotkin & Keinan (2011)

20 items, Likert 0-3
Items 4, 8, 12, 16 are REVERSED (score = 3 - raw)
Scoring: Sum of all items (range 0-60)
"""

NAME = "שאלון להערכת דיכאון (CES-D)"
CODE = "CES-D"

INSTRUCTIONS = """קרא בבקשה את המשפטים הבאים וסמן בסולם 0-3 בדרך הטובה ביותר עד כמה הרגשת או התנהגת כפי שמתואר להלן בכל משפט במשך השבוע האחרון."""

SCALE_LABELS = {
    0: "לעיתים רחוקות או אף לא בשום זמן (פחות מיום אחד)",
    1: "בחלק או בחלק קטן של הזמן (1-2 ימים)",
    2: "לעיתים או לעיתים די קרובות של הזמן (3-4 ימים)",
    3: "רוב או כל הזמן (5-7 ימים)",
}

ITEMS = [
    {"number": 1, "text": "הייתי מוטרד/ת מדברים שבדרך כלל לא מטרידים אותי"},
    {"number": 2, "text": "לא התחשק לי לאכול, היה לי מעט תיאבון"},
    {"number": 3, "text": "הרגשתי שאני לא יכול/ה לצאת מן העצבות, אפילו בעזרת משפחתי או חבריי"},
    {"number": 4, "text": "הרגשתי שאני טוב/ה כמו אנשים אחרים"},
    {"number": 5, "text": "היה לי קשה להתרכז במה שעשיתי"},
    {"number": 6, "text": "הרגשתי מדוכא/ת"},
    {"number": 7, "text": "הרגשתי שכל דבר שעשיתי היה מאמץ"},
    {"number": 8, "text": "הרגשתי מלא/ת תקווה לגבי העתיד"},
    {"number": 9, "text": "חשבתי שחיי היו כישלון"},
    {"number": 10, "text": "הרגשתי מפוחד/ת"},
    {"number": 11, "text": "השינה שלי היתה חסרת מנוחה"},
    {"number": 12, "text": "הייתי מאושר/ת"},
    {"number": 13, "text": "דיברתי פחות מהרגיל"},
    {"number": 14, "text": "הרגשתי בודד/ה"},
    {"number": 15, "text": "אנשים היו לא ידידותיים"},
    {"number": 16, "text": "נהניתי מהחיים"},
    {"number": 17, "text": "היו לי רגעי בכי"},
    {"number": 18, "text": "הרגשתי עצוב/ה"},
    {"number": 19, "text": "הרגשתי שאנשים לא מחבבים אותי"},
    {"number": 20, "text": "לא יכולתי להפעיל את עצמי"},
]

REVERSED_ITEMS = [4, 8, 12, 16]


def score(responses):
    """
    Calculate CES-D score.
    responses: dict mapping item number (int) -> raw score (int, 0-3)
    Returns dict with total sum and interpretation.
    """
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 3 - raw
        else:
            scored[item_num] = raw

    total = sum(scored.values())
    results = {
        "total": total,
        "score_range": "0-60",
    }

    if total <= 10:
        results["interpretation"] = "תסמיני דיכאון נמוכים"
        results["severity"] = "נמוך"
    elif total <= 16:
        results["interpretation"] = "תסמיני דיכאון מתונים"
        results["severity"] = "מתון"
    elif total <= 19:
        results["interpretation"] = "תסמיני דיכאון ברמה גבוהה (ציון חתך: 17+)"
        results["severity"] = "גבוה"
    else:
        results["interpretation"] = "תסמיני דיכאון ברמה גבוהה (ציון חתך מחמיר: 20+)"
        results["severity"] = "גבוה מאוד"

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
