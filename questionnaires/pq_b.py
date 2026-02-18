"""
PQ-B - Prodromal Questionnaire Brief
שאלון פרודרומלי מקוצר
Loewy et al. (2011)

21 items, Yes/No (0=לא, 1=כן)
For each endorsed ("Yes") item: distress rating 1-5
No subscales, no reversed items

Scoring:
  - Total endorsed count (range 0-21), cutoff ≥8
  - Total distress score (range 0-105), sum of distress ratings for endorsed items
"""

NAME = "שאלון פרודרומלי מקוצר (PQ-B)"
CODE = "PQ-B"

INSTRUCTIONS = """השאלון הבא שואל מספר שאלות לגבי מחשבות, רגשות וחוויות שיש לעיתים לאנשים. אנא קרא כל פריט, וסמן האם חווית במהלך החודש האחרון את מחשבות, רגשות או חוויות אלו. אנא אל תדווח במידה ותופעות אלו הופיעו אך ורק תחת השפעה של אלכוהול, סמים או תרופות ללא מרשם."""

DISTRESS_INSTRUCTIONS = "אם כן, עד כמה זה גרם לך למצוקה?"

SCALE_LABELS = {
    0: "לא",
    1: "כן",
}

DISTRESS_SCALE_LABELS = {
    1: "לא מסכים בהחלט",
    2: "לא מסכים",
    3: "ניטרלי",
    4: "מסכים",
    5: "מסכים בהחלט",
}

ITEMS = [
    {"number": 1, "text": "האם סביבות מוכרות נראות לך לפעמים זרות, מבלבלות, מאיימות או לא מציאותיות?"},
    {"number": 2, "text": "האם שמעת רעשים לא רגילים כמו דפיקות, נקישות, לחישות, מחיאות כפיים או צלצולים באוזניים?"},
    {"number": 3, "text": "האם דברים שאתה רואה נראים שונה מהאופן שהם בדרך כלל נראים (בהירים יותר, כהים, גדולים יותר, קטנים יותר או שונים בצורה אחרת כלשהי)?"},
    {"number": 4, "text": "האם היו לך חוויות של טלפתיה (קריאת מחשבות), כוחות על-טבעיים או יכולת לחזות את העתיד?"},
    {"number": 5, "text": "האם הרגשת שאתה לא שולט על הרעיונות או על המחשבות שלך?"},
    {"number": 6, "text": "האם במהלך שיחות אתה מתקשה להבהיר את כוונתך לאנשים אחרים בגלל שאתה נוטה לדבר הרבה או לסטות מהנושא?"},
    {"number": 7, "text": "האם אתה מאמין שאתה מאוד חשוב או שיש לך יכולות לא רגילות?"},
    {"number": 8, "text": "האם אתה מרגיש שאנשים אחרים מביטים עליך או מדברים עליך?"},
    {"number": 9, "text": "האם לפעמים אתה מרגיש תחושות מוזרות על העור או מתחתיו, כאילו חרקים זוחלים עליך?"},
    {"number": 10, "text": "האם לפעמים קורה לך שקולות רחוקים שבאופן רגיל אתה לא מודע להם, פתאום מסיחים את דעתך?"},
    {"number": 11, "text": "האם הייתה לך תחושה כי אדם מסוים או כוח מסוים נמצא סביבך, למרות שלא יכולת לראות אף אחד?"},
    {"number": 12, "text": "האם אתה מודאג לעיתים שמשהו לא בסדר בנפשך?"},
    {"number": 13, "text": "האם קרה לך שהרגשת שאתה לא באמת קיים או שהעולם לא באמת קיים או שאתה בכלל מת?"},
    {"number": 14, "text": "האם קרה לך שהיית מבולבל או לא בטוח האם משהו שחווית היה אמיתי או דמיוני?"},
    {"number": 15, "text": "האם יש לך מחשבות שלדעת אחרים הן לא רגילות או מוזרות?"},
    {"number": 16, "text": "האם אתה מרגיש שחלקים מגופך השתנו בדרך מסוימת או שחלקים מגופך עובדים אחרת מהאופן בו הם עבדו קודם לכן?"},
    {"number": 17, "text": "האם המחשבות שלך, לפעמים, כל כך חזקות עד שאתה כמעט שומע אותן?"},
    {"number": 18, "text": "האם אתה מוצא את עצמך לא בוטח או חשדן כלפי אנשים אחרים?"},
    {"number": 19, "text": "האם ראית דברים לא רגילים כמו הבזקים, להבות, אורות מסנוורים או צורות גיאומטריות?"},
    {"number": 20, "text": "האם היו לך מקרים בהם ראית דברים שאנשים אחרים לא יכולים לראות או לא ראו?"},
    {"number": 21, "text": "האם לפעמים אנשים מתקשים להבין את מה שאתה אומר?"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    Calculate PQ-B score.
    responses: dict mapping item number (int) -> raw score (int, 0 or 1)
               plus f"{item_number}_distress" (str) -> distress rating (int, 1-5)
    Returns dict with total endorsed count, total distress, and interpretation.
    """
    total_endorsed = 0
    total_distress = 0
    item_details = []

    for item in ITEMS:
        num = item["number"]
        endorsed = responses.get(num, 0)
        if endorsed == 1:
            total_endorsed += 1
            distress = responses.get(f"{num}_distress", 0)
            total_distress += distress
            item_details.append({"number": num, "distress": distress})

    results = {
        "total_endorsed": total_endorsed,
        "total_distress": total_distress,
        "endorsed_items": item_details,
        "score_range": "סך פריטים חיוביים 0-21, ציון מצוקה 0-105",
    }

    if total_endorsed >= 8:
        results["severity"] = "סיכון גבוה"
        results["interpretation"] = (
            f"ציון {total_endorsed} מתוך 21 (≥8) – סיכון גבוה. "
            f"ציון מצוקה כולל: {total_distress}. "
            "מומלץ הערכה קלינית מעמיקה."
        )
    elif total_endorsed >= 3:
        results["severity"] = "סיכון בינוני"
        results["interpretation"] = (
            f"ציון {total_endorsed} מתוך 21 (3-7) – סיכון בינוני. "
            f"ציון מצוקה כולל: {total_distress}. "
            "מומלץ מעקב והערכה נוספת."
        )
    else:
        results["severity"] = "סיכון נמוך"
        results["interpretation"] = (
            f"ציון {total_endorsed} מתוך 21 (0-2) – סיכון נמוך. "
            f"ציון מצוקה כולל: {total_distress}."
        )

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
    "has_distress_followup": True,
    "distress_instructions": DISTRESS_INSTRUCTIONS,
    "distress_scale_labels": DISTRESS_SCALE_LABELS,
    "distress_scale_min": 1,
    "distress_scale_max": 5,
}
