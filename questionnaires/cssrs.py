"""
C-SSRS - Columbia Suicide Severity Rating Scale (Screening Version)
סולם קולומביה לדירוג חומרת האובדנות – גרסת סינון
Posner et al. (2011)

CLINICIAN-ADMINISTERED semi-structured interview.
NOT a self-report instrument — must be completed by a trained clinician.

Structure:
  Part A — Suicidal Ideation (items 1-5), branching logic:
    Ask items 1-2 first.
    If BOTH negative → skip to Part B.
    If either is positive → continue with items 3-5.
    If item 1 and/or 2 is positive → rate intensity (I1-I5).
  Intensity — 5 dimensions rated 1-5, for recent period AND lifetime.
  Part B — Suicidal Behavior (items 6-10), assessed for both timeframes.

Response key schema:
  {item_num: 0/1}           — recent period (primary screening)
  {f"{item_num}_l": 0/1}   — lifetime
  {f"{item_num}_count": n} — attempt count, recent (items 6-9)
  {f"{item_num}_count_l": n} — attempt count, lifetime (items 6-9)
  {"I1": 1-5, "I1_l": 1-5, ...} — intensity, recent & lifetime
  {"lethality": 0-5}        — medical outcome for actual attempt
  {"lethality_potential": 0-2} — only if lethality == 0
  {"source": str}           — source of information
  {"months": int}           — reference period in months

Scoring: highest ideation level endorsed (1-5), plus behavior flags.
Posner et al. (2011); Hebrew translation provided by the researcher.
"""

NAME = "סולם קולומביה לדירוג חומרת האובדנות – גרסת סינון (C-SSRS)"
CODE = "C-SSRS"

INSTRUCTIONS = """**ראיון מאבחן — אין להחתים את הנבדק/ת על טופס זה עצמאית**

ה-C-SSRS הוא ראיון חצי-מובנה שנועד לשימוש על ידי מאבחן מוסמך בלבד.

**עקרונות הניהול:**
- השאלות הן **הצעות לגישוש בלבד** — ניתן להתאים את הניסוח כל עוד מוערכים כל סוגי המחשבות וההתנהגויות
- מקורות מידע מקובלים: ראיון עם הנבדק/ת, בני/ות משפחה, גורמים נוספים — ניתן לשלב מקורות
- שיח ישיר על אובדנות אינו מגביר את הסיכון (Gould et al., 2005)
- ניתן להסיק כוונה קלינית מהתנהגות גם אם הנבדק/ת שולל/ת אותה

**זרימת הראיון:**
1. שאל/י שאלות 1-2 תחילה
2. אם שתיהן שליליות → עבור/י לחלק ב' (התנהגות אובדנית)
3. אם אחת חיובית → המשך/י לשאלות 3-4-5
4. אם שאלה 1 ו/או 2 חיובית → הערך/י עוצמת מחשבות
5. הערך/י תמיד את כל סוגי ההתנהגות האובדנית, ללא קשר לתשובות החלק א'
"""

SCALE_LABELS = {
    0: "לא",
    1: "כן",
}

