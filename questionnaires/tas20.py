"""
TAS-20 - Toronto Alexithymia Scale
סולם אלקסיתימיה טורונטו
Bagby, Parker & Taylor (1994)

20 items, Likert 1-5
Reversed items: 4, 5, 10, 18, 19 (score = 6 - raw)
Scoring: Sum of all items (range 20-100)
Cutoff >= 61 suggests alexithymia
Subscales: DIF, DDF, EOT
"""

NAME = "סולם אלקסיתימיה טורונטו (TAS-20)"
CODE = "TAS20"

INSTRUCTIONS = """לפניך מספר הצהרות. אנא ציין/י עד כמה את/ה מסכימים או לא מסכימים לכל אחת מההצהרות."""

SCALE_LABELS = {
    1: "מאוד לא מסכים/ה",
    2: "לא מסכים/ה במקצת",
    3: "לא מסכים/ה ולא מתנגד/ת",
    4: "מסכים/ה במקצת",
    5: "מסכים/ה מאוד",
}

ITEMS = [
    {"number": 1, "text": "לעיתים קרובות אני מרגיש/ה מבולבל/ת לגבי איזה רגש אני מרגיש/ה"},
    {"number": 2, "text": "קשה לי למצוא את המילים המתאימות לבטא את מה שאני מרגיש/ה"},
    {"number": 3, "text": "יש לי תחושות גופניות שאפילו רופאים אינם מבינים"},
    {"number": 4, "text": "קל לי לתאר בקלות את רגשותיי"},
    {"number": 5, "text": "אני מעדיף/ה לנתח הבעיות שלי מאשר רק לתאר אותן"},
    {"number": 6, "text": "כשאני במצב רוח רע אינני יודע/ת עם זה עצב, פחד או כעס"},
    {"number": 7, "text": "לעתים קרובות אני מבולבל/ת מתחושותיי הגופניות"},
    {"number": 8, "text": "אני מעדיף/ה לתת לאירועים לקרות מאשר לנסות להבין מדוע הם קרו"},
    {"number": 9, "text": "יש לי רגשות שקשה לי לזהות"},
    {"number": 10, "text": "חיוני להיות במגע עם הרגשות"},
    {"number": 11, "text": "קשה לי לתאר איך אני מרגיש/ה כלפי אנשים"},
    {"number": 12, "text": "אנשים מבקשים ממני לתאר יותר את רגשותיי"},
    {"number": 13, "text": "אינני יודע/ת מה מתרחש בתוכי"},
    {"number": 14, "text": "לעיתים קרובות אינני יודע/ת מדוע אני כועס/ת"},
    {"number": 15, "text": "אני מעדיף/ה לדבר עם אנשים על אירועי היום יום מאשר על רגשותיהם"},
    {"number": 16, "text": "אני מעדיף/ה לצפות בבידור קל על פני דרמות פסיכולוגיות"},
    {"number": 17, "text": "קשה לי לחלוק רגשות עמוקים אפילו עם חברים קרובים"},
    {"number": 18, "text": "אני יכול/ה להרגיש קרוב/ה למישהו אפילו ברגעי שתיקה"},
    {"number": 19, "text": "אני מוצא/ת שלבחון את רגשותיי מועיל בפתרון בעיות אישיות"},
    {"number": 20, "text": "חיפוש אחר משמעות נסתרת בסרטים או בהצגות מקלקל מההנאה"},
]

REVERSED_ITEMS = [4, 5, 10, 18, 19]

# Subscale definitions
SUBSCALES = {
    "DIF": {"name": "קושי לזהות רגשות", "items": [1, 3, 6, 7, 9, 13, 14]},
    "DDF": {"name": "קושי לתאר רגשות", "items": [2, 4, 11, 12, 17]},
    "EOT": {"name": "נטייה למיקוד קשב חיצוני", "items": [5, 8, 10, 15, 16, 18, 19, 20]},
}


def score(responses):
    """
    Calculate TAS-20 score.
    responses: dict mapping item number (int) -> raw score (int, 1-5)
    Returns dict with total sum, subscale sums, and interpretation.
    """
    # Apply reversals
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 6 - raw
        else:
            scored[item_num] = raw

    # Total score
    total = sum(scored.values())

    results = {
        "total_score": total,
        "score_range": "סכום 20-100",
    }

    # Subscale scores
    for code, info in SUBSCALES.items():
        sub_items = info["items"]
        sub_score = sum(scored.get(i, 0) for i in sub_items)
        results[f"subscale_{code}"] = sub_score
        results[f"subscale_{code}_name"] = info["name"]

    # Interpretation
    if total >= 61:
        results["severity"] = "חשד לאלקסיתימיה"
        results["interpretation"] = f"ציון כולל {total} (≥61) – חשד לאלקסיתימיה. מומלץ להעמיק בהערכה קלינית"
    elif total >= 52:
        results["severity"] = "אזור ביניים"
        results["interpretation"] = f"ציון כולל {total} (52-60) – אזור ביניים. יש לשקול הערכה נוספת"
    else:
        results["severity"] = "תקין"
        results["interpretation"] = f"ציון כולל {total} (<52) – טווח תקין"

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
