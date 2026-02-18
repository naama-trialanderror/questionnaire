"""
DERS - Difficulties in Emotion Regulation Scale
סולם קשיים בוויסות רגשי
Gratz & Roemer (2004)

36 items, Likert 1-5
Reversed items: 1,2,6,7,8,10,17,20,22,24,34 (score = 6 - raw)
Scoring: Sum of all items after reversal (range 36-180)
Higher scores = more difficulty in emotion regulation
6 subscales: NONACCEPT, GOALS, IMPULSE, AWARENESS, STRATEGIES, CLARITY
"""

NAME = "סולם קשיים בוויסות רגשי (DERS)"
CODE = "DERS"

INSTRUCTIONS = "אנא ענה עד כמה המשפטים הבאים מתארים אותך בצורה הטובה ביותר."

SCALE_LABELS = {
    1: "כמעט אף פעם לא (0-10%)",
    2: "לפעמים (11-35%)",
    3: "כמחצית מהזמן (36-65%)",
    4: "רוב הזמן (66-90%)",
    5: "כמעט תמיד (91-100%)",
}

ITEMS = [
    {"number": 1, "text": "אני מודע לרגשות שלי"},
    {"number": 2, "text": "אני שם לב לרגשותיי"},
    {"number": 3, "text": "אני חווה את רגשותיי כמסעירים ובלתי נשלטים"},
    {"number": 4, "text": "איני יודע כיצד אני מרגיש"},
    {"number": 5, "text": "אני מתקשה למצוא היגיון ברגשותיי"},
    {"number": 6, "text": "אני קשוב לרגשותיי"},
    {"number": 7, "text": "אני יודע בדיוק כיצד אני מרגיש"},
    {"number": 8, "text": "אכפת לי מה אני מרגיש"},
    {"number": 9, "text": "אני מבולבל ממה שאני מרגיש"},
    {"number": 10, "text": "כשאני נסער, אני מכיר ברגשותיי"},
    {"number": 11, "text": "כשאני נסער, אני כועס על עצמי שאני מרגיש כך"},
    {"number": 12, "text": "כשאני נסער, אני נהיה נבוך שאני מרגיש כך"},
    {"number": 13, "text": "כשאני נסער, אני מתקשה לסיים דברים"},
    {"number": 14, "text": "כשאני נסער, אני מאבד שליטה"},
    {"number": 15, "text": "כשאני נסער, אני מאמין שאשאר במצב זה כך לאורך זמן"},
    {"number": 16, "text": "כשאני נסער, אני מאמין שבסוף ארגיש מאוד מדוכא"},
    {"number": 17, "text": "כשאני נסער, אני מאמין שרגשותיי תקפים ובעלי משמעות"},
    {"number": 18, "text": "כשאני נסער, אני מתקשה להתרכז בדברים נוספים"},
    {"number": 19, "text": "כשאני נסער, אני מרגיש שאני מאבד שליטה"},
    {"number": 20, "text": "כשאני נסער, אני בכל זאת מצליח לסיים דברים"},
    {"number": 21, "text": "כשאני נסער, אני מרגיש בושה כלפי עצמי שאני מרגיש כך"},
    {"number": 22, "text": "כשאני נסער, אני יודע שאני יכול למצוא דרך להרגיש טוב בסופו של דבר"},
    {"number": 23, "text": "כשאני נסער, אני מרגיש שאני חלש"},
    {"number": 24, "text": "כשאני נסער, אני מרגיש שאני עדיין יכול לשלוט על התנהגותי"},
    {"number": 25, "text": "כשאני נסער, אני מרגיש אשמה על שאני מרגיש כך"},
    {"number": 26, "text": "כשאני נסער, אני מתקשה להתרכז"},
    {"number": 27, "text": "כשאני נסער, אני מתקשה לשלוט בהתנהגותי"},
    {"number": 28, "text": "כשאני נסער, אני מאמין שאין משהו שביכולתי לעשות על מנת להרגיש טוב יותר"},
    {"number": 29, "text": "כשאני נסער אני נהיה עצבני על עצמי שאני מרגיש כך"},
    {"number": 30, "text": "כשאני נסער, אני מתחיל להרגיש רע מאוד לגבי עצמי"},
    {"number": 31, "text": "כשאני נסער, אני מאמין שלשקוע בזה, זה כל מה שאני יכול לעשות"},
    {"number": 32, "text": "כשאני נסער, אני מאבד שליטה בהתנהגותי"},
    {"number": 33, "text": "כשאני נסער, אני מתקשה לחשוב על משהו אחר"},
    {"number": 34, "text": "כשאני נסער, אני לוקח זמן להבין מה אני באמת מרגיש"},
    {"number": 35, "text": "כשאני נסער, לוקח לי הרבה זמן להרגיש טוב יותר"},
    {"number": 36, "text": "כשאני נסער, הרגשות שלי מסעירים ומזעזעים"},
]

