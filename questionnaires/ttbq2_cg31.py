"""
TTBQ2-CG31 - Two-Track Bereavement Questionnaire - Complicated Grief 31
השאלון הדו-מסלולי לאובדן ושכול – גרסת אבל מורכב 31
Rubin, Bar-Nadav & Malkinson

31 items across 4 parts (A, B, C, D), Likert 1-5
4 subscales:
  - Track I - Dysfunction (I-DF): 8 items
  - Track II - Active Relational Traumatic Grief (II-ARTG): 16 items
  - Track II - Relational Conflict (II-RC): 5 items
  - Track II - Close Positive Relationship (II-CPR): 2 items
Note: B5(B9) is scored under both I-DF and II-RC per the manual.

Reversed items marked with R: score reversed so 1=5, 2=4, 3=3, 4=2, 5=1
Scoring: Mean per subscale (sum / number of items completed)
Total: Sum of all subscale raw scores / total items completed
Cutoff: >= 3 suggests complicated grief (after 64+ months since loss)
"""

NAME = "השאלון הדו-מסלולי לאובדן ושכול – אבל מורכב (TTBQ2-CG31)"
CODE = "TTBQ2-CG31"

INSTRUCTIONS = """שאלון זה מתייחס למגוון שאלות אודות החיים שלך לאחר מות אדם חשוב לך.
בכל מקום בו מופיע הקו (______), יש להשיב כאילו כתוב שם שם הנפטר.
מקראה: 1 = נכון מאוד, 2 = נכון, 3 = ככה ככה, 4 = לא כל כך נכון, 5 = לא נכון בכלל.
(בחלק מהשאלות הסולם שונה – אנא שימו לב להנחיות)."""

SCALE_LABELS = {
    1: "נכון מאוד",
    2: "נכון",
    3: "ככה ככה",
    4: "לא כל כך נכון",
    5: "לא נכון בכלל",
}

# Items mapped by their questionnaire codes from the PDF
# Each item has: number (sequential 1-31), text, subscale, reversed flag
# Part A: Items about the last week (items 1-9)
# Part B: Items about the deceased (items 10-21, using ______ for name)
# Part C: Items about the relationship in last 2 years of life (items 22-25)
# Part D: Items about current feelings (items 26-31)

