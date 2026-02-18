"""
IRI - Interpersonal Reactivity Index (Empathy)
מדד התגובתיות הבין-אישית (אמפתיה)
Davis (1983)

28 items, Likert 1-5
Scale: 1=מאוד לא אני, 2=לא אני, 3=ניטרלי, 4=אני, 5=מאוד אני
4 subscales (7 items each):
  PT (תפיסת עמדת האחר): 3R,8,11,15R,21,25,28
  FC (פנטזיה): 1,5,7R,12R,16,23,26
  EC (עניין אמפתי): 2,4R,9,14R,18R,20,22
  PD (מצוקה אישית): 6,10,13R,17,19R,24,27
Reversed items: 3,4,7,12,13,14,15,18,19 (score = 6 - raw)
Scoring: Mean of each subscale (range 1-5). No total score.
"""

NAME = "מדד התגובתיות הבין-אישית (IRI)"
CODE = "IRI"

INSTRUCTIONS = """אנא קרא/י את המשפטים שלפניך וסמן לגבי כל היגד עד כמה הוא מתאר את עצמך בסולם 1-5. 1=מאוד לא אני, 5=מאוד אני."""

SCALE_LABELS = {
    1: "1 - מאוד לא אני",
    2: "2 - לא אני",
    3: "3 - ניטרלי",
    4: "4 - אני",
    5: "5 - מאוד אני",
}

ITEMS = [
    {"number": 1, "text": "אני הוזה בהקיץ ומדמיין/ת באופן די קבוע דברים שיכולים לקרות לי"},
    {"number": 2, "text": "לעיתים קרובות אני מתמלא/ת ברגשות של השתתפות וחמלה כלפי אלו שגורלם לא שפר עליהם כשלי"},
    {"number": 3, "text": "לעיתים קשה לי לראות דברים מנקודת מבטו של האחר"},
    {"number": 4, "text": "לעיתים אינני מרגיש/ה צער רב כשלאחרים יש בעיות"},
    {"number": 5, "text": "אני נעשה/ית מעורבת מאוד ברגשותיהן של הדמויות בספר שאני קורא/ת"},
    {"number": 6, "text": "במצבי דאגה אני מרגיש/ה דאגה ואי שקט"},
    {"number": 7, "text": "לרוב אני אובייקטיבי/ת כשאני צופה בסרט או בהצגה, ולא לעיתים קרובות אני נתפס/ת כולי למתרחש"},
    {"number": 8, "text": "אני מנסה לראות את צדו של כל אחד במחלוקת לפני שאני מגיע להחלטה"},
    {"number": 9, "text": "כשאני רואה מישהו מנוצל, אני מרגיש/ה מין צורך לגונן עליו"},
    {"number": 10, "text": "כשאני במרכזה של סיטואציה רגשית מאוד, אני חש/ה לפעמים חוסר אונים"},
    {"number": 11, "text": "לעיתים אני מנסה להיטיב להבין את חברי בכך שאני מדמיין/ת איך הדברים נראים מנקודת מבטם"},
    {"number": 12, "text": "מעורבות יתרה בספר טוב או בסרט היא חוויה די נדירה עבורי"},
    {"number": 13, "text": "כשאני רואה מישהו נפגע אני נוטה להישאר רגוע"},
    {"number": 14, "text": "צרותיהם של אחרים אינן מטרידות אותי מאד בדרך כלל"},
    {"number": 15, "text": "אם אני משוכנע/ת בצדקתי בדבר מה, אינני מבזבז/ת זמן רב בהאזנה לטיעוניהם של אחרים"},
    {"number": 16, "text": "אחרי סרט או הצגה שראיתי הרגשתי כאילו אני אחת הדמויות"},
    {"number": 17, "text": "סיטואציה טעונה במתח רגשי מעוררת בי חשש"},
    {"number": 18, "text": "כשאני רואה מישהו שמתייחסים אליו בחוסר הגינות, קורה שאני לא מרגיש/ה הרבה רחמים עליו"},
    {"number": 19, "text": "בדרך כלל אני יעיל/ה מאוד בטיפול במצבי חירום"},
    {"number": 20, "text": "דברים שמתרחשים סביבי נוגעים תכופות ללבי"},
    {"number": 21, "text": "אני מאמין/ה כי יש שני צדדים לכל בעיה ואני מנסה לראות את שניהם"},
    {"number": 22, "text": "הייתי מתאר/ת את עצמי כרך/ת-לב למדי"},
    {"number": 23, "text": "כשאני רואה סרט טוב אני יכול/ה בקלות רבה לשים עצמי במקומה של הדמות המרכזית"},
    {"number": 24, "text": "אני נוטה לאבד שליטה במצבי חירום"},
    {"number": 25, "text": "כשאני כועס/ת על מישהו, אני מנסה בדרך-כלל \"לשים עצמי בנעליו\" לרגע"},
    {"number": 26, "text": "כשאני קורא/ת ספור מעניין או רומן, אני מדמיין/ת איך הייתי מרגיש/ה אילו אירועי הסיפור היו קורים לי"},
    {"number": 27, "text": "כשאני רואה מישהו במצב חירום, זקוק נואשות לעזרה, אני מאבד/ת את עשתונותיי"},
    {"number": 28, "text": "לפני שאני מבקר/ת מישהו אני מנסה לדמיין איך הייתי מרגיש/ה אילו הייתי במקומו"},
]

REVERSED_ITEMS = [3, 4, 7, 12, 13, 14, 15, 18, 19]

SUBSCALES = {
    "PT": {"name": "תפיסת עמדת האחר (Perspective Taking)", "items": [3, 8, 11, 15, 21, 25, 28]},
    "FC": {"name": "פנטזיה (Fantasy)", "items": [1, 5, 7, 12, 16, 23, 26]},
    "EC": {"name": "עניין אמפתי (Empathic Concern)", "items": [2, 4, 9, 14, 18, 20, 22]},
    "PD": {"name": "מצוקה אישית (Personal Distress)", "items": [6, 10, 13, 17, 19, 24, 27]},
}


def score(responses):
    """
    Calculate IRI scores.
    responses: dict mapping item number (int) -> raw score (int, 1-5)
    Returns dict with subscale means and interpretation.
    """
    # Reverse score where needed
    scored = {}
    for item_num, raw in responses.items():
        if item_num in REVERSED_ITEMS:
            scored[item_num] = 6 - raw
        else:
            scored[item_num] = raw

    results = {
        "score_range": "ממוצע 1-5 לכל תת-סולם",
    }

    for code, info in SUBSCALES.items():
        item_values = [scored[i] for i in info["items"] if i in scored]
        if item_values:
            mean = round(sum(item_values) / len(item_values), 2)
        else:
            mean = 0
        results[f"{code}_mean"] = mean
        results[f"{code}_name"] = info["name"]

        # Interpretation per subscale
        if mean >= 4:
            level = "גבוה"
        elif mean >= 3:
            level = "בינוני-גבוה"
        elif mean >= 2:
            level = "בינוני-נמוך"
        else:
            level = "נמוך"
        results[f"{code}_level"] = level
        results[f"{code}_interpretation"] = f"{info['name']}: ממוצע {mean} – רמה {level}"

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
