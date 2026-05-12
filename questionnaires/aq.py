"""
AQ - Autism Spectrum Quotient
מנת הספקטרום האוטיסטי
Baron-Cohen et al. (2001), Hebrew validation: Golan & Milua (2006)

50 items, 4-point Likert scale (1-4).
Binary scoring: each item scores 0 or 1 based on direction.
Total range 0-50. Five subscales, 10 items each.

Scoring direction:
- AGREE_ITEMS: score 1 if answer is 1 ("מסכים בהחלט") or 2 ("מסכים במקצת")
- DISAGREE_ITEMS: score 1 if answer is 3 ("לא מסכים במקצת") or 4 ("לא מסכים כלל")

Cutoffs:
- Israel (Golan & Milua, 2006): ≥22 (sensitivity 0.73, specificity 0.82)
- Japan/England (Kurita et al., 2005; Woodbury-Smith et al., 2005): ≥26
- UK original (Baron-Cohen et al., 2001): ≥32
"""

NAME = "מנת הספקטרום האוטיסטי (AQ)"
CODE = "AQ"

INSTRUCTIONS = "קראו כל משפט בתשומת לב ודרגו באיזו מידה אתם מסכימים או אינכם מסכימים."

SCALE_LABELS = {
    1: "מסכים בהחלט",
    2: "מסכים במקצת",
    3: "לא מסכים במקצת",
    4: "לא מסכים כלל",
}

