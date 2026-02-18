"""
OCI-R - Obsessive-Compulsive Inventory - Revised
שאלון אובססיביות-קומפולסיביות מתוקן
Foa et al. (2002)

18 items, Likert 0-4
No reversed items
6 subscales (3 items each): Washing, Checking, Ordering, Obsessing, Hoarding, Neutralising
Scoring: Sum of all items (range 0-72), cutoff >= 21 suggests OCD
"""

NAME = "שאלון אובססיביות-קומפולסיביות מתוקן (OCI-R)"
CODE = "OCI-R"

INSTRUCTIONS = """האמירות הבאות מתייחסות לחוויות שיש לאנשים רבים בחייהם היומיומיים. ציין עד כמה כל אחת מהחוויות הללו גרמה לך סבל או הטרידה אותך במשך החודש האחרון."""

SCALE_LABELS = {
    0: "בכלל לא",
    1: "במידה מעטה",
    2: "במידת מה",
    3: "במידה רבה",
    4: "באופן קיצוני",
}

ITEMS = [
    {"number": 1, "text": "אגרתי כל כך הרבה דברים שהם מפריעים לי", "subscale": "Hoarding"},
    {"number": 2, "text": "לעיתים קרובות אני בודק דברים יותר ממה שנחוץ", "subscale": "Checking"},
    {"number": 3, "text": "אני נעשה מוטרד או מתרגז כאשר דברים אינם מסודרים כיאות", "subscale": "Ordering"},
    {"number": 4, "text": "אני חש צורך לספור כאשר אני עושה דברים מסוימים", "subscale": "Neutralising"},
    {"number": 5, "text": "קשה לי לגעת במשהו כאשר אני יודע שנגעו בו זרים או אנשים מסוימים", "subscale": "Washing"},
    {"number": 6, "text": "אני מתקשה לשלוט במחשבות שלי", "subscale": "Obsessing"},
    {"number": 7, "text": "אני אוסף דברים שאין לי צורך בהם", "subscale": "Hoarding"},
    {"number": 8, "text": "אני בודק שוב ושוב דלתות, חלונות, מגירות וכו'", "subscale": "Checking"},
    {"number": 9, "text": "אני נהיה מוטרד או עצבני אם משנים את הצורה בה סידרתי דברים", "subscale": "Ordering"},
    {"number": 10, "text": "אני חש צורך לחזור על מספרים מסוימים", "subscale": "Neutralising"},
    {"number": 11, "text": "לפעמים אני חייב לשטוף או לנקות את עצמי רק בגלל שאני חש מזוהם", "subscale": "Washing"},
    {"number": 12, "text": "אני מוטרד על ידי מחשבות בלתי נעימות שבאות בניגוד לרצוני", "subscale": "Obsessing"},
    {"number": 13, "text": "אני נמנע מלזרוק דברים כיוון שאני חושש שאזדקק להם בהמשך", "subscale": "Hoarding"},
    {"number": 14, "text": "אני בודק ברזי גז ומים שוב ושוב ומדליק אורות לאחר שכיביתי אותם", "subscale": "Checking"},
    {"number": 15, "text": "אני צריך שדברים יהיו מסודרים בסדר מסוים", "subscale": "Ordering"},
    {"number": 16, "text": "אני מרגיש שישנם מספרים טובים ומספרים רעים", "subscale": "Neutralising"},
    {"number": 17, "text": "אני שוטף את ידי לעיתים תכופות ובאופן ממושך יותר מהנחוץ", "subscale": "Washing"},
    {"number": 18, "text": "אני חווה לעיתים קרובות מחשבות בלתי נעימות ויש לי קושי להיפטר מהן", "subscale": "Obsessing"},
]

REVERSED_ITEMS = []

SUBSCALES = {
    "רחצה (Washing)": [5, 11, 17],
    "בדיקה (Checking)": [2, 8, 14],
    "סדר (Ordering)": [3, 9, 15],
    "אובססיות (Obsessing)": [6, 12, 18],
    "אגירה (Hoarding)": [1, 7, 13],
    "ניטרול (Neutralising)": [4, 10, 16],
}


def score(responses):
    """
    Calculate OCI-R score.
    responses: dict mapping item number (int) -> raw score (int, 0-4)
    Returns dict with total, subscale scores, severity, and interpretation.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "0-72",
        "subscales": {},
    }

    for subscale_name, item_numbers in SUBSCALES.items():
        subscale_score = sum(responses.get(i, 0) for i in item_numbers)
        results["subscales"][subscale_name] = {
            "score": subscale_score,
            "max": 12,
        }

    if total >= 21:
        results["severity"] = "מעל סף קליני"
        results["interpretation"] = (
            "ציון כולל מעל סף קליני (≥21): מרמז על הפרעה טורדנית-כפייתית (OCD). "
            "מומלץ להפנות לאבחון קליני מעמיק"
        )
    elif total >= 14:
        results["severity"] = "בינוני"
        results["interpretation"] = "ציון בינוני: נוכחות מסוימת של תסמינים אובססיביים-קומפולסיביים, מתחת לסף הקליני"
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = "ציון נמוך: רמה נמוכה של תסמינים אובססיביים-קומפולסיביים"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 0,
    "scale_max": 4,
    "score": score,
}
