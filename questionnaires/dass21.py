"""
DASS-21 - Depression Anxiety Stress Scales (Short Form)
שאלון מקוצר להערכת דיכאון, חרדה ולחץ
Lovibond & Lovibond (1995), Hebrew: Janine Lurie

21 items, Likert 0-3
3 subscales: Depression, Anxiety, Stress (7 items each)
Scoring: Sum per subscale
"""

NAME = "שאלון מקוצר להערכת דיכאון, חרדה ולחץ (DASS-21)"
CODE = "DASS-21"

INSTRUCTIONS = """קרא בבקשה כל אמירה וסמן בעיגול מספר 0, 1, 2 או 3 המציין עד כמה האמירה מתארת את מצבך במהלך השבוע האחרון. אין תשובה נכונה או שגויה. אין צורך להתעכב על כל אמירה יתר על המידה."""

SCALE_LABELS = {
    0: "האמירה לא מתארת את מצבי כלל",
    1: "האמירה מתארת את מצבי באופן חלקי, או בחלק מהזמן",
    2: "האמירה מתארת את מצבי באופן ניכר, או בחלק ניכר מהזמן",
    3: "האמירה מתארת את מצבי מאוד, או ברוב הזמן",
}

ITEMS = [
    {"number": 1, "text": "התקשיתי להיות נינוח"},
    {"number": 2, "text": "חשתי ביובש בפה"},
    {"number": 3, "text": "התקשיתי לחוות כל הרגשה חיובית"},
    {"number": 4, "text": "חשתי קושי בנשימה (לדוגמא, נשימה מואצת במיוחד, חוסר אוויר בהעדר פעילות גופנית מאומצת)"},
    {"number": 5, "text": "לא היו לי הכוחות לעשות דברים"},
    {"number": 6, "text": "נטיתי להגזים בתגובותיי למצבים מסוימים"},
    {"number": 7, "text": "חשתי רעד (למשל, בידיים)"},
    {"number": 8, "text": "הרגשתי שאני מתעצבן יותר מדי"},
    {"number": 9, "text": "חששתי ממצבים בהם אולי אכנס לחרדה ואעשה צחוק מעצמי"},
    {"number": 10, "text": "הרגשתי שאין לי למה לצפות בחיים"},
    {"number": 11, "text": "הרגשתי שאני קצר רוח"},
    {"number": 12, "text": "התקשיתי להירגע"},
    {"number": 13, "text": "חוויתי דכדוך ותחושות עצבות"},
    {"number": 14, "text": "הייתי חסר סובלנות כלפי כל דבר שהפריע לי במעשיי"},
    {"number": 15, "text": "הרגשתי שאני קרוב למצב של פאניקה"},
    {"number": 16, "text": "לא הצלחתי להתלהב משום דבר"},
    {"number": 17, "text": "הערכתי העצמית כאדם הייתה מאוד נמוכה"},
    {"number": 18, "text": "הרגשתי רגיש ופגיע למדי"},
    {"number": 19, "text": "חשתי בפעילות ליבי גם ללא פעילות גופנית (לדוגמה, הרגשת עלייה בקצב הלב, החסרת פעימת לב)"},
    {"number": 20, "text": "הייתי מפוחד גם ללא סיבה מיוחדת"},
    {"number": 21, "text": "הרגשתי שהחיים חסרי משמעות"},
]

REVERSED_ITEMS = []

SUBSCALES = {
    "דיכאון": [3, 5, 10, 13, 16, 17, 21],
    "חרדה": [2, 4, 7, 9, 15, 19, 20],
    "לחץ": [1, 6, 8, 11, 12, 14, 18],
}

# Severity cutoffs per subscale (based on Henry & Crawford, 2005)
SEVERITY_CUTOFFS = {
    "דיכאון": [
        (0, 4, "תקין"),
        (5, 6, "קל"),
        (7, 10, "בינוני"),
        (11, 13, "חמור"),
        (14, 21, "חמור ביותר"),
    ],
    "חרדה": [
        (0, 3, "תקין"),
        (4, 5, "קל"),
        (6, 7, "בינוני"),
        (8, 9, "חמור"),
        (10, 21, "חמור ביותר"),
    ],
    "לחץ": [
        (0, 7, "תקין"),
        (8, 9, "קל"),
        (10, 12, "בינוני"),
        (13, 16, "חמור"),
        (17, 21, "חמור ביותר"),
    ],
}


def _get_severity(subscale_name, subscale_sum):
    for low, high, label in SEVERITY_CUTOFFS[subscale_name]:
        if low <= subscale_sum <= high:
            return label
    return "לא ידוע"


def score(responses):
    """
    Calculate DASS-21 scores.
    responses: dict mapping item number (int) -> raw score (int, 0-3)
    Returns dict with subscale sums, severity levels, total, and interpretation.
    """
    results = {"subscales": {}}

    total = 0
    for subscale_name, item_numbers in SUBSCALES.items():
        subscale_sum = sum(responses[i] for i in item_numbers)
        severity = _get_severity(subscale_name, subscale_sum)
        results["subscales"][subscale_name] = {
            "score": subscale_sum,
            "max": 21,
            "severity": severity,
        }
        total += subscale_sum

    results["total"] = total
    results["total_max"] = 63

    severity_levels = [s["severity"] for s in results["subscales"].values()]
    if any(s in ("חמור", "חמור ביותר") for s in severity_levels):
        results["interpretation"] = "נמצאה רמה גבוהה של מצוקה באחד או יותר מתחומי השאלון"
    elif any(s == "בינוני" for s in severity_levels):
        results["interpretation"] = "נמצאה רמה בינונית של מצוקה באחד או יותר מתחומי השאלון"
    elif any(s == "קל" for s in severity_levels):
        results["interpretation"] = "נמצאה רמה קלה של מצוקה באחד או יותר מתחומי השאלון"
    else:
        results["interpretation"] = "הציונים בכל תחומי השאלון נמצאים בטווח התקין"

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
