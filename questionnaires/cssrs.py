"""
C-SSRS - Columbia Suicide Severity Rating Scale (Screening Version)
סולם קולומביה לדירוג חומרת האובדנות – גרסת סינון
Posner et al. (2011)

Semi-structured screening interview with Yes/No questions.
Suicidal Ideation: 5 levels (1-5), with branching logic.
Suicidal Behavior: 4 types.
Intensity rating for most severe ideation (frequency, duration, controllability, deterrents, reasons).

Adapted for self-report format: all items presented as Yes/No.
Scoring: highest ideation level endorsed (1-5), plus behavior flags.
"""

NAME = "סולם קולומביה לדירוג חומרת האובדנות – גרסת סינון (C-SSRS)"
CODE = "C-SSRS"

INSTRUCTIONS = """אנא ענה על השאלות הבאות בכנות. השאלות מתייחסות למחשבות והתנהגויות בחודש האחרון.
אם התשובות לשאלות 1 ו-2 שליליות, דלג ישירות לחלק ב' (התנהגות אובדנית)."""

# C-SSRS uses Yes(1)/No(0) scale
SCALE_LABELS = {
    0: "לא",
    1: "כן",
}

ITEMS = [
    # Part A: Suicidal Ideation
    {"number": 1, "text": "הרצון להיות מת/ה: האם היית רוצה להיות מת/ה או האם את/ה מייחל/ת להירדם ולא להתעורר עוד?", "section": "מחשבות אובדניות"},
    {"number": 2, "text": "מחשבות אובדניות פעילות בלתי ספציפיות: האם יש לך מחשבות על התאבדות?", "section": "מחשבות אובדניות"},
    {"number": 3, "text": "מחשבות אובדניות פעילות בשיטה כלשהי (לא תכנית) ללא כוונת פעולה: האם חשבת כיצד היית יכול/ה לעשות זאת?", "section": "מחשבות אובדניות"},
    {"number": 4, "text": "מחשבות אובדניות פעילות עם כוונה מסוימת לפעול, אך ללא תכנית ספציפית: האם יש לך מחשבות כאלה וכוונה כלשהי לפעול על פיהן?", "section": "מחשבות אובדניות"},
    {"number": 5, "text": "מחשבות אובדניות פעילות עם תכנית וכוונה מוגדרות: האם התחלת לעבד או כבר עיבדת את הפרטים של אופן ההתאבדות? האם בכוונתך להוציא תכנית זו אל הפועל?", "section": "מחשבות אובדניות"},
    # Part B: Suicidal Behavior
    {"number": 6, "text": "ניסיון בפועל: האם ביצעת ניסיון התאבדות? האם עשית משהו במטרה לפגוע בעצמך? האם עשית משהו מסוכן שיכול היה לגרום למותך?", "section": "התנהגות אובדנית"},
    {"number": 7, "text": "ניסיון שסוכל: האם קרה שהתחלת לבצע משהו כדי לשים קץ לחייך, אך מישהו או משהו עצר בעדך בטרם הספקת לבצע דבר למעשה?", "section": "התנהגות אובדנית"},
    {"number": 8, "text": "ניסיון שנזנח: האם קרה שהתחלת לבצע משהו כדי לנסות לשים קץ לחייך, אך עצרת בעצמך בטרם ביצעת משהו למעשה?", "section": "התנהגות אובדנית"},
    {"number": 9, "text": "פעולות הכנה או התנהגות מכינה: האם נקטת צעדים כלשהם לקראת ביצוע ניסיון התאבדות או התחלת בפעולות הכנה (כגון איסוף כדורים, הצטיידות באקדח, מסירה של דברי ערך או חיבור מכתב פרידה)?", "section": "התנהגות אובדנית"},
    {"number": 10, "text": "פגיעה עצמית שאיננה אובדנית: האם התנהגת באופן של פגיעה עצמית ללא כוונת התאבדות?", "section": "התנהגות אובדנית"},
]

REVERSED_ITEMS = []

INTENSITY_ITEMS = [
    {
        "number": "I1",
        "text": "תדירות: כמה פעמים היו לך מחשבות אלו?",
        "labels": {
            1: "פעם אחת בלבד",
            2: "פחות מפעם בשבוע",
            3: "פעם בשבוע",
            4: "מדי יום או כמעט מדי יום",
            5: "הרבה פעמים ביום",
        },
    },
    {
        "number": "I2",
        "text": "משך: כמה זמן נמשכו המחשבות?",
        "labels": {
            1: "חולפות — שניות ספורות או דקות",
            2: "פרק זמן קצר — עד שעה",
            3: "פרק זמן ארוך — מספר שעות ביום",
            4: "פרק זמן ארוך מאוד — רוב שעות היום",
            5: "מתמשכות או בלתי פוסקות",
        },
    },
    {
        "number": "I3",
        "text": "שליטה: האם יכולת לשלוט במחשבות?",
        "labels": {
            1: "בקלות — יכולתי להפסיק לחשוב בנקל",
            2: "עם מאמץ מסוים",
            3: "בקושי",
            4: "בקושי רב",
            5: "לא יכולתי לשלוט — המחשבות השתלטו",
        },
    },
    {
        "number": "I4",
        "text": "גורמים מרתיעים: האם היו דברים שמנעו ממך לפעול?",
        "labels": {
            1: "גורמים מרתיעים מנעו ממך בבירור",
            2: "גורמים מרתיעים ככל הנראה מנעו ממך",
            3: "לא בטוח/ה אם גורמים מרתיעים מנעו ממך",
            4: "גורמים מרתיעים ככל הנראה לא מנעו ממך",
            5: "גורמים מרתיעים בהחלט לא מנעו ממך",
        },
    },
    {
        "number": "I5",
        "text": "סיבות: מדוע רצית להתאבד?",
        "labels": {
            1: "כדי למשוך תשומת לב, להתנקם, או לעורר תגובה מאחרים",
            2: "דרך לסיים או להפסיק את הכאב (לא ראית דרך אחרת)",
            3: "שילוב של 1 ו-2",
            4: "בעיקר כדי לסיים את הכאב",
            5: "לגמרי כדי לסיים את הכאב ולהיעלם",
        },
    },
]