ITEMS = [
    # ── Part A: Suicidal Ideation ──────────────────────────────────────
    {
        "number": 1,
        "text": "הרצון להיות מת/ה",
        "section": "מחשבות אובדניות",
        "guidance": (
            "**הגדרה:** הנבדק/ת מאשר/ת קיום מחשבות על הרצון למות או לא להיות יותר בין "
            "החיים, או על המשאלה להירדם ולא להתעורר עוד.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם היית רוצה להיות מת/ה?\n"
            "• האם את/ה מייחל/ת להירדם ולא להתעורר עוד?"
        ),
    },
    {
        "number": 2,
        "text": "מחשבות אובדניות פעילות בלתי ספציפיות",
        "section": "מחשבות אובדניות",
        "guidance": (
            "**הגדרה:** מחשבות כלליות ובלתי-ספציפיות על הרצון לסיים את החיים/להתאבד "
            "(כגון: 'חשבתי להתאבד'), ללא שיטה, כוונה או תכנית.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם אכן יש לך מחשבות על התאבדות?\n\n"
            "**⚠ לאחר שאלה זו:** אם גם שאלה 1 וגם שאלה 2 שליליות → עבור/י לחלק ב' (התנהגות). "
            "אם אחת חיובית → שאל/י שאלות 3-5."
        ),
    },
    {
        "number": 3,
        "text": "מחשבות אובדניות פעילות עם שיטה כלשהי (ללא תכנית)",
        "section": "מחשבות אובדניות",
        "guidance": (
            "**הגדרה:** הנבדק/ת חשב/ה על שיטה אחת לפחות, אך **ללא** תכנית מפורטת "
            "(מקום, זמן, אמצעי). כולל: 'חשבתי על נטילת מנת יתר, אך מעולם לא הייתה לי תכנית ספציפית'.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם חשבת כיצד היית יכול/ה לעשות זאת?\n"
            "• [אם כן — נא לתאר]"
        ),
    },
    {
        "number": 4,
        "text": "מחשבות אובדניות פעילות עם כוונה מסוימת לפעול (ללא תכנית ספציפית)",
        "section": "מחשבות אובדניות",
        "guidance": (
            "**הגדרה:** מחשבות פעילות על התאבדות + כוונה מסוימת לפעול, בניגוד ל: "
            "'יש לי מחשבות כאלה, אך בפירוש לא אעשה כלום על פיהן'.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם יש לך מחשבות כאלה וכוונה כלשהי לפעול על פיהן?"
        ),
    },
    {
        "number": 5,
        "text": "מחשבות אובדניות פעילות עם תכנית וכוונה מוגדרות",
        "section": "מחשבות אובדניות",
        "guidance": (
            "**הגדרה:** מחשבות התאבדות עם פרטי תכנית מעובדים (חלקית או מלאה). "
            "לנבדק/ת כוונה מסוימת להוציאה אל הפועל.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם התחלת לעבד או כבר עיבדת את הפרטים של אופן ההתאבדות?\n"
            "• האם בכוונתך להוציא תכנית זו אל הפועל?"
        ),
    },
    # ── Part B: Suicidal Behavior ──────────────────────────────────────
    {
        "number": 6,
        "text": "ניסיון אובדני בפועל",
        "section": "התנהגות אובדנית",
        "guidance": (
            "**הגדרה:** פעולה עם פוטנציאל פגיעה עצמית שננקטה תוך **רצון מסוים** (אפילו חלקי) "
            "למות. אין חובה שיהיו נזק או פגיעה — מספיק הפוטנציאל.\n\n"
            "**דגשים קליניים:**\n"
            "• הכוונה אינה חייבת להיות 100% — גם 'רצון חלקי' נחשב\n"
            "• **ניתן להסיק כוונה קלינית** מהתנהגות גם אם הנבדק/ת שולל/ת אותה\n"
            "• יש לשאול מדוע בוצעה הפעולה — להבחין מ-NSSI (פגיעה לא-אובדנית)\n\n"
            "**שאלות מוצעות:**\n"
            "• האם ביצעת ניסיון התאבדות? האם עשית משהו במטרה לפגוע בעצמך?\n"
            "• האם עשית משהו מסוכן שיכול היה לגרום למותך? מה עשית?\n"
            "• האם רצית למות (אפילו קצת) כאשר ____?\n"
            "• או עשית זאת מסיבות אחרות — להקל על מתח, לזכות באהדה?"
        ),
    },
    {
        "number": 7,
        "text": "ניסיון שסוכל",
        "section": "התנהגות אובדנית",
        "guidance": (
            "**הגדרה:** ניסיון אובדני שהופסק על ידי גורם **חיצוני** (לא על ידי האדם עצמו) "
            "בתחילת פעולה של פגיעה עצמית.\n\n"
            "**דוגמאות:** גלולות ביד אך נמנע מלבלוע; אקדח מכוון לעצמו אך ניטל; עומד לקפוץ אך תפסו.\n\n"
            "**הבדל מניסיון שנזנח:** כאן גורם חיצוני עצר — לא האדם עצמו.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם קרה שהתחלת לבצע משהו כדי לשים קץ לחייך, אך מישהו/משהו עצר בעדך?"
        ),
    },
    {
        "number": 8,
        "text": "ניסיון שנזנח",
        "section": "התנהגות אובדנית",
        "guidance": (
            "**הגדרה:** ניסיון שהאדם **עצמו** הפסיק בטרם ביצע פעולה של פגיעה עצמית "
            "(בניגוד לניסיון שסוכל).\n\n"
            "**שאלות מוצעות:**\n"
            "• האם קרה שהתחלת לבצע משהו כדי לנסות לשים קץ לחייך, אך עצרת בעצמך?"
        ),
    },
    {
        "number": 9,
        "text": "פעולות הכנה או התנהגות מכינה",
        "section": "התנהגות אובדנית",
        "guidance": (
            "**הגדרה:** הכנות לקראת ביצוע ניסיון — כל דבר מעבר לביטויים מילוליים ומחשבות: "
            "עיבוד שיטה, איסוף אמצעים, כתיבת מכתב פרידה, חלוקת טובין.\n\n"
            "**חשוב:** יש למנות רק פעולות **שלא הובילו** לניסיונות בפועל/שסוכלו/שנזנחו.\n\n"
            "**שאלות מוצעות:**\n"
            "• האם נקטת צעדים לקראת ביצוע ניסיון? האם איספת כדורים, קנית אקדח, "
            "מסרת דברי ערך, כתבת מכתב פרידה?"
        ),
    },
    {
        "number": 10,
        "text": "פגיעה עצמית שאיננה אובדנית (NSSI)",
        "section": "התנהגות אובדנית",
        "guidance": (
            "**הגדרה:** פגיעה עצמית (חיתוך, כוויה, שריטה וכד') **ללא** כל כוונה אובדנית.\n\n"
            "**חשוב:** לשאול ולתאר בנפרד — NSSI מהווה גורם סיכון קליני אך מוגדר שונה "
            "מניסיון אובדני."
        ),
    },
]

