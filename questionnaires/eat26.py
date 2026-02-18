"""
EAT-26 - Eating Attitudes Test
מבחן עמדות אכילה
Garner, Olmsted, Bohr & Garfinkel (1982)

26 items, 6-point scale (0-5)
Special scoring: top 3 responses score points (5→3, 4→2, 3→1, rest→0)
Item 25 is reverse scored (0→3, 1→2, 2→1, rest→0)
Total score range: 0-78, cutoff >= 20
"""

NAME = "מבחן עמדות אכילה (EAT-26)"
CODE = "EAT26"

INSTRUCTIONS = """סמן את האפשרות הנראית לך מתאימה ביותר (אף פעם, לעיתים רחוקות, לפעמים, לעיתים קרובות, בדרך כלל ותמיד)."""

SCALE_LABELS = {
    0: "אף פעם",
    1: "לעיתים רחוקות",
    2: "לפעמים",
    3: "לעיתים קרובות",
    4: "בדרך כלל",
    5: "תמיד",
}

ITEMS = [
    {"number": 1, "text": "מפחידה אותי המחשבה שאני שמן"},
    {"number": 2, "text": "אני נמנע מאכילה שאני רעב"},
    {"number": 3, "text": "אני מוצא את עצמי מגלה עסוק יתר בנושאי אוכל"},
    {"number": 4, "text": "התנסיתי בזלילה תוך הרגשה שאיני יכול לחדול"},
    {"number": 5, "text": "אני חותך את המזון לפיסות קטנות"},
    {"number": 6, "text": "אני מודע לכמות הקלוריות במזון אותו אני אוכל"},
    {"number": 7, "text": "אני נמנע במיוחד מאכילת מזון עשיר בפחמימות (לחם, אורז, תפוחי אדמה וכו')"},
    {"number": 8, "text": "אני מרגיש שאחרים היו מעדיפים שאוכל יותר"},
    {"number": 9, "text": "אני מקיא לאחר הארוחה"},
    {"number": 10, "text": "אני חש מאוד אשם לאחר אכילה"},
    {"number": 11, "text": "אני מגלה עיסוק יתר בשאיפה להיות רזה יותר"},
    {"number": 12, "text": "אני חושב על שריפת קלוריות בזמן שאני מתעמל"},
    {"number": 13, "text": "אחרים חושבים שאני רזה"},
    {"number": 14, "text": "אני מוטרד מהמחשבה שיש שומן על גופי"},
    {"number": 15, "text": "לוקח לי יותר זמן מאשר לאחרים לאכול את הארוחות"},
    {"number": 16, "text": "אני נמנע מלאכול מזון עם סוכר"},
    {"number": 17, "text": "אני אוכל מזון דיאטטי"},
    {"number": 18, "text": "אני מרגיש שאוכל שולט על חיי"},
    {"number": 19, "text": "אני מראה שליטה עצמית בנושא מזון"},
    {"number": 20, "text": "אני מרגיש שאחרים לוחצים עליי לאכול"},
    {"number": 21, "text": "אני מקדיש יותר מידי זמן ומחשבה לאוכל"},
    {"number": 22, "text": "אני מרגיש אי נוחות לאחר אכילת ממתקים"},
    {"number": 23, "text": "אני עסוק בענייני דיאטה"},
    {"number": 24, "text": "אני מעדיף שהקיבה שלי תהיה ריקה"},
    {"number": 25, "text": "אני נהנה לנסות מאכלים חדשים עשירי קלוריות"},
    {"number": 26, "text": "יש לי דחף להקיא אחרי ארוחות"},
]

REVERSED_ITEMS = [25]

BEHAVIORAL_ITEMS = [
    {"number": "B1", "text": "האם אכלת בזלילה כשהרגשת שאינך יכול/ה להפסיק?"},
    {"number": "B2", "text": "האם הקאת במכוון לאחר אכילה כדי לשלוט במשקלך או בצורת גופך?"},
    {"number": "B3", "text": "האם השתמשת בחומרים משלשלים, כדורי דיאטה או משתנים כדי לשלוט במשקלך או בצורת גופך?"},
    {"number": "B4", "text": "האם התאמנת יותר מ-60 דקות ביום כדי לרדת במשקל או לשלוט במשקלך?"},
    {"number": "B5", "text": "האם ירדת 9 ק\"ג (20 פאונד) או יותר בששת החודשים האחרונים?"},
]

BEHAVIORAL_SCALE_LABELS = {
    0: "אף פעם",
    1: "פעם בחודש או פחות",
    2: "2-3 פעמים בחודש",
    3: "פעם בשבוע",
    4: "2-6 פעמים בשבוע",
    5: "פעם ביום או יותר",
}

SUBSCALES = {
    "דיאטה": [1, 6, 7, 10, 11, 12, 14, 16, 17, 22, 23, 24, 25],
    "בולימיה": [3, 4, 9, 18, 21, 26],
    "שליטה": [2, 5, 8, 13, 15, 19, 20],
}


def _score_item(item_number, raw_value):
    """
    Apply EAT-26 special scoring to a single item.
    For most items: raw 5→3, raw 4→2, raw 3→1, raw 0,1,2→0
    For item 25 (reversed): raw 0→3, raw 1→2, raw 2→1, raw 3,4,5→0
    """
    if item_number == 25:
        # Reverse scored item
        scoring_map = {0: 3, 1: 2, 2: 1, 3: 0, 4: 0, 5: 0}
    else:
        # Standard scoring
        scoring_map = {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 3}
    return scoring_map.get(raw_value, 0)


def score(responses):
    """
    Calculate EAT-26 score.
    responses: dict mapping item number (int) -> raw score (int, 0-5)
    Returns dict with total score, subscale scores, and interpretation.
    """
    # Score each item using the special scoring
    scored = {item_num: _score_item(item_num, raw) for item_num, raw in responses.items()}

    total = sum(scored.values())

    # Calculate subscale scores
    subscale_scores = {}
    for subscale_name, item_numbers in SUBSCALES.items():
        subscale_total = sum(scored.get(n, 0) for n in item_numbers)
        subscale_scores[subscale_name] = subscale_total

    # Behavioral flags (items B1-B5)
    behavioral_flags = {}
    any_behavioral = False
    for bitem in BEHAVIORAL_ITEMS:
        bnum = bitem["number"]
        bval = responses.get(bnum, 0)
        behavioral_flags[bnum] = bval
        if bval >= 1:  # Any frequency > "never"
            any_behavioral = True

    results = {
        "total": total,
        "score_range": "0-78",
        "cutoff": 20,
        "subscales": subscale_scores,
        "behavioral_flags": behavioral_flags,
    }

    referral_needed = total >= 20 or any_behavioral
    if referral_needed:
        parts = []
        if total >= 20:
            parts.append(f"ציון כולל {total} (≥20)")
        if any_behavioral:
            parts.append("דווח על התנהגויות קליניות")
        results["severity"] = "מומלצת הפניה"
        results["interpretation"] = (
            f"{' + '.join(parts)} – מומלצת הפניה להערכה קלינית מקיפה לאבחון הפרעת אכילה."
        )
    else:
        results["severity"] = "מתחת לסף קליני"
        results["interpretation"] = f"ציון כולל {total} (<20) וללא דיווח על התנהגויות קליניות."

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 0,
    "scale_max": 5,
    "score": score,
    "behavioral_items": BEHAVIORAL_ITEMS,
    "behavioral_scale_labels": BEHAVIORAL_SCALE_LABELS,
    "behavioral_scale_min": 0,
    "behavioral_scale_max": 5,
}