def score(responses):
    """
    Calculate C-SSRS screening score.
    responses: dict mapping item number (int) -> 0 (No) or 1 (Yes)
    Returns dict with ideation level, behavior flags, and risk assessment.
    """
    # Determine highest ideation level (items 1-5)
    ideation_level = 0
    for i in range(5, 0, -1):
        if responses.get(i, 0) == 1:
            ideation_level = i
            break

    # Check behavior (items 6-10)
    actual_attempt = responses.get(6, 0) == 1
    interrupted_attempt = responses.get(7, 0) == 1
    aborted_attempt = responses.get(8, 0) == 1
    preparatory_behavior = responses.get(9, 0) == 1
    non_suicidal_self_injury = responses.get(10, 0) == 1

    any_behavior = actual_attempt or interrupted_attempt or aborted_attempt or preparatory_behavior

    results = {
        "ideation_level": ideation_level,
        "actual_attempt": actual_attempt,
        "interrupted_attempt": interrupted_attempt,
        "aborted_attempt": aborted_attempt,
        "preparatory_behavior": preparatory_behavior,
        "non_suicidal_self_injury": non_suicidal_self_injury,
        "score_range": "רמת חשיבה: 0-5, התנהגות: כן/לא",
    }

    # Risk assessment
    ideation_labels = {
        0: "לא דווח על מחשבות אובדניות",
        1: "רצון להיות מת/ה",
        2: "מחשבות אובדניות פעילות בלתי ספציפיות",
        3: "מחשבות אובדניות פעילות עם שיטה כלשהי",
        4: "מחשבות אובדניות פעילות עם כוונה לפעול",
        5: "מחשבות אובדניות פעילות עם תכנית וכוונה מוגדרות",
    }
    results["ideation_description"] = ideation_labels[ideation_level]

    # Determine severity
    if actual_attempt:
        results["severity"] = "קריטי"
        results["interpretation"] = "דווח על ניסיון אובדני בפועל – נדרשת התערבות מיידית"
    elif ideation_level >= 4 or preparatory_behavior:
        results["severity"] = "חמור"
        results["interpretation"] = "מחשבות אובדניות ברמת חומרה גבוהה ו/או פעולות הכנה – נדרשת הערכה קלינית דחופה"
    elif ideation_level >= 3 or interrupted_attempt or aborted_attempt:
        results["severity"] = "בינוני-חמור"
        results["interpretation"] = "מחשבות אובדניות עם שיטה ו/או ניסיונות שסוכלו/נזנחו – נדרשת הערכה קלינית"
    elif ideation_level >= 1:
        results["severity"] = "בינוני"
        results["interpretation"] = "דווח על מחשבות אובדניות – יש לבחון בראיון קליני"
    else:
        results["severity"] = "ללא"
        results["interpretation"] = "לא דווח על מחשבות או התנהגויות אובדניות בתקופת ההערכה"

    if non_suicidal_self_injury:
        results["clinical_note"] = "דווח על פגיעה עצמית שאיננה אובדנית – יש לבחון בראיון קליני"

    # Build behavior summary
    behaviors = []
    if actual_attempt:
        behaviors.append("ניסיון בפועל")
    if interrupted_attempt:
        behaviors.append("ניסיון שסוכל")
    if aborted_attempt:
        behaviors.append("ניסיון שנזנח")
    if preparatory_behavior:
        behaviors.append("פעולות הכנה")
    if non_suicidal_self_injury:
        behaviors.append("פגיעה עצמית לא אובדנית")
    results["behavior_summary"] = ", ".join(behaviors) if behaviors else "לא דווח על התנהגויות אובדניות"

    # Intensity ratings (only present if ideation was endorsed)
    if ideation_level >= 1:
        intensity = {}
        intensity_total = 0
        for iitem in INTENSITY_ITEMS:
            inum = iitem["number"]
            ival = responses.get(inum, 0)
            if ival:
                intensity[inum] = {
                    "label": iitem["text"].split(":")[0],
                    "value": ival,
                    "description": iitem["labels"].get(ival, ""),
                }
                intensity_total += ival
        if intensity:
            results["intensity"] = intensity
            results["intensity_total"] = intensity_total

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
    "intensity_items": INTENSITY_ITEMS,
}
