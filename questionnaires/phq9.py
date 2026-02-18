"""
PHQ-9 - Patient Health Questionnaire-9
שאלון בריאות המטופל – 9
Kroenke et al. (2001)

9 items, Likert 0-3
No reversed items
Scoring: Sum of all items (range 0-27)
Plus functional impairment question (not scored)
"""

NAME = "שאלון בריאות המטופל (PHQ-9)"
CODE = "PHQ-9"

INSTRUCTIONS = """במהלך השבועיים האחרונים, באיזו תדירות היית מוטרד מכל אחת מהבעיות הבאות:"""

SCALE_LABELS = {
    0: "כלל לא",
    1: "מספר ימים",
    2: "יותר ממחצית הימים",
    3: "כמעט כל יום",
}

ITEMS = [
    {"number": 1, "text": "עניין או הנאה מועטים מעשיית דברים"},
    {"number": 2, "text": "תחושת דכדוך, דיכאון או חוסר תקווה"},
    {"number": 3, "text": "קשיים בהירדמות, או בשינה רציפה, או עודף שינה"},
    {"number": 4, "text": "תחושה של עייפות או אנרגיה מועטה"},
    {"number": 5, "text": "תיאבון מועט או אכילת יתר"},
    {"number": 6, "text": "מרגיש רע לגבי עצמך – מרגיש שאתה כישלון או שאכזבת את עצמך או את משפחתך"},
    {"number": 7, "text": "קושי להתרכז בדברים, כמו קריאה בעיתון או צפיה בטלוויזיה"},
    {"number": 8, "text": "היית מדבר או נע באיטיות עד כדי כך שאחרים הבחינו בכך, או להפך היית חסר שקט ומנוחה כך שהיית צריך להסתובב יותר מהרגיל"},
    {"number": 9, "text": "מחשבות שהיה עדיף לו היית מת או מחשבות על פגיעה בעצמך בדרך כל שהיא"},
]

REVERSED_ITEMS = []

# Functional impairment question (displayed but not part of scored total)
FUNCTIONAL_IMPAIRMENT_QUESTION = "אם סימנת בעיות כלשהן, אנא סמן עד כמה בעיות אלו הקשו עליך לבצע את עבודתך, לטפל בדברים בבית או להסתדר עם אנשים אחרים?"
FUNCTIONAL_IMPAIRMENT_OPTIONS = {
    0: "לא הקשו כלל",
    1: "הקשו במידת מה",
    2: "הקשו מאוד",
    3: "הקשו באופן קיצוני",
}


def score(responses):
    """
    Calculate PHQ-9 score.
    responses: dict mapping item number (int) -> raw score (int, 0-3)
    Returns dict with total sum and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "0-27",
    }

    if total <= 4:
        results["interpretation"] = "היעדר דיכאון"
        results["severity"] = "ללא"
    elif total <= 9:
        results["interpretation"] = "דיכאון ברמה תת-סיפית/נמוכה"
        results["severity"] = "נמוך"
    elif total <= 14:
        results["interpretation"] = "רמת דיכאון בינוני"
        results["severity"] = "בינוני"
    elif total <= 19:
        results["interpretation"] = "דיכאון בינוני-חמור"
        results["severity"] = "בינוני-חמור"
    else:
        results["interpretation"] = "דיכאון חמור"
        results["severity"] = "חמור"

    # Check for suicidality flag (item 9)
    if 9 in responses and responses[9] > 0:
        results["clinical_note"] = "שימו לב: פריט 9 (מחשבות על מוות/פגיעה עצמית) סומן כחיובי – יש לבחון נושא זה בראיון קליני"

    # Check DSM criterion: 5+ symptoms at "more than half the days" (>=2), with item 1 or 2 included
    symptoms_present = sum(1 for item_num, val in responses.items() if val >= 2)
    anhedonia_or_depression = (responses.get(1, 0) >= 2) or (responses.get(2, 0) >= 2)
    if symptoms_present >= 5 and anhedonia_or_depression:
        results["dsm_screening"] = "מסנן חיובי: 5 תסמינים או יותר סומנו כקיימים לפחות 'יותר ממחצית הזמן', כולל אנהדוניה ו/או מצב רוח דיכאוני – מומלץ ראיון קליני מלא"

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