ITEMS = [
    # Part A - Last week
    {"number": 1, "text": "מצב רוחי מאוד מדוכא", "subscale": "I-DF", "code": "A2"},
    {"number": 2, "text": "אני מרגיש מאוד חרד", "subscale": "I-DF", "code": "A3"},
    {"number": 3, "text": "כיוון השינויים במשמעות לחיי היה לרעה בלבד", "subscale": "I-DF", "code": "A6"},
    {"number": 4, "text": "מחשבות ורגשות מציפים ומבלבלים אותי", "subscale": "II-ARTG", "code": "A7",
     "alt_scale": {1: "מספר פעמים ביום", 2: "כמעט בכל יום", 3: "כמעט בכל שבוע", 4: "כמעט בכל חודש", 5: "כמעט אף פעם"}},
    {"number": 5, "text": "אני מתפקד בעבודה / בלימודים בצורה טובה מאוד (סמן X אם אינו רלוונטי)", "subscale": "I-DF", "code": "A9"},
    {"number": 6, "text": "התפיסה העצמית שלי השבוע הייתה חיובית כמעט לגמרי", "subscale": "I-DF", "code": "A11"},
    {"number": 7, "text": "אני מתקשה לתפקד מבחינה חברתית", "subscale": "I-DF", "code": "A12"},
    {"number": 8, "text": "האמונה והביטחון ביכולת שלי להתמודד בכוחות עצמי עם מטלות החיים חזקה מאוד", "subscale": "I-DF", "code": "A19"},
    {"number": 9, "text": "בעקבות האובדן, ניתן להגדיר את מצבי הנוכחי כמאוד זקוק לעזרה", "subscale": "II-ARTG", "code": "A20"},
    # Part B - About the deceased
    {"number": 10, "text": "יחסיי עם ______ היו כאלו שכשאני חושב עליו, אני בדרך כלל נזכר בחילוקי הדעות שהיו לנו", "subscale": "II-RC", "code": "B2*"},
    {"number": 11, "text": "קורה שאני מתנהג או מגיב באופן רגשי, כאילו אני לא מאמין ש______ איננו/ה. דבר זה קורה לי:",
     "subscale": "II-ARTG", "code": "B4",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 12, "text": "אני חושב על ______ כל הזמן", "subscale": "II-ARTG", "code": "B6"},
    {"number": 13, "text": "כיום הגעתי למידה של השלמה עם האובדן של ______", "subscale": "II-ARTG", "code": "B7"},
    {"number": 14, "text": "מחשבות על ______ מעוררות בי תחושות חיוביות", "subscale": "II-RC", "code": "B9"},
    {"number": 15, "text": "אני זוכר את ______:",
     "subscale": "II-ARTG", "code": "B10",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 16, "text": "אני נמנע מדברים שמזכירים לי את ______", "subscale": "II-RC", "code": "B11"},
    {"number": 17, "text": "החיים בלי ______ קשים מנשוא", "subscale": "II-ARTG", "code": "B13"},
    {"number": 18, "text": "אני חש געגועים עזים ל______:",
     "subscale": "II-ARTG", "code": "B15",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 19, "text": "אני חש כאב כשאני נזכר ב______", "subscale": "II-ARTG", "code": "B16"},
    {"number": 20, "text": "עכשיו אני מבין אנשים שחושבים לשים קץ לחייהם אחרי אובדן של אדם קרוב", "subscale": "II-ARTG", "code": "B17"},
    {"number": 21, "text": "ניתן להגדיר את מצבי היום בעקבות האובדן כמאוד סובל", "subscale": "II-ARTG", "code": "B20"},
    # Part C - Relationship in last 2 years of life
    {"number": 22, "text": "בחייו/ה, ______ היה/הייתה בעבורי מקור מרכזי לתמיכה רגשית", "subscale": "II-CPR", "code": "C2"},
    {"number": 23, "text": "היחסים שלי ושל ______ התאפיינו בעליות ומורדות בולטות ותכופות", "subscale": "II-CPR", "code": "C4"},
    {"number": 24, "text": "היחסים שלי עם ______ התאפיינו במעברים חדים בין קרבה לבין כעס ו/או רצון להתרחק", "subscale": "II-CPR", "code": "C7"},
    {"number": 25, "text": "______ היה/הייתה האדם הקרוב ביותר אלי", "subscale": "II-RC", "code": "C8"},
    # Part D - Current feelings
    {"number": 26, "text": "אני כועס בגלל האובדן", "subscale": "II-ARTG", "code": "D4"},
    {"number": 27, "text": "אני ממשיך לחוות את האובדן כאירוע מזעזע וטראומטי בחיי", "subscale": "II-ARTG", "code": "D7"},
    {"number": 28, "text": "אני רואה תמונות או בבואות ממקום המוות שנכנסות למחשבותיי:",
     "subscale": "II-ARTG", "code": "D10",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 29, "text": "אני רואה תמונות או בבואות של ______ בראשי:",
     "subscale": "II-ARTG", "code": "D11",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 30, "text": "מחשבות ורגשות על מותו/ה של ______ מציפים אותי",
     "subscale": "II-ARTG", "code": "D14",
     "alt_scale": {1: "כמעט אף פעם", 2: "כמעט בכל חודש", 3: "כמעט בכל שבוע", 4: "כמעט בכל יום", 5: "מספר פעמים ביום"}},
    {"number": 31, "text": "אני מסוגל לדבר ולחלוק את רגשותיי עם אנשים אחרים ולקבל את עזרתם ותמיכתם", "subscale": "I-DF", "code": "D18*"},
]