ITEMS = [
    {"number": 1, "text": "אני מעדיף לעשות דברים יחד עם אחרים ולא לבדי"},
    {"number": 2, "text": "אני מעדיף לעשות דברים באותו האופן שוב ושוב"},
    {"number": 3, "text": "כשאני מנסה לדמיין משהו, קל לי מאוד ליצור תמונה בראשי"},
    {"number": 4, "text": "לעתים קרובות אני שוקע עמוק כל-כך בדבר אחד עד שאני מפסיק לראות דברים אחרים"},
    {"number": 5, "text": "לא פעם אני שם לב לקולות חלשים שאחרים אינם שמים לב אליהם"},
    {"number": 6, "text": "בדרך-כלל אני שם לב למספרי מכוניות או לפרטי מידע דומים"},
    {"number": 7, "text": "אנשים אומרים לי פעמים רבות שמה שאמרתי לא מנומס, אף על פי שלי נראה שהייתי מנומס"},
    {"number": 8, "text": "כשאני קורא סיפור אני יכול לדמיין לי בקלות איך נראות הדמויות"},
    {"number": 9, "text": "תאריכים מרתקים אותי"},
    {"number": 10, "text": "בקבוצה חברתית אני מסוגל בקלות לעקוב אחר כמה וכמה שיחות של אנשים"},
    {"number": 11, "text": "אני מסתדר בקלות בסיטואציות חברתיות"},
    {"number": 12, "text": "אני נוטה להבחין בפרטים שאחרים אינם מבחינים בהם"},
    {"number": 13, "text": "אני מעדיף בילוי בספרייה על פני בילוי במסיבה"},
    {"number": 14, "text": "קל לי להמציא סיפורים"},
    {"number": 15, "text": "אני נמשך לבני-אדם יותר מאשר לעצמים"},
    {"number": 16, "text": "יש לי תחומי עניין מוגדרים היטב ואני מתעצבן כשאני לא יכול לעסוק בהם"},
    {"number": 17, "text": "אני נהנה משיחת חולין חברתית"},
    {"number": 18, "text": "כשאני מדבר, לא תמיד קל לאחרים להשחיל מילה"},
    {"number": 19, "text": "מספרים מרתקים אותי"},
    {"number": 20, "text": "כשאני קורא סיפור, קשה לי להבין את כוונותיהן של הדמויות"},
    {"number": 21, "text": "אני לא כל-כך נהנה לקרוא ספרות יפה"},
    {"number": 22, "text": "קשה לי לרכוש חברים חדשים"},
    {"number": 23, "text": "אני שם לב לדפוסים בכל מיני דברים כל הזמן"},
    {"number": 24, "text": "אני מעדיף בילוי בתיאטרון על פני בילוי במוזיאון"},
    {"number": 25, "text": "אני לא מוטרד כששגרת היום שלי מופרת"},
    {"number": 26, "text": "לעתים קרובות מתברר לי שאני לא יודע להחזיק שיחה שלא תגווע"},
    {"number": 27, "text": 'קל לי "לקרוא בין השורות" כשמישהו מדבר אלי'},
    {"number": 28, "text": "בדרך-כלל אני מתרכז בתמונה כולה ולא בפרטים הקטנים"},
    {"number": 29, "text": "אין לי זיכרון טוב למספרי טלפון"},
    {"number": 30, "text": "בדרך-כלל אני לא מבחין בשינויים קלים בסיטואציה או במראהו של אדם אחר"},
    {"number": 31, "text": "אני מבחין מיד כשאדם שמקשיב לי מתחיל להשתעמם"},
    {"number": 32, "text": "קל לי לעשות כמה דברים בבת אחת"},
    {"number": 33, "text": "כשאני מדבר בטלפון, אני לא בטוח מתי תורי לדבר"},
    {"number": 34, "text": "אני נהנה לעשות דברים באופן ספונטני"},
    {"number": 35, "text": "לא פעם אני האחרון שמבין בדיחה"},
    {"number": 36, "text": "אני מבחין בקלות מה אדם אחר חושב או מרגיש ממראה פניו בלבד"},
    {"number": 37, "text": "כשמפריעים לי, אני יכול לחזור למה שעשיתי לפני כן במהירות רבה"},
    {"number": 38, "text": "אני טוב בשיחת חולין חברתית"},
    {"number": 39, "text": "אנשים אומרים לי פעמים רבות שאני מדבר עוד ועוד על אותו הדבר"},
    {"number": 40, "text": 'כשהייתי צעיר נהניתי לשחק עם ילדים אחרים במשחקי "כאילו"'},
    {"number": 41, "text": "אני אוהב לאסוף מידע על סוגים של דברים (למשל, סוגי מכוניות, מיני ציפורים, סוגי רכבות, מיני צמחים וכו')"},
    {"number": 42, "text": "קשה לי לדמיין איך זה להיות אדם אחר"},
    {"number": 43, "text": "אני אוהב לתכנן בקפידה כל פעילות שאני משתתף בה"},
    {"number": 44, "text": "אני נהנה מאירועים חברתיים"},
    {"number": 45, "text": "אני מתקשה להבין את כוונותיהם של אנשים אחרים"},
    {"number": 46, "text": "מצבים חדשים מעוררים בי חרדה"},
    {"number": 47, "text": "אני נהנה להכיר אנשים חדשים"},
    {"number": 48, "text": "אני דיפלומט טוב"},
    {"number": 49, "text": "אני לא מצטיין בזכירת ימי ההולדת של אנשים אחרים"},
    {"number": 50, "text": "קל לי מאוד לשחק עם ילדים במשחקים שכרוכים בהעמדת פנים"},
]

REVERSED_ITEMS = []

# Items where "agree" (1 or 2) scores 1 point — endorsing the item = autistic direction
AGREE_ITEMS = {2, 4, 5, 6, 7, 9, 12, 13, 16, 18, 19, 20, 21, 22, 23, 26, 33, 35, 39, 41, 42, 43, 45, 46}

# Items where "disagree" (3 or 4) scores 1 point — NOT endorsing = autistic direction
DISAGREE_ITEMS = {1, 3, 8, 10, 11, 14, 15, 17, 24, 25, 27, 28, 29, 30, 31, 32, 34, 36, 37, 38, 40, 44, 47, 48, 49, 50}

