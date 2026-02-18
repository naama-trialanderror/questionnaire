"""
PTGI - Post-Traumatic Growth Inventory
שאלון צמיחה פוסט-טראומטית
Tedeschi & Calhoun (1996), Hebrew: Laufer & Solomon (2006)

21 items, Likert 1-4
No reversed items
5 subscales: Relating to Others, New Possibilities, Personal Strength,
             Spiritual Change, Appreciation of Life
Scoring: Sum of all items (range 21-84)
Higher scores = more post-traumatic growth
"""

NAME = "שאלון צמיחה פוסט-טראומטית (PTGI)"
CODE = "PTGI"

INSTRUCTIONS = """לפניך שורה של דברים שלפעמים משתנים בחיי אנשים אחרי אירועים. אנא סמן לגבי כל אחד מההיגדים את המידה שבה התרחש שינוי כזה בחייך כתוצאה מהאירוע."""

SCALE_LABELS = {
    1: "לא חל שינוי",
    2: "חל שינוי במידה נמוכה",
    3: "חל שינוי במידה בינונית",
    4: "חל שינוי במידה רבה",
}

ITEMS = [
    {"number": 1, "text": "העדיפויות שלי בנוגע למה שחשוב בחיים"},
    {"number": 2, "text": "אני נוטה יותר לנסות דברים הדורשים שינוי"},
    {"number": 3, "text": "ערך החיים עלה בעיני"},
    {"number": 4, "text": "תחושה שאני סומך על עצמי"},
    {"number": 5, "text": "הבנה טובה יותר של עניינים רוחניים"},
    {"number": 6, "text": "הידיעה שאני יכול לסמוך על אנשים בשעת צרה"},
    {"number": 7, "text": "תחושת קרבה לאחרים"},
    {"number": 8, "text": "ידיעה שאני יכול להתגבר על קשיים"},
    {"number": 9, "text": "רצון להביע את תחושותיי"},
    {"number": 10, "text": "להיות מסוגל לקבל את הדברים כפי שהם"},
    {"number": 11, "text": "מעריך כל יום שאני חי"},
    {"number": 12, "text": "היכולת לחוש חמלה כלפי אחרים"},
    {"number": 13, "text": "אני מסוגל לעשות את חיי לטובים יותר"},
    {"number": 14, "text": "נפתחו הזדמנויות חדשות שלא הייתי מכיר בנסיבות אחרות"},
    {"number": 15, "text": "להשקיע ביחסים עם אחרים"},
    {"number": 16, "text": "אמונה דתית"},
    {"number": 17, "text": "גיליתי שאני חזק יותר ממה שחשבתי"},
    {"number": 18, "text": "למדתי הרבה על כמה אנשים הם נהדרים"},
    {"number": 19, "text": "פיתחתי תחומי התעניינות חדשים"},
    {"number": 20, "text": "אני מקבל את העובדה שאני זקוק לאחרים"},
    {"number": 21, "text": "פיתחתי דרך חדשה בחיי"},
]

REVERSED_ITEMS = []

SUBSCALES = {
    "יחסים עם אחרים": {"english": "Relating to Others", "items": [6, 7, 9, 12, 15, 18, 20]},
    "אפשרויות חדשות": {"english": "New Possibilities", "items": [2, 14, 17, 19, 21]},
    "חוזק אישי": {"english": "Personal Strength", "items": [4, 8, 10, 13]},
    "שינוי רוחני": {"english": "Spiritual Change", "items": [5, 16]},
    "הערכת החיים": {"english": "Appreciation of Life", "items": [1, 3, 11]},
}


def score(responses):
    """
    Calculate PTGI score.
    responses: dict mapping item number (int) -> raw score (int, 1-4)
    Returns dict with total sum, subscale means, and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "21-84",
        "subscales": {},
    }

    for subscale_name, subscale_info in SUBSCALES.items():
        items = subscale_info["items"]
        subscale_sum = sum(responses[i] for i in items)
        subscale_mean = round(subscale_sum / len(items), 2)
        results["subscales"][subscale_name] = {
            "english": subscale_info["english"],
            "mean": subscale_mean,
            "sum": subscale_sum,
            "max": len(items) * 4,
        }

    # Interpretation based on total score
    if total <= 35:
        results["interpretation"] = "רמה נמוכה של צמיחה פוסט-טראומטית"
    elif total <= 52:
        results["interpretation"] = "רמה נמוכה-בינונית של צמיחה פוסט-טראומטית"
    elif total <= 68:
        results["interpretation"] = "רמה בינונית-גבוהה של צמיחה פוסט-טראומטית"
    else:
        results["interpretation"] = "רמה גבוהה של צמיחה פוסט-טראומטית"

    results["note"] = "שאלון זה מודד שינויים חיוביים בעקבות אירוע טראומטי. אין סף קליני – ציון גבוה יותר מעיד על צמיחה רבה יותר"

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
