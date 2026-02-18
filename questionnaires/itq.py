"""
ITQ - International Trauma Questionnaire
שאלון הטראומה הבינלאומי
Cloitre et al. (2018)

18 items, Likert 0-4
No reversed items
Scoring: Diagnostic algorithm for PTSD, DSO, and Complex PTSD
"""

NAME = "שאלון הטראומה הבינלאומי (ITQ)"
CODE = "ITQ"

INSTRUCTIONS = """לפניך רשימה של בעיות שלפעמים אנשים מדווחים עליהן לאחר שחוו אירועים טראומטיים. אנא ענה על השאלות ביחס לאירוע שמטריד אותך הכי הרבה. סמן עד כמה אתה מוטרד מהתגובות הללו בחודש האחרון."""

SCALE_LABELS = {
    0: "כלל לא",
    1: "במידה מועטה",
    2: "במידה בינונית",
    3: "במידה רבה",
    4: "במידה רבה מאוד",
}

ITEMS = [
    # PTSD symptoms
    {"number": 1, "text": "חלומות מטרידים בהם חוזרים חלקים מאירוע, או חלומות אשר קשורים לאירוע", "section": "תסמיני PTSD"},
    {"number": 2, "text": "דימויים או זיכרונות חזקים שעולים בראשך בהם אתה מרגיש כאילו האירוע מתרחש שוב כאן ועכשיו", "section": "תסמיני PTSD"},
    {"number": 3, "text": "הימנעות מתזכורות פנימיות של האירוע (למשל, מחשבות, רגשות או תחושות גופניות)", "section": "תסמיני PTSD"},
    {"number": 4, "text": "הימנעות מתזכורות חיצוניות של האירוע (למשל, אנשים, מקומות, שיחות, חפצים, פעילויות או מצבים)", "section": "תסמיני PTSD"},
    {"number": 5, "text": "תחושה של דריכות, ערנות או עמידה על המשמר", "section": "תסמיני PTSD"},
    {"number": 6, "text": "הרגשה שאתה קופצני או נבהל בקלות", "section": "תסמיני PTSD"},
    # Functional impairment (PTSD)
    {"number": 7, "text": "השפיעו על מערכות היחסים או על חיי החברה שלך", "section": "פגיעה תפקודית - PTSD"},
    {"number": 8, "text": "השפיעו על עבודתך או על יכולתך לעבוד", "section": "פגיעה תפקודית - PTSD"},
    {"number": 9, "text": "השפיעו על חלק חשוב אחר בחייך כגון הורות, לימודים או פעילויות חשובות אחרות", "section": "פגיעה תפקודית - PTSD"},
    # DSO symptoms
    {"number": 10, "text": "כאשר אני מוטרד, לוקח לי זמן רב להירגע", "section": "הפרעות בארגון העצמי"},
    {"number": 11, "text": "אני מרגיש קהות חושים, כבוי חושית", "section": "הפרעות בארגון העצמי"},
    {"number": 12, "text": "אני מרגיש שאני כישלון", "section": "הפרעות בארגון העצמי"},
    {"number": 13, "text": "אני מרגיש חסר ערך", "section": "הפרעות בארגון העצמי"},
    {"number": 14, "text": "אני חש מרוחק או מנותק מאנשים", "section": "הפרעות בארגון העצמי"},
    {"number": 15, "text": "אני מתקשה להישאר קרוב רגשית לאחרים", "section": "הפרעות בארגון העצמי"},
    # Functional impairment (DSO)
    {"number": 16, "text": "עוררו דאגה או מצוקה בנוגע למערכות היחסים שלך או חיי החברה שלך", "section": "פגיעה תפקודית - DSO"},
    {"number": 17, "text": "השפיעו על עבודתך או יכולתך לעבוד", "section": "פגיעה תפקודית - DSO"},
    {"number": 18, "text": "השפיעו על חלק חשוב אחר בחייך, כגון הורות, לימודים או כל פעילויות חשובות אחרות", "section": "פגיעה תפקודית - DSO"},
]

REVERSED_ITEMS = []

