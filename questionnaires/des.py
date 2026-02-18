"""
DES - Dissociative Experiences Scale
סולם חוויות דיסוציאטיביות
Bernstein & Putnam (1986), Hebrew: Somer, Dolgin & Saadon (2001)

28 items, scale 0-100 (increments of 10)
No reversed items
Scoring: Mean of all items (range 0-100)
Cutoff >= 30 suggests pathological dissociation
"""

NAME = "סולם חוויות דיסוציאטיביות (DES)"
CODE = "DES"

INSTRUCTIONS = """שאלון זה מורכב מעשרים ושמונה שאלות העוסקות בחוויות שעשויות להיות לך בחיי היום-יום.
אנא קבע באיזו מידה החוויה המתוארת בשאלה ישימה לגביך וסמן את האחוז מן הזמן שבו יש לך חוויה זו.
חשוב שתשובותיך ישקפו חוויות שלא תחת השפעת אלכוהול או סמים."""

SCALE_LABELS = {
    0: "0% - אף פעם",
    10: "10%",
    20: "20%",
    30: "30%",
    40: "40%",
    50: "50%",
    60: "60%",
    70: "70%",
    80: "80%",
    90: "90%",
    100: "100% - תמיד",
}

ITEMS = [
    {"number": 1, "text": "נוהגים או נוסעים במכונית או באוטובוס ולפתע מבינים שלא זוכרים מה קרה במהלך כל הנסיעה או חלקה"},
    {"number": 2, "text": "מקשיבים למישהו מדבר ולפתע מבינים שלא שמעו חלק ממה שנאמר או כל מה שנאמר"},
    {"number": 3, "text": "מוצאים את עצמם במקום כלשהו, ללא שמץ של מושג כיצד הגיעו לשם"},
    {"number": 4, "text": "מוצאים את עצמם לבושים בבגדים שאינם זוכרים שלבשו"},
    {"number": 5, "text": "מוצאים דברים חדשים בין חפציהם, שאינם זוכרים שקנו"},
    {"number": 6, "text": "ניגשים אליהם אנשים שאינם מכירים וקוראים להם בשם אחר, או מתעקשים שהכירו אותם בעבר"},
    {"number": 7, "text": "חשים כאילו עומדים ליד עצמם או מסתכלים על עצמם עושים פעולה כלשהי"},
    {"number": 8, "text": "נאמר להם כי לפעמים אינם מזהים חברים או בני משפחה"},
    {"number": 9, "text": "אינם זוכרים אירועים חשובים בחייהם (למשל, חתונה או סיום לימודים)"},
    {"number": 10, "text": "מאשימים אותם בשקר, כשהם אינם חושבים ששיקרו"},
    {"number": 11, "text": "מסתכלים במראה ואינם מזהים את עצמם"},
    {"number": 12, "text": "חשים שאנשים אחרים, חפצים, והעולם שסביבם אינם אמיתיים"},
    {"number": 13, "text": "חשים כי נדמה שגופם אינו שייך להם"},
    {"number": 14, "text": "נזכרים באירוע מן העבר בצורה כל כך מוחשית, שמרגישים כאילו חווים אותו מחדש"},
    {"number": 15, "text": "לא בטוחים האם דברים שהם זוכרים שקרו, אכן קרו, או שרק חלמו אותם"},
    {"number": 16, "text": "נמצאים במקום מוכר אך מרגישים שהוא זר ולא מוכר"},
    {"number": 17, "text": "צופים בטלוויזיה או בסרט ונעשים כל כך שקועים בסיפור עד שאינם מודעים לאירועים סביבם"},
    {"number": 18, "text": "נעשים כל כך מעורבים בפנטזיה או חלום בהקיץ, שחשים כאילו זה קורה במציאות"},
    {"number": 19, "text": "יכולים להתעלם מכאב"},
    {"number": 20, "text": "יושבים ובוהים בחלל, לא חושבים על דבר, ואינם מודעים לזמן שעובר"},
    {"number": 21, "text": "כשהם לבד מדברים בקול רם אל עצמם"},
    {"number": 22, "text": "מתנהגים במצב אחד כל כך שונה בהשוואה למצב אחר, שמרגישים כמעט כאילו שני אנשים נפרדים"},
    {"number": 23, "text": "במצבים מסוימים מסוגלים לעשות דברים בקלות וספונטניות מדהימות, למרות שבדרך כלל קשים עבורם"},
    {"number": 24, "text": "אינם בטוחים אם עשו משהו או שרק חשבו על לעשותו"},
    {"number": 25, "text": "מוצאים עדויות לכך שעשו דברים שאינם זוכרים שעשו"},
    {"number": 26, "text": "מוצאים כתבים, ציורים או פתקים שבהכרח הם עשו, אך אינם זוכרים שעשו"},
    {"number": 27, "text": "שומעים קולות בתוך ראשם שאומרים להם לעשות דברים או מעירים על דברים שעושים"},
    {"number": 28, "text": "חשים כאילו מסתכלים על העולם דרך ערפל, כך שאנשים וחפצים נדמים כרחוקים או לא ברורים"},
]

REVERSED_ITEMS = []


def score(responses):
    """
    Calculate DES score.
    responses: dict mapping item number (int) -> raw score (int, 0-100 in increments of 10)
    Returns dict with mean score and interpretation.
    """
    values = list(responses.values())
    total_mean = round(sum(values) / len(values), 1) if values else 0

    results = {
        "total_mean": total_mean,
        "score_range": "ממוצע 0-100% (אחוז הזמן בו מתרחשת החוויה)",
    }

    if total_mean >= 30:
        results["severity"] = "חמור"
        results["interpretation"] = f"ציון ממוצע {total_mean}% (≥30%) – מצביע על רמה גבוהה של חוויות דיסוציאטיביות. יש לבחון בראיון קליני"
    elif total_mean >= 20:
        results["severity"] = "בינוני"
        results["interpretation"] = f"ציון ממוצע {total_mean}% – רמה בינונית של חוויות דיסוציאטיביות. מומלץ המשך הערכה"
    elif total_mean >= 10:
        results["severity"] = "קל"
        results["interpretation"] = f"ציון ממוצע {total_mean}% – רמה קלה של חוויות דיסוציאטיביות"
    else:
        results["severity"] = "נמוך"
        results["interpretation"] = f"ציון ממוצע {total_mean}% – רמה נמוכה של חוויות דיסוציאטיביות"

    # Flag high-severity items (items associated with pathological dissociation)
    pathological_items = [3, 4, 5, 6, 8, 11, 13, 25, 26, 27]
    high_path = [n for n in pathological_items if responses.get(n, 0) >= 40]
    if high_path:
        results["clinical_note"] = f"פריטים פתולוגיים עם ציון גבוה (≥40%): {len(high_path)} מתוך {len(pathological_items)} – מומלץ להעמיק בראיון קליני"

    return results


questionnaire = {
    "name": NAME,
    "code": CODE,
    "instructions": INSTRUCTIONS,
    "scale_labels": SCALE_LABELS,
    "items": ITEMS,
    "reversed_items": REVERSED_ITEMS,
    "scale_min": 0,
    "scale_max": 100,
    "score": score,
}