REVERSED_ITEMS = []

INTENSITY_ITEMS = [
    {
        "number": "I1",
        "text": "שכיחות — כמה פעמים היו לך המחשבות?",
        "guidance": "כמה פעמים בשבוע חזרו המחשבות האובדניות החמורות ביותר?",
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
        "text": "משך — כמה זמן נמשכות המחשבות כשהן עולות?",
        "guidance": "כמה זמן כל אפיזודה של מחשבות אובדניות?",
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
        "text": "יכולת שליטה — האם יכולת להפסיק לחשוב על זה?",
        "guidance": "האם יכול/ה לשלוט במחשבות ולהפסיק אותן ברצון?",
        "labels": {
            1: "בקלות — יכול/ה להפסיק לחשוב בנקל",
            2: "עם מאמץ מסוים",
            3: "בקושי",
            4: "בקושי רב",
            5: "לא יכול/ה לשלוט — המחשבות השתלטו",
        },
    },
    {
        "number": "I4",
        "text": "גורמים מרתיעים — האם היו דברים שמנעו ממך לפעול?",
        "guidance": "האם קיימים דברים/אנשים (משפחה, דת, פחד מכאב) שמנעו מהאדם לפעול לפי המחשבות?",
        "labels": {
            1: "גורמים מרתיעים מנעו בבירור",
            2: "גורמים מרתיעים ככל הנראה מנעו",
            3: "לא בטוח/ה אם גורמים מרתיעים מנעו",
            4: "גורמים מרתיעים ככל הנראה לא מנעו",
            5: "גורמים מרתיעים בהחלט לא מנעו",
        },
    },
    {
        "number": "I5",
        "text": "סיבות — מדוע רצית להתאבד?",
        "guidance": (
            "מחקר מצביע על כך שרצון למות כדי לסיים כאב מהווה סיכון גבוה יותר "
            "לנקיטת מעשים אובדניים."
        ),
        "labels": {
            1: "כדי למשוך תשומת לב, להתנקם, לעורר תגובה מאחרים",
            2: "דרך לסיים/להפסיק את הכאב (לא ראה/תה דרך אחרת)",
            3: "שילוב של 1 ו-2",
            4: "בעיקר כדי לסיים את הכאב",
            5: "לגמרי כדי לסיים את הכאב ולהיעלם",
        },
    },
]

# Medical lethality for actual attempts (item 6)
LETHALITY_LABELS = {
    0: "0 — ללא נזק גופני / נזק מזערי (כגון שריטות שטחיות)",
    1: "1 — נזק גופני מועט (דיבור ישנוני, כוויות דרגה א', דימום קל, נקעים)",
    2: "2 — נזק גופני בינוני — דרוש השגחה רפואית",
    3: "3 — נזק בינוני-חמור — דרוש אשפוז וכנראה טיפול נמרץ",
    4: "4 — נזק גופני חמור — דרוש אשפוז ביחידה לטיפול נמרץ",
    5: "5 — מוות",
}

# Lethality potential (only when medical lethality = 0)
LETHALITY_POTENTIAL_LABELS = {
    0: "0 — אין סבירות כי ההתנהגות תגרום לפגיעה",
    1: "1 — סביר שתגרום לפגיעה, אך כנראה לא למוות",
    2: "2 — סביר שתגרום למוות למרות עזרה רפואית זמינה",
}