# Five subscales per Baron-Cohen et al. (2001) / Golan & Milua (2006)
# Each subscale: 10 items, max score = 10
SUBSCALES = {
    "מיומנויות חברתיות": [1, 11, 13, 15, 22, 36, 44, 45, 47, 48],
    "הטיית/שינוי קשב": [2, 4, 10, 16, 25, 32, 34, 37, 43, 46],
    "קשב לפרטים": [5, 6, 9, 12, 19, 23, 28, 29, 30, 49],
    "תקשורת": [7, 17, 18, 26, 27, 31, 33, 35, 38, 39],
    "דמיון": [3, 8, 14, 20, 21, 24, 40, 41, 42, 50],
}

# Cutoff scores from validation studies
CUTOFFS = {
    "ישראל (Golan & Milua, 2006)": {"threshold": 22, "sensitivity": 0.73, "specificity": 0.82},
    "יפן / אנגליה (Kurita et al., 2005; Woodbury-Smith et al., 2005)": {"threshold": 26},
    "UK מקורי (Baron-Cohen et al., 2001)": {"threshold": 32},
}


def score(responses):
    """
    Calculate AQ score with subscale breakdown.
    responses: dict mapping item number (int) -> raw answer (int, 1-4)
    Returns dict with total binary score, subscale breakdown, and interpretation.
    """
    binary_scores = {}
    for item_num, answer in responses.items():
        if not isinstance(item_num, int):
            continue
        if item_num in AGREE_ITEMS:
            binary_scores[item_num] = 1 if answer in (1, 2) else 0
        elif item_num in DISAGREE_ITEMS:
            binary_scores[item_num] = 1 if answer in (3, 4) else 0
        else:
            binary_scores[item_num] = 0

    total = sum(binary_scores.values())

    # Subscale scores
    subscales = {}
    for sub_name, sub_items in SUBSCALES.items():
        sub_score = sum(binary_scores.get(i, 0) for i in sub_items)
        subscales[sub_name] = {
            "score": sub_score,
            "max": 10,
            "items": sub_items,
        }

    results = {
        "total": total,
        "score_range": "סה\"כ 0-50 (סכום ציונים בינאריים)",
        "binary_scores": binary_scores,
        "subscales": subscales,
    }

    # Interpretation with all cutoffs
    above_il = total >= 22
    above_intl = total >= 26
    above_orig = total >= 32

    if above_orig:
        results["severity"] = "גבוה מאוד"
        results["interpretation"] = (
            f"ציון כולל {total}/50 — מעל כל ציוני הסף (ישראל ≥22, יפן/אנגליה ≥26, UK מקורי ≥32). "
            "מעיד על נוכחות משמעותית של תכונות ספקטרום אוטיסטי. מומלץ הפניה לאבחון מקיף."
        )
    elif above_intl:
        results["severity"] = "מעל סף בינלאומי"
        results["interpretation"] = (
            f"ציון כולל {total}/50 — מעל הסף הישראלי (≥22) ומעל הסף הבינלאומי של יפן/אנגליה (≥26). "
            "מומלץ הערכה קלינית נוספת."
        )
    elif above_il:
        results["severity"] = "מעל סף קליני ישראלי"
        results["interpretation"] = (
            f"ציון כולל {total}/50 — מעל סף הקאט-אוף הישראלי (≥22, רגישות 0.73, ספציפיות 0.82). "
            "מומלצת הערכה קלינית נוספת."
        )
    elif total >= 16:
        results["severity"] = "בינוני"
        results["interpretation"] = (
            f"ציון כולל {total}/50 — מתחת לסף הישראלי (22). "
            "מעיד על נוכחות מסוימת של תכונות בספקטרום — בדוק/י בהקשר הקליני הרחב."
        )
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = (
            f"ציון כולל {total}/50 — רמה נמוכה של תכונות ספקטרום אוטיסטי."
        )

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
