"""
PCL-5 - PTSD Checklist for DSM-5
רשימת מאפיינים להפרעת דחק פוסט-טראומטית
Weathers et al. (2013)

20 items, Likert 0-4
No reversed items
4 clusters: B (1-5), C (6-7), D (8-14), E (15-20)
Scoring: Sum of all items (range 0-80)
Cutoff >= 33 suggests PTSD
"""

NAME = "רשימת מאפיינים להפרעת דחק פוסט-טראומטית (PCL-5)"
CODE = "PCL-5"

INSTRUCTIONS = """להלן רשימה של בעיות ותופעות מהן סובלים לעיתים אנשים בתגובה לאירועי חיים מלחיצים. אנא ציין/י באיזו מידה הפריעה לך בעיה זו בחודש האחרון."""

SCALE_LABELS = {
    0: "כלל לא",
    1: "במידה מועטה",
    2: "באופן בינוני",
    3: "במידה רבה",
    4: "באופן קיצוני",
}

ITEMS = [
    {"number": 1, "text": "זיכרונות טורדניים, חוזרים ולא רצויים של החוויה הטראומטית"},
    {"number": 2, "text": "חלומות טורדניים, חוזרים של החוויה הטראומטית"},
    {"number": 3, "text": "הרגשה או התנהגות פתאומית כאילו החוויה הטראומטית ממש שבה ומתרחשת שוב"},
    {"number": 4, "text": "הרגשת מצוקה כאשר משהו הזכיר לך את החוויה הטראומטית"},
    {"number": 5, "text": "תגובות גופניות חזקות כאשר משהו הזכיר לך את החוויה הטראומטית (למשל, דפיקות לב, קשיי נשימה, הזעה)"},
    {"number": 6, "text": "הימנעות ממחשבות, רגשות או תחושות גופניות שהזכירו לך את החוויה הטראומטית"},
    {"number": 7, "text": "הימנעות מגורמים חיצוניים שהזכירו לך את החוויה הטראומטית (כמו: אנשים, מקומות, שיחות, חפצים, פעילויות או מצבים)"},
    {"number": 8, "text": "קושי לזכור חלקים חשובים מתוך החוויה הטראומטית"},
    {"number": 9, "text": "אמונות שליליות חזקות על עצמך, או על אנשים אחרים, או על העולם"},
    {"number": 10, "text": "האשמה של עצמך או של מישהו אחר על מה שקרה באירוע או אחריו"},
    {"number": 11, "text": "רגשות שליליים חזקים כמו פחד או אימה, כעס, אשמה או בושה"},
    {"number": 12, "text": "אובדן עניין בפעילויות מהן נהגת ליהנות"},
    {"number": 13, "text": "תחושה של ריחוק או ניתוק מאנשים אחרים"},
    {"number": 14, "text": "קושי להרגיש רגשות חיוביים"},
    {"number": 15, "text": "הרגשת עצבנות או כעסנות או התנהגות תוקפנית"},
    {"number": 16, "text": "לקיחת יותר מידי סיכונים, או עשיית דברים שיכולים להזיק לעצמך"},
    {"number": 17, "text": "תחושה של דריכות, עמידה על המשמר או ערנות מוגברת"},
    {"number": 18, "text": "הרגשה שאתה נוטה להיבהל בקלות או מאוד קופצני"},
    {"number": 19, "text": "קשיים בריכוז"},
    {"number": 20, "text": "קשיים להירדם או להישאר ישנ/ה"},
]

REVERSED_ITEMS = []

CLUSTERS = {
    "B": {"name": "חודרנות", "items": [1, 2, 3, 4, 5]},
    "C": {"name": "הימנעות", "items": [6, 7]},
    "D": {"name": "שינויים שליליים בקוגניציה ובמצב רוח", "items": [8, 9, 10, 11, 12, 13, 14]},
    "E": {"name": "שינויים בעוררות ובתגובתיות", "items": [15, 16, 17, 18, 19, 20]},
}

# DSM-5 minimum symptom counts per cluster for provisional diagnosis
DSM5_MIN_SYMPTOMS = {
    "B": 1,
    "C": 1,
    "D": 2,
    "E": 2,
}


def score(responses):
    """
    Calculate PCL-5 score.
    responses: dict mapping item number (int) -> raw score (int, 0-4)
    Returns dict with total, cluster scores, severity, interpretation,
    and DSM-5 provisional diagnosis.
    """
    total = sum(responses.values())

    results = {
        "total": total,
        "score_range": "0-80",
        "clusters": {},
    }

    # Calculate cluster scores and DSM-5 provisional diagnosis
    dsm5_met = True
    for cluster_key, cluster_info in CLUSTERS.items():
        cluster_items = cluster_info["items"]
        cluster_sum = sum(responses[i] for i in cluster_items)
        symptoms_present = sum(1 for i in cluster_items if responses[i] >= 2)
        cluster_max = len(cluster_items) * 4

        results["clusters"][cluster_key] = {
            "name": cluster_info["name"],
            "score": cluster_sum,
            "max": cluster_max,
            "symptoms_present": symptoms_present,
        }

        if symptoms_present < DSM5_MIN_SYMPTOMS[cluster_key]:
            dsm5_met = False

    results["dsm5_provisional"] = dsm5_met

    # Severity and interpretation
    if total < 33:
        results["severity"] = "מתחת לסף"
        results["interpretation"] = "רמת תסמיני PTSD מתחת לסף הקליני (ציון < 33)"
    else:
        results["severity"] = "סיכון קליני"
        results["interpretation"] = "דגל אדום: ציון מעל סף קליני ל-PTSD (ציון ≥ 33)"

    if dsm5_met:
        results["dsm5_note"] = "עומד בקריטריונים לאבחנה זמנית של PTSD לפי DSM-5 (מספר מינימלי של תסמינים בכל אשכול)"
    else:
        results["dsm5_note"] = "אינו עומד בקריטריונים לאבחנה זמנית של PTSD לפי DSM-5"

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