def score(responses):
    """
    Calculate C-SSRS screening score.
    Handles both simple format (integer keys only) and extended clinician format
    (with _l lifetime keys, _count keys, lethality, source, months).

    Primary risk assessment is based on the RECENT period.
    Lifetime data is stored alongside for clinical completeness.
    """
    # ── Ideation: recent period ──────────────────────────────────────
    ideation_level = 0
    for i in range(5, 0, -1):
        if responses.get(i, 0) == 1:
            ideation_level = i
            break

    # ── Ideation: lifetime ───────────────────────────────────────────
    ideation_level_lifetime = 0
    for i in range(5, 0, -1):
        if responses.get(f"{i}_l", 0) == 1:
            ideation_level_lifetime = i
            break

    # ── Behavior: recent ────────────────────────────────────────────
    actual_attempt = responses.get(6, 0) == 1
    interrupted_attempt = responses.get(7, 0) == 1
    aborted_attempt = responses.get(8, 0) == 1
    preparatory_behavior = responses.get(9, 0) == 1
    non_suicidal_self_injury = responses.get(10, 0) == 1

    # ── Behavior: lifetime ───────────────────────────────────────────
    actual_attempt_l = responses.get("6_l", 0) == 1
    interrupted_attempt_l = responses.get("7_l", 0) == 1
    aborted_attempt_l = responses.get("8_l", 0) == 1
    preparatory_behavior_l = responses.get("9_l", 0) == 1
    nssi_l = responses.get("10_l", 0) == 1

    any_behavior_recent = actual_attempt or interrupted_attempt or aborted_attempt or preparatory_behavior
    any_behavior_lifetime = actual_attempt_l or interrupted_attempt_l or aborted_attempt_l or preparatory_behavior_l

    # ── Attempt counts ───────────────────────────────────────────────
    attempt_count_recent = responses.get("6_count") or 0
    attempt_count_lifetime = responses.get("6_count_l") or 0

    # ── Lethality ────────────────────────────────────────────────────
    lethality = responses.get("lethality")
    lethality_potential = responses.get("lethality_potential")

    # ── Context ──────────────────────────────────────────────────────
    source = responses.get("source", "")
    months = responses.get("months", 1)

    ideation_labels = {
        0: "לא דווח על מחשבות אובדניות",
        1: "רצון להיות מת/ה",
        2: "מחשבות אובדניות פעילות בלתי ספציפיות",
        3: "מחשבות אובדניות פעילות עם שיטה כלשהי",
        4: "מחשבות אובדניות פעילות עם כוונה לפעול",
        5: "מחשבות אובדניות פעילות עם תכנית וכוונה מוגדרות",
    }

    results = {
        # ── Recent period (primary risk) ──
        "ideation_level": ideation_level,
        "ideation_description": ideation_labels[ideation_level],
        "actual_attempt": actual_attempt,
        "interrupted_attempt": interrupted_attempt,
        "aborted_attempt": aborted_attempt,
        "preparatory_behavior": preparatory_behavior,
        "non_suicidal_self_injury": non_suicidal_self_injury,
        # ── Lifetime ──
        "ideation_level_lifetime": ideation_level_lifetime,
        "ideation_description_lifetime": ideation_labels[ideation_level_lifetime],
        "actual_attempt_lifetime": actual_attempt_l,
        "interrupted_attempt_lifetime": interrupted_attempt_l,
        "aborted_attempt_lifetime": aborted_attempt_l,
        "preparatory_lifetime": preparatory_behavior_l,
        "nssi_lifetime": nssi_l,
        # ── Counts ──
        "attempt_count_recent": attempt_count_recent,
        "attempt_count_lifetime": attempt_count_lifetime,
        # ── Lethality ──
        "lethality": lethality,
        "lethality_potential": lethality_potential,
        # ── Context ──
        "source": source,
        "months": months,
        "score_range": "רמת חשיבה: 0-5 | התנהגות: כן/לא",
    }

    # ── Severity (based on recent period) ───────────────────────────
    if actual_attempt:
        results["severity"] = "קריטי"
        results["interpretation"] = "דווח על ניסיון אובדני בפועל בתקופה האחרונה — נדרשת התערבות מיידית"
    elif ideation_level >= 4 or preparatory_behavior:
        results["severity"] = "חמור"
        results["interpretation"] = "מחשבות אובדניות ברמת חומרה גבוהה ו/או פעולות הכנה — נדרשת הערכה קלינית דחופה"
    elif ideation_level >= 3 or interrupted_attempt or aborted_attempt:
        results["severity"] = "בינוני-חמור"
        results["interpretation"] = "מחשבות אובדניות עם שיטה ו/או ניסיונות שסוכלו/נזנחו — נדרשת הערכה קלינית"
    elif ideation_level >= 1:
        results["severity"] = "בינוני"
        results["interpretation"] = "דווח על מחשבות אובדניות — יש לבחון בראיון קליני"
    else:
        results["severity"] = "ללא"
        results["interpretation"] = "לא דווח על מחשבות או התנהגויות אובדניות בתקופת ההערכה"

    # Add lifetime severity note if lifetime is more severe than recent
    if ideation_level_lifetime > ideation_level or any_behavior_lifetime:
        results["lifetime_note"] = (
            f"במהלך החיים: רמת חשיבה {ideation_level_lifetime}/5 — "
            f"{ideation_labels[ideation_level_lifetime]}"
        )

    if non_suicidal_self_injury or nssi_l:
        results["clinical_note"] = "דווח על פגיעה עצמית שאיננה אובדנית (NSSI) — יש לבחון בהקשר קליני"

    # ── Behavior summary (recent) ────────────────────────────────────
    behaviors_recent = []
    if actual_attempt:
        behaviors_recent.append("ניסיון בפועל")
    if interrupted_attempt:
        behaviors_recent.append("ניסיון שסוכל")
    if aborted_attempt:
        behaviors_recent.append("ניסיון שנזנח")
    if preparatory_behavior:
        behaviors_recent.append("פעולות הכנה")
    if non_suicidal_self_injury:
        behaviors_recent.append("NSSI")
    results["behavior_summary"] = ", ".join(behaviors_recent) if behaviors_recent else "לא דווח על התנהגויות אובדניות"

    # ── Behavior summary (lifetime) ──────────────────────────────────
    behaviors_lifetime = []
    if actual_attempt_l:
        behaviors_lifetime.append("ניסיון בפועל")
    if interrupted_attempt_l:
        behaviors_lifetime.append("ניסיון שסוכל")
    if aborted_attempt_l:
        behaviors_lifetime.append("ניסיון שנזנח")
    if preparatory_behavior_l:
        behaviors_lifetime.append("פעולות הכנה")
    if nssi_l:
        behaviors_lifetime.append("NSSI")
    results["behavior_summary_lifetime"] = (
        ", ".join(behaviors_lifetime) if behaviors_lifetime else "לא דווח"
    )

    # ── Lethality description ────────────────────────────────────────
    if lethality is not None:
        leth_labels_clean = {
            0: "ללא נזק / נזק מזערי",
            1: "נזק מועט",
            2: "נזק בינוני",
            3: "נזק בינוני-חמור",
            4: "נזק חמור",
            5: "מוות",
        }
        results["lethality_description"] = leth_labels_clean.get(lethality, str(lethality))
    if lethality_potential is not None:
        pot_labels_clean = {
            0: "אין סבירות לפגיעה",
            1: "סביר — פגיעה אך לא מוות",
            2: "סביר — מוות",
        }
        results["lethality_potential_description"] = pot_labels_clean.get(lethality_potential, str(lethality_potential))

    # ── Intensity ratings ────────────────────────────────────────────
    if ideation_level >= 1:
        intensity = {}
        intensity_total = 0
        for iitem in INTENSITY_ITEMS:
            inum = iitem["number"]
            ival = responses.get(inum, 0)
            if ival:
                intensity[inum] = {
                    "label": iitem["text"].split("—")[0].strip(),
                    "value": ival,
                    "description": iitem["labels"].get(ival, ""),
                }
                intensity_total += ival
        if intensity:
            results["intensity"] = intensity
            results["intensity_total"] = intensity_total

    if ideation_level_lifetime >= 1:
        intensity_l = {}
        intensity_total_l = 0
        for iitem in INTENSITY_ITEMS:
            inum_l = f"{iitem['number']}_l"
            ival_l = responses.get(inum_l, 0)
            if ival_l:
                intensity_l[inum_l] = {
                    "label": iitem["text"].split("—")[0].strip(),
                    "value": ival_l,
                    "description": iitem["labels"].get(ival_l, ""),
                }
                intensity_total_l += ival_l
        if intensity_l:
            results["intensity_lifetime"] = intensity_l
            results["intensity_total_lifetime"] = intensity_total_l

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
    "clinician_mode": True,
    "lethality_labels": LETHALITY_LABELS,
    "lethality_potential_labels": LETHALITY_POTENTIAL_LABELS,
}
