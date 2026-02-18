"""
SHS - Subjective Happiness Scale
מדד האושר הסובייקטיבי
Lyubomirsky & Lepper (1999)

4 items, Likert 1-7
Item 4 is REVERSED (score = 8 - raw)
Scoring: Mean of 4 items (after reversal)
"""

NAME = "מדד האושר הסובייקטיבי (SHS)"
CODE = "SHS"

INSTRUCTIONS = """עבור כל אחד מהמשפטים או השאלות הבאות הקף בעיגול את המספר על הסקלה, שאתה חש כי מייצגת את מי שאתה בצורה טובה ביותר."""

# Each item has its own unique scale labels
ITEMS = [
    {
        "number": 1,
        "text": "באופן כללי אני מחשיב את עצמי:",
        "labels": {1: "אדם לא כל כך מאושר", 7: "אדם מאוד מאושר"},
    },
    {
        "number": 2,
        "text": "בהשוואה לחברי אני מחשיב את עצמי:",
        "labels": {1: "פחות מאושר", 7: "יותר מאושר"},
    },
    {
        "number": 3,
        "text": "ישנם אנשים אשר באופן כללי הם מאוד מאושרים. הם נהנים מהחיים ללא קשר לקורה סביבם, וממצים את הטוב ביותר מכל דבר. באיזו מידה אפיון זה מתאר אותך?",
        "labels": {1: "כלל לא", 7: "במידה רבה מאוד"},
    },
    {
        "number": 4,
        "text": "ישנם אנשים שבאופן כללי אינם מאוד מאושרים. אף-על-פי שהם אינם מדוכאים, נראה שהם לעולם אינם מאושרים כפי שיכלו להיות. באיזו מידה אפיון זה מתאר אותך?",
        "labels": {1: "כלל לא", 7: "במידה רבה מאוד"},
    },
]

SCALE_LABELS = {}  # Not used globally; each item has its own labels
REVERSED_ITEMS = [4]


def score(responses):
    """
    Calculate SHS score.
    responses: dict mapping item number (int) -> raw score (int, 1-7)
    Returns dict with total mean and interpretation.
    """
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 8 - raw
        else:
            scored[item_num] = raw

    total_mean = sum(scored.values()) / len(scored)
    results = {
        "item_scores": {f"פריט {k}": v for k, v in sorted(scored.items())},
        "total": round(total_mean, 2),
    }

    if total_mean >= 6:
        results["interpretation"] = "אושר סובייקטיבי גבוה מהממוצע"
    elif total_mean >= 4.5:
        results["interpretation"] = "אושר סובייקטיבי בטווח הממוצע (ממוצע באוכלוסייה האמריקאית: 4.5-5.5)"
    elif total_mean >= 3.5:
        results["interpretation"] = "אושר סובייקטיבי מתחת לממוצע"
    else:
        results["interpretation"] = "אושר סובייקטיבי נמוך"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 1,
    "scale_max": 7,
    "score": score,
}