# Reversed items per the scoring key in the PDF (marked with R)
# These are items where the scale direction means that LOW numbers = more distress
# After reversal, HIGH score = more distress for all items
# From scoring key: items with -r suffix need reversal
# A2-r, A3-r, A6-r, A7-r, A12-r, A20-r (Part A reversed)
# B2*-r, B6-r, B8-r (B13-r), B10-r (B16-r), B11-r, B13-r (B17-r), B20-r (Part B reversed)
# C2-r, C4-r, C7-r, C8-r (Part C reversed)
# D4-r, D7-r (Part D reversed)
# Non-reversed: A9, A11, A19, B4, B7, B9(B14), B10(B15), D10, D11, D14, D18*

REVERSED_ITEMS = [1, 2, 3, 4, 7, 9, 10, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Subscale definitions mapping item numbers to subscales
SUBSCALE_ITEMS = {
    "I-DF": [1, 2, 3, 5, 6, 7, 8, 31],  # A2, A3, A6, A9, A11, A12, A19, D18*
    "II-ARTG": [4, 9, 11, 12, 13, 15, 17, 18, 19, 20, 21, 26, 27, 28, 29, 30],  # 16 items
    "II-RC": [10, 14, 16, 25],  # B2*, B9, B11, C8 - note B9/B5 dual-coded
    "II-CPR": [22, 23, 24],  # C2, C4, C7 - note: C4-r and C7-r reversed = high=conflict=distress
}


def score(responses):
    """
    Calculate TTBQ2-CG31 scores.
    responses: dict mapping item number (int) -> raw score (int, 1-5)
    Returns dict with subscale means, total mean, and interpretation.
    """
    # Apply reversals: for reversed items, 1->5, 2->4, 3->3, 4->2, 5->1
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 6 - raw
        else:
            scored[item_num] = raw

    # Calculate subscale scores
    subscale_results = {}
    total_raw_sum = 0
    total_items = 0

    for subscale_name, item_nums in SUBSCALE_ITEMS.items():
        subscale_scores = [scored[n] for n in item_nums if n in scored]
        if subscale_scores:
            raw_sum = sum(subscale_scores)
            mean = raw_sum / len(subscale_scores)
            subscale_results[subscale_name] = {
                "mean": round(mean, 2),
                "raw_sum": raw_sum,
                "items_completed": len(subscale_scores),
            }
            total_raw_sum += raw_sum
            total_items += len(subscale_scores)

    total_mean = round(total_raw_sum / total_items, 2) if total_items > 0 else 0

    results = {
        "total_mean": total_mean,
        "subscales": subscale_results,
        "score_range": "ממוצע 1-5 (ציון גבוה = קשיים רבים יותר)",
    }

    # Subscale labels
    subscale_labels = {
        "I-DF": "מסלול I – חוסר תפקוד",
        "II-ARTG": "מסלול II – התאבלות אקטיבית וטראומה",
        "II-RC": "מסלול II – אספקטים קונפליקטואליים של הקשר",
        "II-CPR": "מסלול II – מערכת יחסים קרובה וחיובית עם הנפטר",
    }
    results["subscale_labels"] = subscale_labels

    # Interpretation based on cutoff >= 3
    if total_mean >= 3:
        results["severity"] = "חמור"
        results["interpretation"] = f"ציון כללי {total_mean} (≥3) – מצביע על אבל מורכב עם קשיי התמודדות משמעותיים. במחקר נמצא כי ציון זה מזהה אנשים עם סיבוכים חמורים בתהליך השכול"
    elif total_mean >= 2.5:
        results["severity"] = "בינוני"
        results["interpretation"] = f"ציון כללי {total_mean} – ציון תת-קליני. יש לתת תשומת לב מיוחדת גם לציונים מתחת לנקודת החתך, במיוחד אם יש פריטים בודדים עם ציונים גבוהים"
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = f"ציון כללי {total_mean} – רמה נמוכה של קשיי התמודדות עם האובדן"

    # Flag item 20 (B17 - understanding people who end their lives)
    if 20 in scored and scored[20] >= 4:
        results["clinical_note"] = "שימו לב: פריט 'עכשיו אני מבין אנשים שחושבים לשים קץ לחייהם' סומן ברמה גבוהה – יש לבחון סממנים אובדניים בראיון קליני"

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