# Item groupings for diagnostic algorithm
PTSD_RE_EXPERIENCING = [1, 2]       # P1, P2
PTSD_AVOIDANCE = [3, 4]             # P3, P4
PTSD_HYPERAROUSAL = [5, 6]          # P5, P6
PTSD_FUNCTIONAL = [7, 8, 9]         # P7, P8, P9
DSO_AFFECT_DYSREGULATION = [10, 11] # C1, C2
DSO_NEGATIVE_SELF = [12, 13]        # C3, C4
DSO_DISTURBED_RELATIONS = [14, 15]  # C5, C6
DSO_FUNCTIONAL = [16, 17, 18]       # C7, C8, C9

PTSD_SYMPTOM_ITEMS = [1, 2, 3, 4, 5, 6]
DSO_SYMPTOM_ITEMS = [10, 11, 12, 13, 14, 15]


def _cluster_met(responses, item_numbers, threshold=2):
    """Check if at least one item in the cluster scores >= threshold."""
    return any(responses.get(i, 0) >= threshold for i in item_numbers)


def score(responses):
    """
    Calculate ITQ score using diagnostic algorithm.
    responses: dict mapping item number (int) -> raw score (int, 0-4)
    Returns dict with diagnostic results and scores.
    """
    # PTSD diagnosis
    re_experiencing_met = _cluster_met(responses, PTSD_RE_EXPERIENCING)
    avoidance_met = _cluster_met(responses, PTSD_AVOIDANCE)
    hyperarousal_met = _cluster_met(responses, PTSD_HYPERAROUSAL)
    ptsd_functional_met = _cluster_met(responses, PTSD_FUNCTIONAL)

    ptsd_met = all([re_experiencing_met, avoidance_met, hyperarousal_met, ptsd_functional_met])

    # DSO diagnosis
    affect_dysreg_met = _cluster_met(responses, DSO_AFFECT_DYSREGULATION)
    negative_self_met = _cluster_met(responses, DSO_NEGATIVE_SELF)
    disturbed_rel_met = _cluster_met(responses, DSO_DISTURBED_RELATIONS)
    dso_functional_met = _cluster_met(responses, DSO_FUNCTIONAL)

    dso_met = all([affect_dysreg_met, negative_self_met, disturbed_rel_met, dso_functional_met])

    # Complex PTSD
    cptsd_met = ptsd_met and dso_met

    # Symptom sums
    ptsd_symptom_sum = sum(responses.get(i, 0) for i in PTSD_SYMPTOM_ITEMS)
    dso_symptom_sum = sum(responses.get(i, 0) for i in DSO_SYMPTOM_ITEMS)
    total_sum = sum(responses.values())

    results = {
        "ptsd_met": ptsd_met,
        "dso_met": dso_met,
        "cptsd_met": cptsd_met,
        "ptsd_symptom_sum": ptsd_symptom_sum,
        "dso_symptom_sum": dso_symptom_sum,
        "total_sum": total_sum,
        "score_range": "0-72",
    }

    # Severity and interpretation
    if cptsd_met:
        results["severity"] = "חמור"
        results["interpretation"] = (
            "עומד בקריטריונים לאבחנת PTSD מורכב (Complex PTSD): "
            "קריטריוני PTSD מתקיימים וכן קריטריוני הפרעה בארגון העצמי (DSO)"
        )
    elif ptsd_met and not dso_met:
        results["severity"] = "בינוני-חמור"
        results["interpretation"] = (
            "עומד בקריטריונים לאבחנת PTSD: "
            "נמצאו תסמיני חוויה-מחדש, הימנעות, עוררות-יתר ופגיעה תפקודית"
        )
    elif dso_met and not ptsd_met:
        results["severity"] = "בינוני"
        results["interpretation"] = (
            "עומד בקריטריוני הפרעה בארגון העצמי (DSO) אך לא בקריטריוני PTSD מלאים"
        )
    else:
        results["severity"] = "מתחת לסף"
        results["interpretation"] = "אינו עומד בקריטריונים לאבחנת PTSD או PTSD מורכב"

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