REVERSED_ITEMS = [1, 2, 6, 7, 8, 10, 17, 20, 22, 24, 34]

SUBSCALES = {
    "NONACCEPT": {"label": "חוסר קבלה", "items": [11, 12, 21, 23, 25, 29], "range": (6, 30)},
    "GOALS": {"label": "התנהגות מכוונת מטרה", "items": [13, 18, 20, 26, 33], "range": (5, 25)},
    "IMPULSE": {"label": "שליטה בדחפים", "items": [3, 14, 19, 24, 27, 32], "range": (6, 30)},
    "AWARENESS": {"label": "מודעות רגשית", "items": [2, 6, 8, 10, 17, 34], "range": (6, 30)},
    "STRATEGIES": {"label": "אסטרטגיות ויסות", "items": [15, 16, 22, 28, 30, 31, 35, 36], "range": (8, 40)},
    "CLARITY": {"label": "בהירות רגשית", "items": [1, 4, 5, 7, 9], "range": (5, 25)},
}


def score(responses):
    """
    Calculate DERS score.
    responses: dict mapping item number (int) -> raw score (int, 1-5)
    Returns dict with total score, subscale scores, and interpretation.
    """
    # Reverse-score applicable items
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 6 - raw
        else:
            scored[item_num] = raw

    # Total score
    total = sum(scored.values())

    results = {
        "total": total,
        "score_range": "טווח 36-180 (ציון גבוה יותר = קושי רב יותר בוויסות רגשי)",
    }

    # Subscale scores
    subscales = {}
    for key, info in SUBSCALES.items():
        sub_items = [scored[i] for i in info["items"] if i in scored]
        sub_total = sum(sub_items)
        subscales[key] = {
            "label": info["label"],
            "score": sub_total,
            "range": f"{info['range'][0]}-{info['range'][1]}",
        }
    results["subscales"] = subscales

    # Interpretation based on severity (no official cutoff; using distribution-based thresholds)
    if total >= 140:
        results["severity"] = "חמור מאוד"
        results["interpretation"] = f"ציון כולל {total} (מתוך 180) – קשיים חמורים מאוד בוויסות רגשי. מומלץ הפניה לטיפול מקצועי"
    elif total >= 116:
        results["severity"] = "חמור"
        results["interpretation"] = f"ציון כולל {total} (מתוך 180) – קשיים חמורים בוויסות רגשי. מומלץ הערכה קלינית מעמיקה"
    elif total >= 92:
        results["severity"] = "בינוני"
        results["interpretation"] = f"ציון כולל {total} (מתוך 180) – קשיים בינוניים בוויסות רגשי"
    elif total >= 68:
        results["severity"] = "קל"
        results["interpretation"] = f"ציון כולל {total} (מתוך 180) – קשיים קלים בוויסות רגשי"
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = f"ציון כולל {total} (מתוך 180) – רמה נמוכה של קשיים בוויסות רגשי"

    # Flag subscales with high scores (above 75% of max)
    high_subscales = []
    for key, info in SUBSCALES.items():
        sub_score = subscales[key]["score"]
        max_score = info["range"][1]
        if sub_score >= max_score * 0.75:
            high_subscales.append(f"{info['label']} ({key})")
    if high_subscales:
        results["clinical_note"] = f"תת-סולמות עם ציון גבוה (≥75% מהטווח): {', '.join(high_subscales)}"

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
