"""
LEC-5 - Life Events Checklist for DSM-5
סקר מאורעות חיים מלחיצים
Weathers et al. (2013), Hebrew: Ben-Ezra et al. (2018)

16 life events + open-ended item.
Each event: respondent marks date of occurrence.
This is an inventory — no scoring, just event recording.
"""

NAME = "סקר מאורעות חיים מלחיצים (LEC-5)"
CODE = "LEC-5"

INSTRUCTIONS = """השאלות הבאות מתארות רשימה של אירועי חיים מלחיצים.
סמן/י בבקשה את האירועים אשר התרחשו בחייך בשנה-שנתיים האחרונות ומעיקים עליך עד היום, או שהעיקו עליך בחצי השנה האחרונה."""

SCALE_LABELS = {
    0: "לא",
    1: "כן",
}

ITEMS = [
    {"number": 1, "text": "גירושין/פרידה"},
    {"number": 2, "text": "סכסוכים משפחתיים"},
    {"number": 3, "text": "סכסוכים במקום העבודה"},
    {"number": 4, "text": "סכסוכים עם שכנים"},
    {"number": 5, "text": "מחלה של אדם אהוב"},
    {"number": 6, "text": "מוות של אדם אהוב"},
    {"number": 7, "text": "הסתגלות כתוצאה מפרישה מעבודה"},
    {"number": 8, "text": "אבטלה"},
    {"number": 9, "text": "עבודה רבה / מועטה מידי"},
    {"number": 10, "text": "לחץ לעמוד בתאריכי יעד / לחץ של זמן"},
    {"number": 11, "text": "מעבר דירה"},
    {"number": 12, "text": "בעיות כלכליות"},
    {"number": 13, "text": "מחלה חמורה שלך"},
    {"number": 14, "text": "תאונה רצינית"},
    {"number": 15, "text": "תקיפה"},
    {"number": 16, "text": "ויתור על תחביב שחשוב לך"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    LEC-5 is an inventory — no clinical scoring.
    responses: dict mapping item number (int) -> 0 (No) or 1 (Yes)
    Returns dict with count of endorsed events and list of endorsed events.
    """
    endorsed = [n for n, v in responses.items() if v == 1]
    total_endorsed = len(endorsed)

    endorsed_texts = []
    for item in ITEMS:
        if item["number"] in endorsed:
            endorsed_texts.append(item["text"])

    results = {
        "total_endorsed": total_endorsed,
        "endorsed_events": endorsed_texts,
        "score_range": "0-16 (מספר אירועים שדווחו)",
        "interpretation": f"דווח על {total_endorsed} אירועי חיים מלחיצים",
    }

    if total_endorsed == 0:
        results["severity"] = "ללא"
        results["interpretation"] = "לא דווח על אירועי חיים מלחיצים"
    elif total_endorsed <= 3:
        results["severity"] = "מעט"
        results["interpretation"] = f"דווח על {total_endorsed} אירועי חיים מלחיצים"
    elif total_endorsed <= 6:
        results["severity"] = "בינוני"
        results["interpretation"] = f"דווח על {total_endorsed} אירועי חיים מלחיצים – עומס אירועים בינוני"
    else:
        results["severity"] = "רב"
        results["interpretation"] = f"דווח על {total_endorsed} אירועי חיים מלחיצים – עומס אירועים משמעותי"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 0,
    "scale_max": 1,
    "score": score,
}
