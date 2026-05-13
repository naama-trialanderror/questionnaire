import csv
import io
import json
import os
from datetime import datetime
from glob import glob

import streamlit as st
from fpdf import FPDF

from questionnaires import ALL_QUESTIONNAIRES

# --- Page config ---
st.set_page_config(
    page_title="שאלונים לדיווח עצמי",
    page_icon="📋",
    layout="centered",
    menu_items={},
)

# --- Modern RTL CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

    /* ── Base ── */
    .stApp {
        font-family: 'Rubik', 'Segoe UI', Tahoma, sans-serif;
    }
    .stApp, .stMarkdown, .stRadio, .stButton, .stAlert,
    .stTextInput, .stMultiSelect, .stSelectbox, .stCheckbox {
        direction: rtl;
        text-align: right;
    }
    .stRadio > div,
    .stRadio > div[role="radiogroup"],
    .stRadio > div[role="radiogroup"] label {
        direction: rtl;
        text-align: right;
    }
    section[data-testid="stSidebar"],
    [data-testid="stMetric"] {
        direction: rtl;
        text-align: right;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header {visibility: hidden;}

    /* ── Typography ── */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #1a1a2e !important;
    }
    h2 {
        font-weight: 600 !important;
        color: #16213e !important;
    }
    h3 {
        font-weight: 500 !important;
        color: #0f3460 !important;
    }

    /* ── Client questionnaire items ── */
    .q-item {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        background: #fafbfc;
        border-right: 4px solid #6c63ff;
        transition: box-shadow 0.2s;
    }
    .q-item:hover {
        box-shadow: 0 2px 12px rgba(108, 99, 255, 0.08);
    }
    .item-text {
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
        font-weight: 500;
        color: #1a1a2e;
        line-height: 1.7;
    }
    /* Legacy alias */
    .item-container {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        background: #fafbfc;
        border-right: 4px solid #6c63ff;
    }

    /* ── Progress bar ── */
    .q-progress-wrap {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1.2rem;
    }
    .q-progress-bar {
        flex: 1;
        height: 6px;
        background: #e8e8f0;
        border-radius: 3px;
        overflow: hidden;
    }
    .q-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #6c63ff, #a78bfa);
        border-radius: 3px;
        transition: width 0.4s ease;
    }
    .q-progress-text {
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
        white-space: nowrap;
    }

    /* ── Scale legend ── */
    .scale-legend {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.8rem 0 1rem 0;
        direction: rtl;
    }
    .scale-chip {
        background: #f0f0f8;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.82rem;
        color: #444;
        white-space: nowrap;
    }

    /* ── Dashboard result cards ── */
    .results-box {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #eef2ff, #f0f4ff);
        border: 1px solid #c7d2fe;
        margin: 0.8rem 0;
    }
    .warning-box {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #fef3f2, #fef0ee);
        border: 1px solid #fca5a5;
        margin: 0.8rem 0;
    }
    .severe-box {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #fde8e8, #fce4ec);
        border: 1px solid #e57373;
        margin: 0.8rem 0;
    }

    /* ── Thank you screen ── */
    .thank-you {
        text-align: center;
        padding: 4rem 1rem;
    }
    .thank-you h1 {
        font-size: 2.5rem;
        color: #6c63ff !important;
        font-weight: 700 !important;
    }
    .thank-you p {
        font-size: 1.1rem;
        color: #555;
    }

    /* ── Dashboard visual item rows ── */
    .subscale-header {
        padding: 0.55rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.92rem;
        margin: 1.2rem 0 0.4rem 0;
        color: #fff;
        letter-spacing: 0.01em;
    }
    .item-row {
        display: flex;
        align-items: center;
        padding: 0.45rem 0.8rem;
        margin: 2px 0;
        border-radius: 6px;
        gap: 0.5rem;
        transition: background 0.15s;
    }
    .item-row:hover {
        filter: brightness(0.97);
    }
    .item-row .item-num {
        min-width: 2rem;
        font-weight: 600;
        color: #666;
        font-size: 0.85rem;
    }
    .item-row .item-txt {
        flex: 1;
        font-size: 0.88rem;
        color: #333;
        line-height: 1.5;
    }
    .item-row .item-val {
        min-width: 2.5rem;
        text-align: center;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.85rem;
    }
    .item-row .item-bar {
        width: 70px;
        height: 6px;
        background: #e8e8f0;
        border-radius: 3px;
        overflow: hidden;
    }
    .item-row .item-bar-fill {
        height: 100%;
        border-radius: 3px;
    }
    .item-rev-tag {
        font-size: 0.65rem;
        background: #fef3c7;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        color: #92400e;
        font-weight: 500;
    }
    .item-high {
        background-color: #fef2f2;
    }
    .item-normal {
        background-color: #fafbfc;
    }

    /* ── Setup screen ── */
    .setup-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .setup-header h1 {
        font-size: 2rem !important;
        margin-bottom: 0.2rem !important;
    }
    .setup-header p {
        color: #888;
        font-size: 0.95rem;
    }

    /* ── Metric cards ── */
    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }

    /* ── Buttons ── */
    .stButton > button[kind="primary"] {
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }
    .stButton > button {
        border-radius: 10px !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* ── Dividers ── */
    hr {
        border: none !important;
        height: 1px !important;
        background: #e8e8f0 !important;
        margin: 1.5rem 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Scroll-to-top JS (fires on every rerun) ---
st.html('<script>parent.document.querySelector("section.main").scrollTo(0, 0);</script>')

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
try:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    _CAN_SAVE_FILES = True
except OSError:
    _CAN_SAVE_FILES = False

# --- Session state defaults ---
if "screen" not in st.session_state:
    st.session_state.screen = "setup"
if "client_number" not in st.session_state:
    st.session_state.client_number = ""
if "selected_questionnaires" not in st.session_state:
    st.session_state.selected_questionnaires = []
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "all_responses" not in st.session_state:
    st.session_state.all_responses = {}
if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = []


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def save_session(client_number, all_responses):
    """Build session data, store in session state, optionally save to disk."""
    session_data = {
        "client_number": client_number,
        "timestamp": datetime.now().isoformat(),
        "questionnaires": {},
    }

    for q_key, responses in all_responses.items():
        q = ALL_QUESTIONNAIRES[q_key]
        results = q["score"](responses)
        session_data["questionnaires"][q["code"]] = {
            "name": q["name"],
            "raw_responses": {str(k): v for k, v in responses.items()},
            "results": results,
        }

    # Always store in session state (works everywhere including cloud)
    st.session_state.completed_sessions.append(session_data)

    # Try to save to disk (works locally / Docker, silently skipped on cloud)
    if _CAN_SAVE_FILES:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_number}_{timestamp}.json"
            filepath = os.path.join(RESULTS_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    return session_data


def load_all_sessions():
    """Load sessions from disk + session state (deduped by timestamp)."""
    sessions = []
    seen_timestamps = set()

    # Load from disk (local / Docker)
    if _CAN_SAVE_FILES:
        for filepath in sorted(glob(os.path.join(RESULTS_DIR, "*.json")), reverse=True):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["_filepath"] = filepath
                    data["_filename"] = os.path.basename(filepath)
                    sessions.append(data)
                    seen_timestamps.add(data.get("timestamp", ""))
            except (json.JSONDecodeError, OSError):
                pass

    # Add in-memory sessions (cloud mode or current session)
    for s in reversed(st.session_state.get("completed_sessions", [])):
        if s.get("timestamp", "") not in seen_timestamps:
            sessions.insert(0, s)
            seen_timestamps.add(s.get("timestamp", ""))

    return sessions


def render_questionnaire_client(q, q_key):
    """Render questionnaire for client — code only, NO scores, NO reversed markers."""
    # Show only code letters to keep answering unbiased
    st.markdown(f"### {q['code']}")
    st.markdown(f"{q['instructions']}")

    # Show scale legend as compact chips
    if q["scale_labels"]:
        chips = " ".join(
            f'<span class="scale-chip"><b>{val}</b> = {q["scale_labels"][val]}</span>'
            for val in range(q["scale_min"], q["scale_max"] + 1)
            if val in q["scale_labels"]
        )
        st.markdown(f'<div class="scale-legend">{chips}</div>', unsafe_allow_html=True)

    st.markdown("---")

    responses = {}
    all_answered = True
    current_section = None

    for item in q["items"]:
        num = item["number"]

        # Show section header if item has one (e.g., C-SSRS)
        if "section" in item and item["section"] != current_section:
            current_section = item["section"]
            st.markdown(f"### {current_section}")

        st.markdown(
            f'<div class="q-item">'
            f'<div class="item-text">{num}. {item["text"]}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        options_range = list(range(q["scale_min"], q["scale_max"] + 1))

        # Use item-specific alt_scale, then item labels, then questionnaire scale_labels
        if "alt_scale" in item:
            alt = item["alt_scale"]
            format_func = lambda x, alt=alt: f"{x} - {alt[x]}" if x in alt else str(x)
        elif "labels" in item:
            labels = item["labels"]
            format_func = lambda x, lb=labels: f"{x} - {lb[x]}" if x in lb else str(x)
        elif q["scale_labels"]:
            sl = q["scale_labels"]
            format_func = lambda x, sl=sl: f"{x} - {sl[x]}" if x in sl else str(x)
        else:
            format_func = str

        selected = st.radio(
            label=f"פריט {num}",
            options=options_range,
            format_func=format_func,
            key=f"client_{q_key}_{num}",
            index=None,
            label_visibility="collapsed",
        )

        if selected is not None:
            responses[num] = selected
        else:
            all_answered = False

        # PQ-B: show distress followup if endorsed
        if q.get("has_distress_followup") and selected == 1:
            st.markdown(
                f'<div style="margin-right: 2rem; padding: 0.5rem; '
                f'border-right: 3px solid #7c3aed;">'
                f'<em>{q["distress_instructions"]}</em></div>',
                unsafe_allow_html=True,
            )
            d_sl = q["distress_scale_labels"]
            d_min = q["distress_scale_min"]
            d_max = q["distress_scale_max"]
            d_options = list(range(d_min, d_max + 1))
            d_selected = st.radio(
                label=f"מצוקה פריט {num}",
                options=d_options,
                format_func=lambda x, sl=d_sl: f"{x} - {sl[x]}" if x in sl else str(x),
                key=f"client_{q_key}_{num}_distress",
                index=None,
                label_visibility="collapsed",
            )
            if d_selected is not None:
                responses[f"{num}_distress"] = d_selected
            else:
                all_answered = False

    # C-SSRS: show intensity items if ideation endorsed
    if q.get("intensity_items"):
        any_ideation = any(responses.get(i, 0) == 1 for i in range(1, 6))
        if any_ideation:
            st.divider()
            st.markdown("### עוצמת המחשבות האובדניות")
            st.markdown("*בהתייחס למחשבות האובדניות החמורות ביותר שתיארת:*")
            for iitem in q["intensity_items"]:
                inum = iitem["number"]
                st.markdown(f'**{iitem["text"]}**')
                i_labels = iitem["labels"]
                i_options = sorted(i_labels.keys())
                i_selected = st.radio(
                    label=f"עוצמה {inum}",
                    options=i_options,
                    format_func=lambda x, lb=i_labels: f"{x} - {lb[x]}",
                    key=f"client_{q_key}_{inum}",
                    index=None,
                    label_visibility="collapsed",
                )
                if i_selected is not None:
                    responses[inum] = i_selected
                else:
                    all_answered = False

    # EAT-26: show behavioral section after the 26 items
    if q.get("behavioral_items"):
        st.divider()
        st.markdown("### חלק ב' — התנהגויות בששת החודשים האחרונים")
        b_sl = q["behavioral_scale_labels"]
        b_min = q["behavioral_scale_min"]
        b_max = q["behavioral_scale_max"]
        b_options = list(range(b_min, b_max + 1))
        for bitem in q["behavioral_items"]:
            bnum = bitem["number"]
            st.markdown(
                f'<div class="item-container">'
                f'<div class="item-text">{bnum}. {bitem["text"]}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
            b_selected = st.radio(
                label=f"פריט {bnum}",
                options=b_options,
                format_func=lambda x, sl=b_sl: f"{x} - {sl[x]}" if x in sl else str(x),
                key=f"client_{q_key}_{bnum}",
                index=None,
                label_visibility="collapsed",
            )
            if b_selected is not None:
                responses[bnum] = b_selected
            else:
                all_answered = False

    return responses, all_answered


def render_questionnaire_clinician(q, q_key):
    """Render C-SSRS (and any clinician_mode questionnaire) as a guided clinician interview.

    Returns (responses, all_answered) matching the render_questionnaire_client signature.
    """
    from questionnaires.cssrs import LETHALITY_LABELS, LETHALITY_POTENTIAL_LABELS

    st.markdown(
        '<div style="background:#fde8e8;border:2px solid #e74c3c;border-radius:10px;'
        'padding:0.8rem 1rem;margin-bottom:1rem;">'
        '⚕️ <strong>ראיון מאבחן</strong> — אין להחתים את הנבדק/ת על טופס זה. '
        'המאבחן/ת מנהל/ת את הראיון ומתעד/ת את התשובות.</div>',
        unsafe_allow_html=True,
    )

    responses = {}

    # ── Context ─────────────────────────────────────────────────────
    col_src, col_mon = st.columns(2)
    with col_src:
        source = st.selectbox(
            "מקור מידע",
            ["ראיון עם הנבדק/ת", "בני/ות משפחה", "שניהם — נבדק/ת ומשפחה", "מקור אחר"],
            key=f"clinician_{q_key}_source",
        )
        responses["source"] = source
    with col_mon:
        months = st.number_input(
            "תקופת הייחוס (חודשים)",
            min_value=1, max_value=24, value=1, step=1,
            key=f"clinician_{q_key}_months",
        )
        responses["months"] = int(months)

    st.info(
        "השאלות הן **הצעות לגישוש בלבד** — ניתן להתאים את הניסוח כל עוד "
        "מוערכים כל סוגי המחשבות וההתנהגויות."
    )

    # Helper: render a single Yes/No item with two columns (recent | lifetime)
    def _render_yn_item(num, item, months_val):
        """Render one Yes/No item with guidance expander and two timeframe columns."""
        label_recent = f"ב-{months_val} חודשים האחרונים"
        label_lifetime = "במהלך החיים"

        guidance = item.get("guidance", "")
        item_name = item["text"]

        st.markdown(f"**{num}. {item_name}**")
        if guidance:
            with st.expander("הגדרה קלינית ושאלות מוצעות"):
                st.markdown(guidance)

        col_r, col_l = st.columns(2)
        with col_r:
            st.markdown(f"*{label_recent}*")
            val_r = st.radio(
                f"recent_{num}",
                options=[0, 1],
                format_func=lambda x: "כן" if x == 1 else "לא",
                key=f"clinician_{q_key}_{num}_r",
                index=None,
                label_visibility="collapsed",
                horizontal=True,
            )
        with col_l:
            st.markdown(f"*{label_lifetime}*")
            val_l = st.radio(
                f"lifetime_{num}",
                options=[0, 1],
                format_func=lambda x: "כן" if x == 1 else "לא",
                key=f"clinician_{q_key}_{num}_l",
                index=None,
                label_visibility="collapsed",
                horizontal=True,
            )
        return val_r, val_l

    # ── PART A: Suicidal Ideation ────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="subscale-header" style="background-color:#c0392b;">'
        'חלק א׳ — מחשבות אובדניות</div>',
        unsafe_allow_html=True,
    )
    st.warning(
        "**זרימת הראיון:** שאל/י שאלות 1-2 תחילה.\n\n"
        "• אם **שתיהן שליליות** (לאחרונה) ← עבור/י לחלק ב׳ (התנהגות).\n\n"
        "• אם **אחת חיובית** ← המשך/י לשאלות 3-4-5."
    )

    items_by_num = {item["number"]: item for item in q["items"]}

    # Items 1-2
    val_1r, val_1l = _render_yn_item(1, items_by_num[1], months)
    if val_1r is not None:
        responses[1] = val_1r
    if val_1l is not None:
        responses["1_l"] = val_1l

    val_2r, val_2l = _render_yn_item(2, items_by_num[2], months)
    if val_2r is not None:
        responses[2] = val_2r
    if val_2l is not None:
        responses["2_l"] = val_2l

    # Branching logic
    any_ideation_12_r = responses.get(1, 0) == 1 or responses.get(2, 0) == 1
    any_ideation_12_l = responses.get("1_l", 0) == 1 or responses.get("2_l", 0) == 1
    show_345 = any_ideation_12_r or any_ideation_12_l

    both_1_2_answered_r = (val_1r is not None) and (val_2r is not None)
    if both_1_2_answered_r and not any_ideation_12_r:
        st.info("שתי השאלות שליליות (לאחרונה) → ניתן לעבור לחלק ב׳ — התנהגות אובדנית.")

    # Items 3-5 (conditional)
    if show_345:
        st.markdown(
            '<div class="subscale-header" style="background-color:#e74c3c;opacity:0.85;">'
            'הערכת חומרת החשיבה (שאלות 3-5)</div>',
            unsafe_allow_html=True,
        )
        for num in [3, 4, 5]:
            vr, vl = _render_yn_item(num, items_by_num[num], months)
            if vr is not None:
                responses[num] = vr
            if vl is not None:
                responses[f"{num}_l"] = vl

    # ── Intensity ────────────────────────────────────────────────────
    any_ideation_r = any(responses.get(i, 0) == 1 for i in [1, 2, 3, 4, 5])
    any_ideation_l = any(responses.get(f"{i}_l", 0) == 1 for i in [1, 2, 3, 4, 5])

    if any_ideation_r or any_ideation_l:
        st.markdown("---")
        st.markdown(
            '<div class="subscale-header" style="background-color:#8e44ad;">'
            'עוצמת המחשבות האובדניות</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "*העריך/י לגבי **סוג המחשבות החמורות ביותר** שהיו לאדם — "
            "בתקופה האחרונה ובמהלך החיים:*"
        )

        for iitem in q["intensity_items"]:
            inum = iitem["number"]
            guidance = iitem.get("guidance", "")
            st.markdown(f"**{iitem['text']}**")
            if guidance:
                st.caption(guidance)

            i_options = sorted(iitem["labels"].keys())
            i_fmt = lambda x, lb=iitem["labels"]: f"{x} — {lb[x]}"

            col_r, col_l = st.columns(2)
            with col_r:
                st.markdown(f"*ב-{months} חודשים*")
                val_ir = st.radio(
                    f"intensity_r_{inum}",
                    options=i_options,
                    format_func=i_fmt,
                    key=f"clinician_{q_key}_{inum}_r",
                    index=None,
                    label_visibility="collapsed",
                )
                if val_ir is not None:
                    responses[inum] = val_ir
            with col_l:
                st.markdown("*במהלך החיים*")
                val_il = st.radio(
                    f"intensity_l_{inum}",
                    options=i_options,
                    format_func=i_fmt,
                    key=f"clinician_{q_key}_{inum}_l",
                    index=None,
                    label_visibility="collapsed",
                )
                if val_il is not None:
                    responses[f"{inum}_l"] = val_il

    # ── PART B: Suicidal Behavior ────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="subscale-header" style="background-color:#2980b9;">'
        'חלק ב׳ — התנהגות אובדנית</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "הערך/י את **כל** סוגי ההתנהגות האובדנית, ללא קשר לתשובות חלק א׳. "
        "חובה לשאול על כל הסוגים."
    )

    behavior_items = [item for item in q["items"] if item["number"] >= 6]

    for item in behavior_items:
        num = item["number"]
        vr, vl = _render_yn_item(num, item, months)
        if vr is not None:
            responses[num] = vr
        if vl is not None:
            responses[f"{num}_l"] = vl

        # Attempt counts (items 6-9)
        if num <= 9:
            show_count_r = responses.get(num, 0) == 1
            show_count_l = responses.get(f"{num}_l", 0) == 1
            if show_count_r or show_count_l:
                cnt_col_r, cnt_col_l = st.columns(2)
                with cnt_col_r:
                    if show_count_r:
                        cnt_r = st.number_input(
                            f"מספר אירועים (ב-{months} חודשים)",
                            min_value=1, max_value=100, value=1, step=1,
                            key=f"clinician_{q_key}_{num}_count_r",
                        )
                        responses[f"{num}_count"] = int(cnt_r)
                with cnt_col_l:
                    if show_count_l:
                        cnt_l = st.number_input(
                            "מספר אירועים (כל החיים)",
                            min_value=1, max_value=100, value=1, step=1,
                            key=f"clinician_{q_key}_{num}_count_l",
                        )
                        responses[f"{num}_count_l"] = int(cnt_l)

        # Lethality rating (item 6 only)
        if num == 6 and (responses.get(6, 0) == 1 or responses.get("6_l", 0) == 1):
            st.markdown("**דירוג תוצאה קטלנית / נזק רפואי (0-5):**")
            leth_labels = q.get("lethality_labels", LETHALITY_LABELS)
            leth_options = sorted(leth_labels.keys())
            lethality = st.radio(
                "lethality_rating",
                options=leth_options,
                format_func=lambda x, ll=leth_labels: ll[x],
                key=f"clinician_{q_key}_lethality",
                index=None,
                label_visibility="collapsed",
            )
            if lethality is not None:
                responses["lethality"] = lethality
                if lethality == 0:
                    st.markdown("**פוטנציאל קטלני (0-2) — מכיוון שנזק = 0:**")
                    pot_labels = q.get("lethality_potential_labels", LETHALITY_POTENTIAL_LABELS)
                    pot_options = sorted(pot_labels.keys())
                    leth_pot = st.radio(
                        "lethality_potential",
                        options=pot_options,
                        format_func=lambda x, pl=pot_labels: pl[x],
                        key=f"clinician_{q_key}_lethality_potential",
                        index=None,
                        label_visibility="collapsed",
                    )
                    if leth_pot is not None:
                        responses["lethality_potential"] = leth_pot

        st.markdown("")  # spacer

    # ── Compute all_answered + missing labels ────────────────────────
    item_labels = {item["number"]: item["text"] for item in q["items"]}
    missing = []

    for num in [1, 2]:
        name = item_labels.get(num, f"שאלה {num}")
        if responses.get(num) is None:
            missing.append(f"שאלה {num} ({name}) — לאחרונה")
        if responses.get(f"{num}_l") is None:
            missing.append(f"שאלה {num} ({name}) — במהלך החיים")

    if show_345:
        for num in [3, 4, 5]:
            name = item_labels.get(num, f"שאלה {num}")
            if responses.get(num) is None:
                missing.append(f"שאלה {num} ({name}) — לאחרונה")
            if responses.get(f"{num}_l") is None:
                missing.append(f"שאלה {num} ({name}) — במהלך החיים")

    if any_ideation_r:
        for iitem in q["intensity_items"]:
            if responses.get(iitem["number"]) is None:
                missing.append(f"עוצמה: {iitem['text']} — לאחרונה")
    if any_ideation_l:
        for iitem in q["intensity_items"]:
            if responses.get(f"{iitem['number']}_l") is None:
                missing.append(f"עוצמה: {iitem['text']} — במהלך החיים")

    for num in [6, 7, 8, 9, 10]:
        name = item_labels.get(num, f"שאלה {num}")
        if responses.get(num) is None:
            missing.append(f"שאלה {num} ({name}) — לאחרונה")
        if responses.get(f"{num}_l") is None:
            missing.append(f"שאלה {num} ({name}) — במהלך החיים")

    all_answered = len(missing) == 0

    # Show live missing-fields indicator
    if missing:
        st.markdown("---")
        st.markdown(
            '<div style="background:#fff8e1;border:1px solid #f59e0b;border-radius:8px;'
            'padding:0.7rem 1rem;margin-top:0.5rem;">'
            '<strong>שדות שעוד לא מולאו:</strong><ul style="margin:0.3rem 0 0 0;padding-right:1.2rem;">'
            + "".join(f"<li>{m}</li>" for m in missing)
            + "</ul></div>",
            unsafe_allow_html=True,
        )

    return responses, all_answered


# Subscale color palette for visual grouping
SUBSCALE_COLORS = [
    "#4a90d9", "#9b59b6", "#e67e22", "#27ae60", "#e74c3c",
    "#2980b9", "#8e44ad", "#f39c12", "#16a085", "#c0392b",
]


def _get_subscale_map(q_module):
    """
    Build item_number -> (subscale_name, subscale_color) mapping.
    Handles different subscale dict formats across questionnaires.
    Returns (mapping_dict, ordered_subscale_list) or (None, None) if no subscales.
    """
    code = q_module["code"]
    # Import subscale definitions from the module file
    import importlib
    mod_name = {
        "MHC-SF": "mhc_sf", "DASS-21": "dass21", "TTBQ2-CG31": "ttbq2_cg31",
        "PCL-5": "pcl5", "PTGI": "ptgi", "ITQ": "itq", "OCI-R": "oci_r",
        "TAS-20": "tas20", "EAT-26": "eat26", "IRI": "iri", "DERS": "ders",
        "AQ": "aq",
    }.get(code)
    if not mod_name:
        return None, None

    try:
        mod = importlib.import_module(f"questionnaires.{mod_name}")
    except ImportError:
        return None, None

    subscale_items = {}  # name -> list of item numbers

    if code == "TTBQ2-CG31" and hasattr(mod, "SUBSCALE_ITEMS"):
        for key, items in mod.SUBSCALE_ITEMS.items():
            subscale_items[key] = items
    elif code == "PCL-5" and hasattr(mod, "CLUSTERS"):
        for key, cdata in mod.CLUSTERS.items():
            name = f"אשכול {key} — {cdata['name']}"
            subscale_items[name] = cdata["items"]
    elif code == "ITQ":
        subscale_items["חודרנות (Re)"] = getattr(mod, "PTSD_RE_EXPERIENCING", [])
        subscale_items["הימנעות (Av)"] = getattr(mod, "PTSD_AVOIDANCE", [])
        subscale_items["עוררות (Th)"] = getattr(mod, "PTSD_HYPERAROUSAL", [])
        subscale_items["פגיעה תפקודית PTSD"] = getattr(mod, "PTSD_FUNCTIONAL", [])
        subscale_items["ויסות רגשי (AD)"] = getattr(mod, "DSO_AFFECT_DYSREGULATION", [])
        subscale_items["דימוי עצמי שלילי (NSC)"] = getattr(mod, "DSO_NEGATIVE_SELF", [])
        subscale_items["קשיים ביחסים (DR)"] = getattr(mod, "DSO_DISTURBED_RELATIONS", [])
        subscale_items["פגיעה תפקודית DSO"] = getattr(mod, "DSO_FUNCTIONAL", [])
    elif hasattr(mod, "SUBSCALES"):
        for key, val in mod.SUBSCALES.items():
            if isinstance(val, list):
                subscale_items[key] = val
            elif isinstance(val, dict) and "items" in val:
                name_field = val.get("name") or val.get("label") or val.get("english") or key
                subscale_items[f"{name_field} ({key})" if key != name_field else key] = val["items"]
    else:
        return None, None

    if not subscale_items:
        return None, None

    mapping = {}
    ordered = []
    for idx, (sub_name, items) in enumerate(subscale_items.items()):
        color = SUBSCALE_COLORS[idx % len(SUBSCALE_COLORS)]
        ordered.append((sub_name, color))
        for item_num in items:
            mapping[item_num] = (sub_name, color)

    return mapping, ordered


def _render_visual_items(q_module, raw, results):
    """
    Render full questionnaire items in a visual layout grouped by subscale.
    Shows color-coded subscale headers, item bars, reversed item markers,
    and highlights high-scoring items.
    """
    items = q_module["items"]
    scale_min = q_module["scale_min"]
    scale_max = q_module["scale_max"]
    scale_range = scale_max - scale_min if scale_max > scale_min else 1
    reversed_items = set(q_module["reversed_items"])
    scale_labels = q_module.get("scale_labels", {})

    subscale_map, subscale_order = _get_subscale_map(q_module)
    mid = (scale_min + scale_max) / 2

    # Build item lookup
    item_by_num = {item["number"]: item for item in items}

    if subscale_map and subscale_order:
        # Render grouped by subscale
        assigned = set()
        for sub_name, sub_color in subscale_order:
            sub_items = [it for it in items if it["number"] in subscale_map
                         and subscale_map[it["number"]][0] == sub_name]
            if not sub_items:
                continue
            st.markdown(
                f'<div class="subscale-header" style="background-color: {sub_color};">'
                f'{sub_name}</div>',
                unsafe_allow_html=True,
            )
            for item in sub_items:
                _render_single_item(item, raw, scale_min, scale_max, scale_range,
                                    mid, reversed_items, scale_labels, sub_color)
                assigned.add(item["number"])

        # Render any unassigned items
        unassigned = [it for it in items if it["number"] not in assigned]
        if unassigned:
            st.markdown(
                '<div class="subscale-header" style="background-color: #888;">כללי</div>',
                unsafe_allow_html=True,
            )
            for item in unassigned:
                _render_single_item(item, raw, scale_min, scale_max, scale_range,
                                    mid, reversed_items, scale_labels, "#888")
    else:
        # No subscales — render all items flat with section grouping if available
        current_section = None
        for item in items:
            if "section" in item and item["section"] != current_section:
                current_section = item["section"]
                st.markdown(
                    f'<div class="subscale-header" style="background-color: #4a90d9;">'
                    f'{current_section}</div>',
                    unsafe_allow_html=True,
                )
            _render_single_item(item, raw, scale_min, scale_max, scale_range,
                                mid, reversed_items, scale_labels, "#4a90d9")

    # PQ-B distress followup display
    if q_module.get("has_distress_followup"):
        endorsed_with_distress = []
        for item in items:
            num = str(item["number"])
            if raw.get(num, "0") in (1, "1"):
                d_key = f"{item['number']}_distress"
                d_val = raw.get(d_key) or raw.get(str(d_key))
                endorsed_with_distress.append((item, d_val))
        if endorsed_with_distress:
            st.markdown(
                '<div class="subscale-header" style="background-color: #e74c3c;">'
                'פריטים שאושרו — דירוג מצוקה</div>',
                unsafe_allow_html=True,
            )
            d_labels = q_module.get("distress_scale_labels", {})
            for item, d_val in endorsed_with_distress:
                d_display = f"{d_val}" if d_val else "—"
                d_label = d_labels.get(int(d_val), "") if d_val else ""
                st.markdown(
                    f'<div class="item-row item-high">'
                    f'<span class="item-num">{item["number"]}.</span>'
                    f'<span class="item-txt">{item["text"]}</span>'
                    f'<span class="item-val" style="background:#e74c3c;color:#fff;">'
                    f'מצוקה: {d_display}</span>'
                    f'<span style="font-size:0.8rem;color:#666;">{d_label}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # EAT-26 behavioral section display
    if q_module.get("behavioral_items"):
        from questionnaires.eat26 import BEHAVIORAL_SCALE_LABELS
        st.markdown(
            '<div class="subscale-header" style="background-color: #c0392b;">'
            'התנהגויות בששת החודשים האחרונים</div>',
            unsafe_allow_html=True,
        )
        for bitem in q_module["behavioral_items"]:
            bnum = str(bitem["number"])
            bval = raw.get(bnum, "0")
            try:
                bval_int = int(bval)
            except (ValueError, TypeError):
                bval_int = 0
            b_label = BEHAVIORAL_SCALE_LABELS.get(bval_int, str(bval))
            row_class = "item-high" if bval_int >= 1 else "item-normal"
            st.markdown(
                f'<div class="item-row {row_class}">'
                f'<span class="item-num">{bnum}.</span>'
                f'<span class="item-txt">{bitem["text"]}</span>'
                f'<span class="item-val" style="background:{"#c0392b" if bval_int >= 1 else "#27ae60"};'
                f'color:#fff;">{bval_int}</span>'
                f'<span style="font-size:0.8rem;color:#666;">{b_label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # C-SSRS intensity section display
    if q_module.get("intensity_items"):
        intensity = results.get("intensity", {})
        if intensity:
            st.markdown(
                '<div class="subscale-header" style="background-color: #8e44ad;">'
                'עוצמת המחשבות האובדניות</div>',
                unsafe_allow_html=True,
            )
            for iitem in q_module["intensity_items"]:
                inum = iitem["number"]
                idata = intensity.get(inum)
                if idata:
                    pct = (idata["value"] - 1) / 4 * 100
                    bar_color = _severity_bar_color(idata["value"], 1, 5, 3)
                    st.markdown(
                        f'<div class="item-row item-high">'
                        f'<span class="item-num">{inum}.</span>'
                        f'<span class="item-txt">{idata["label"]}</span>'
                        f'<span class="item-val" style="background:{bar_color};color:#fff;">'
                        f'{idata["value"]}/5</span>'
                        f'<div class="item-bar">'
                        f'<div class="item-bar-fill" style="width:{pct}%;background:{bar_color};"></div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


def _severity_bar_color(val, scale_min, scale_max, mid):
    """Return color based on value relative to scale."""
    if val is None:
        return "#ccc"
    ratio = (val - scale_min) / (scale_max - scale_min) if scale_max > scale_min else 0
    if ratio >= 0.75:
        return "#e74c3c"
    elif ratio >= 0.5:
        return "#e67e22"
    elif ratio >= 0.25:
        return "#f1c40f"
    else:
        return "#27ae60"


def _render_single_item(item, raw, scale_min, scale_max, scale_range,
                         mid, reversed_items, scale_labels, sub_color):
    """Render a single questionnaire item as a visual row."""
    num = item["number"]
    val_raw = raw.get(str(num), None)
    try:
        val = int(val_raw) if val_raw is not None else None
    except (ValueError, TypeError):
        val = None

    is_rev = num in reversed_items
    val_display = val if val is not None else "—"
    val_label = scale_labels.get(val, "") if val is not None else ""

    # Determine if high score (above midpoint — accounting for reversal)
    if val is not None:
        effective = (scale_max - val + scale_min) if is_rev else val
        is_high = effective > mid
    else:
        effective = None
        is_high = False

    row_class = "item-high" if is_high else "item-normal"

    # Bar fill percentage
    if val is not None:
        pct = ((val - scale_min) / scale_range * 100) if scale_range else 0
    else:
        pct = 0

    bar_color = _severity_bar_color(effective, scale_min, scale_max, mid) if val is not None else "#ccc"
    rev_tag = '<span class="item-rev-tag">↩ הפוך</span>' if is_rev else ""

    st.markdown(
        f'<div class="item-row {row_class}">'
        f'<span class="item-num">{num}.</span>'
        f'<span class="item-txt">{item["text"]} {rev_tag}</span>'
        f'<span class="item-val" style="background:{sub_color};color:#fff;">{val_display}</span>'
        f'<div class="item-bar">'
        f'<div class="item-bar-fill" style="width:{pct}%;background:{bar_color};"></div>'
        f'</div>'
        f'<span style="font-size:0.75rem;color:#888;min-width:6rem;">{val_label}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_dashboard_results(q_code, q_data):
    """Render detailed results for therapist dashboard."""
    q_name = q_data["name"]
    raw = q_data["raw_responses"]
    results = q_data["results"]

    # Find the questionnaire module by code
    q_module = None
    for qm in ALL_QUESTIONNAIRES.values():
        if qm["code"] == q_code:
            q_module = qm
            break

    st.markdown(f"## {q_name}")

    # --- Full Questionnaire View ---
    with st.expander("תצוגת שאלון מלאה — פריטים לפי תת-סולמות", expanded=False):
        if q_module:
            _render_visual_items(q_module, raw, results)
        else:
            for num, val in raw.items():
                st.markdown(f"פריט {num}: **{val}**")

    # --- Computed Scores ---
    st.markdown("### ציונים מחושבים")

    if q_code == "C-SSRS":
        # ── Context ──
        months = results.get("months", 1)
        source = results.get("source", "")
        if source:
            st.markdown(f"**מקור מידע:** {source} | **תקופת ייחוס:** {months} חודשים")

        severity = results.get("severity", "")
        severity_class = "severe-box" if severity in ("קריטי", "חמור") else \
                         "warning-box" if severity in ("בינוני-חמור", "בינוני") else "results-box"

        # ── Recent period ──
        st.markdown(f"#### תקופה אחרונה (ב-{months} חודשים)")
        ideation = results.get("ideation_level", 0)
        ideation_desc = results.get("ideation_description", "")
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חשיבה אובדנית:</strong> {ideation}/5 — {ideation_desc}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>התנהגות אובדנית:</strong> {results.get("behavior_summary", "לא דווח")}'
            f'</div>',
            unsafe_allow_html=True,
        )
        cnt_r = results.get("attempt_count_recent")
        if cnt_r:
            st.markdown(f"**מספר ניסיונות (לאחרונה):** {cnt_r}")

        # ── Lifetime ──
        st.markdown("#### במהלך החיים")
        ideation_l = results.get("ideation_level_lifetime", 0)
        ideation_desc_l = results.get("ideation_description_lifetime", "לא דווח")
        sev_class_l = "severe-box" if ideation_l >= 4 else \
                      "warning-box" if ideation_l >= 2 else "results-box"
        st.markdown(
            f'<div class="{sev_class_l}">'
            f'<strong>רמת חשיבה אובדנית (חיים):</strong> {ideation_l}/5 — {ideation_desc_l}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="{sev_class_l}">'
            f'<strong>התנהגות אובדנית (חיים):</strong> {results.get("behavior_summary_lifetime", "לא דווח")}'
            f'</div>',
            unsafe_allow_html=True,
        )
        cnt_l = results.get("attempt_count_lifetime")
        if cnt_l:
            st.markdown(f"**מספר ניסיונות (כל החיים):** {cnt_l}")

        # ── Lethality ──
        if results.get("lethality") is not None:
            leth_desc = results.get("lethality_description", str(results["lethality"]))
            st.markdown(
                f'<div class="warning-box">'
                f'<strong>תוצאה קטלנית / נזק רפואי:</strong> {results["lethality"]}/5 — {leth_desc}'
                f'</div>',
                unsafe_allow_html=True,
            )
        if results.get("lethality_potential") is not None:
            pot_desc = results.get("lethality_potential_description", str(results["lethality_potential"]))
            st.markdown(
                f'<div class="warning-box">'
                f'<strong>פוטנציאל קטלני:</strong> {results["lethality_potential"]}/2 — {pot_desc}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # ── Intensity (recent) ──
        intensity = results.get("intensity", {})
        if intensity:
            st.markdown(f"**עוצמת מחשבות — ב-{months} חודשים:**")
            for ikey, idata in intensity.items():
                st.markdown(f"- **{idata['label']}:** {idata['value']}/5 — {idata['description']}")
            itotal = results.get("intensity_total", 0)
            st.metric(label="ציון עוצמה כולל — לאחרונה (5-25)", value=itotal)

        # ── Intensity (lifetime) ──
        intensity_l = results.get("intensity_lifetime", {})
        if intensity_l:
            st.markdown("**עוצמת מחשבות — במהלך החיים:**")
            for ikey, idata in intensity_l.items():
                st.markdown(f"- **{idata['label']}:** {idata['value']}/5 — {idata['description']}")
            itotal_l = results.get("intensity_total_lifetime", 0)
            st.metric(label="ציון עוצמה כולל — חיים (5-25)", value=itotal_l)

    elif q_code == "TTBQ2-CG31":
        # TTBQ2-CG31: subscale means
        subscale_labels = results.get("subscale_labels", {})
        for sub_key, sub_data in results.get("subscales", {}).items():
            label = subscale_labels.get(sub_key, sub_key)
            mean_val = sub_data["mean"]
            severity_class = "severe-box" if mean_val >= 3 else \
                             "warning-box" if mean_val >= 2.5 else "results-box"
            st.markdown(
                f'<div class="{severity_class}">'
                f'<strong>{label}:</strong> ממוצע {mean_val} '
                f'(סכום: {sub_data["raw_sum"]}, פריטים: {sub_data["items_completed"]})'
                f'</div>',
                unsafe_allow_html=True,
            )
        total_mean = results.get("total_mean", 0)
        st.metric(label="ציון כללי (ממוצע)", value=total_mean)
        if "score_range" in results:
            st.markdown(f"**טווח:** {results['score_range']}")

    elif q_code == "LEC-5":
        # LEC-5: endorsed events list
        total = results.get("total_endorsed", 0)
        st.metric(label=f"מספר מאורעות שדווחו (טווח: {results.get('score_range', '0-16')})", value=total)
        events = results.get("endorsed_events", [])
        if events:
            st.markdown("**מאורעות שדווחו:**")
            for ev in events:
                st.markdown(f"- {ev}")
        if "severity" in results:
            st.markdown(f"**רמת חשיפה:** {results['severity']}")

    elif q_code == "PCL-5":
        # PCL-5: total + clusters + DSM-5 provisional
        total = results.get("total", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "גבוה" in severity or "PTSD" in severity else \
                         "warning-box" if "בינוני" in severity else "results-box"
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '0-80')})", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )
        clusters = results.get("clusters", {})
        if clusters:
            st.markdown("**אשכולות תסמינים:**")
            for cluster_key, cdata in clusters.items():
                st.markdown(
                    f"- **אשכול {cluster_key} — {cdata['name']}:** "
                    f"{cdata['score']}/{cdata['max']} "
                    f"(תסמינים פעילים: {cdata['symptoms_present']})"
                )
        if results.get("dsm5_provisional"):
            st.markdown(
                '<div class="severe-box">⚠️ <strong>סינון DSM-5 חיובי:</strong> '
                'עומד/ת בקריטריונים הזמניים לאבחנת PTSD</div>',
                unsafe_allow_html=True,
            )
        if "dsm5_note" in results:
            st.markdown(f"**הערת DSM-5:** {results['dsm5_note']}")

    elif q_code == "PTGI":
        # PTGI: total + subscale means
        total = results.get("total", 0)
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '21-84')})", value=total)
        subscales = results.get("subscales", {})
        if subscales:
            st.markdown("**תת-סולמות:**")
            for sub_name, sub_data in subscales.items():
                st.markdown(
                    f"- **{sub_name} ({sub_data['english']}):** "
                    f"סכום {sub_data['sum']}/{sub_data['max']}, ממוצע {sub_data['mean']}"
                )
        if "note" in results:
            st.markdown(f"*{results['note']}*")

    elif q_code == "ITQ":
        # ITQ: PTSD / C-PTSD diagnostic algorithm
        st.markdown("**תוצאות אבחוניות:**")
        ptsd_met = results.get("ptsd_met", False)
        dso_met = results.get("dso_met", False)
        cptsd_met = results.get("cptsd_met", False)

        ptsd_class = "severe-box" if ptsd_met else "results-box"
        st.markdown(
            f'<div class="{ptsd_class}">'
            f'<strong>PTSD:</strong> {"עומד/ת בקריטריונים" if ptsd_met else "לא עומד/ת בקריטריונים"} '
            f'(סכום תסמינים: {results.get("ptsd_symptom_sum", 0)})'
            f'</div>',
            unsafe_allow_html=True,
        )
        dso_class = "severe-box" if dso_met else "results-box"
        st.markdown(
            f'<div class="{dso_class}">'
            f'<strong>הפרעות בארגון עצמי (DSO):</strong> '
            f'{"עומד/ת בקריטריונים" if dso_met else "לא עומד/ת בקריטריונים"} '
            f'(סכום תסמינים: {results.get("dso_symptom_sum", 0)})'
            f'</div>',
            unsafe_allow_html=True,
        )
        cptsd_class = "severe-box" if cptsd_met else "results-box"
        st.markdown(
            f'<div class="{cptsd_class}">'
            f'<strong>PTSD מורכב (C-PTSD):</strong> '
            f'{"עומד/ת בקריטריונים" if cptsd_met else "לא עומד/ת בקריטריונים"}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '0-72')})",
                  value=results.get("total_sum", 0))

    elif q_code == "OCI-R":
        # OCI-R: total + subscales (score/max)
        total = results.get("total", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "גבוה" in severity or "חמור" in severity else \
                         "warning-box" if "בינוני" in severity else "results-box"
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '0-72')})", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )
        subscales = results.get("subscales", {})
        if subscales:
            st.markdown("**תת-סולמות:**")
            for sub_name, sub_data in subscales.items():
                st.markdown(f"- **{sub_name}:** {sub_data['score']}/{sub_data['max']}")

    elif q_code == "DES":
        # DES: mean score (0-100)
        total_mean = results.get("total_mean", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "גבוה" in severity or "חמור" in severity else \
                         "warning-box" if "בינוני" in severity else "results-box"
        st.metric(label=f"ציון ממוצע (טווח: {results.get('score_range', '0-100')})", value=f"{total_mean:.1f}")
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )

    elif q_code == "TAS-20":
        # TAS-20: total + 3 flat subscales
        total = results.get("total_score", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "אלקסיתימ" in severity and ("גבוה" in severity or "≥" in severity) else \
                         "warning-box" if "בינוני" in severity or "אפשרית" in severity else "results-box"
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '20-100')})", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**תת-סולמות:**")
        for code in ["DIF", "DDF", "EOT"]:
            name = results.get(f"subscale_{code}_name", code)
            score = results.get(f"subscale_{code}", 0)
            st.markdown(f"- **{name} ({code}):** {score}")

    elif q_code == "PQ-B":
        # PQ-B: total endorsed + distress score
        total = results.get("total_endorsed", 0)
        total_distress = results.get("total_distress", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "גבוה" in severity or "חמור" in severity else \
                         "warning-box" if "בינוני" in severity else "results-box"
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(label="סה\"כ תסמינים מאושרים (0-21)", value=total)
        with col_b:
            st.metric(label="ציון מצוקה כולל (0-105)", value=total_distress)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )

    elif q_code == "EAT-26":
        # EAT-26: total + subscales (plain int)
        total = results.get("total", 0)
        severity = results.get("severity", "")
        cutoff = results.get("cutoff", 20)
        severity_class = "severe-box" if total >= cutoff else "results-box"
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '0-78')}, סף: {cutoff})", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )
        subscales = results.get("subscales", {})
        if subscales:
            st.markdown("**תת-סולמות:**")
            for sub_name, sub_val in subscales.items():
                st.markdown(f"- **{sub_name}:** {sub_val}")
        behavioral = results.get("behavioral_flags", {})
        if behavioral and any(v >= 1 for v in behavioral.values()):
            from questionnaires.eat26 import BEHAVIORAL_ITEMS, BEHAVIORAL_SCALE_LABELS
            st.markdown("**התנהגויות שדווחו:**")
            for bitem in BEHAVIORAL_ITEMS:
                bval = behavioral.get(bitem["number"], 0)
                if bval >= 1:
                    label = BEHAVIORAL_SCALE_LABELS.get(bval, str(bval))
                    st.markdown(
                        f'<div class="warning-box">⚠️ {bitem["text"]}: <strong>{label}</strong></div>',
                        unsafe_allow_html=True,
                    )

    elif q_code == "IRI":
        # IRI: per-subscale means, no total
        st.markdown("**תת-סולמות (ממוצע פריטים):**")
        for code in ["PT", "FC", "EC", "PD"]:
            name = results.get(f"{code}_name", code)
            mean = results.get(f"{code}_mean", 0)
            level = results.get(f"{code}_level", "")
            interp = results.get(f"{code}_interpretation", "")
            level_class = "severe-box" if "גבוה" in level else \
                          "warning-box" if "בינוני" in level else "results-box"
            st.markdown(
                f'<div class="{level_class}">'
                f'<strong>{name} ({code}):</strong> ממוצע {mean:.2f} — {level}'
                f'<br><small>{interp}</small>'
                f'</div>',
                unsafe_allow_html=True,
            )

    elif q_code == "DERS":
        # DERS: total + subscales with label/score/range
        total = results.get("total", 0)
        severity = results.get("severity", "")
        severity_class = "severe-box" if "גבוה" in severity or "חמור" in severity else \
                         "warning-box" if "בינוני" in severity else "results-box"
        st.metric(label=f"ציון כללי (טווח: {results.get('score_range', '36-180')})", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )
        subscales = results.get("subscales", {})
        if subscales:
            st.markdown("**תת-סולמות:**")
            for sub_code, sub_data in subscales.items():
                st.markdown(
                    f"- **{sub_data['label']} ({sub_code}):** "
                    f"{sub_data['score']} (טווח: {sub_data['range']})"
                )

    elif q_code == "AQ":
        # AQ: total binary score + cutoff comparison + subscale breakdown
        total = results.get("total", 0)
        severity = results.get("severity", "")
        severity_class = (
            "severe-box" if severity in ("גבוה מאוד", "מעל סף בינלאומי", "מעל סף קליני ישראלי")
            else "warning-box" if severity == "בינוני"
            else "results-box"
        )
        st.metric(label="ציון כולל בינארי (טווח: 0–50)", value=total)
        st.markdown(
            f'<div class="{severity_class}">'
            f'<strong>רמת חומרה:</strong> {severity}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Cutoff comparison — all three validation studies
        st.markdown("**השוואה לציוני סף:**")
        for cutoff_name, threshold in [
            ("ישראל — Golan & Milua (2006)", 22),
            ("יפן / אנגליה — Kurita et al. (2005); Woodbury-Smith et al. (2005)", 26),
            ("UK מקורי — Baron-Cohen et al. (2001)", 32),
        ]:
            above = total >= threshold
            box_class = "warning-box" if above else "results-box"
            status = "✓ מעל הסף" if above else "✗ מתחת לסף"
            st.markdown(
                f'<div class="{box_class}">'
                f'{cutoff_name} (≥{threshold}): <strong>{status}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Subscale scores — 5 subscales, max 10 each
        subscales = results.get("subscales", {})
        if subscales:
            st.markdown("**תת-סולמות (0–10 כל אחד):**")
            cols = st.columns(len(subscales))
            for col, (sub_name, sub_data) in zip(cols, subscales.items()):
                with col:
                    st.metric(label=sub_name, value=f"{sub_data['score']}/10")

            # Per-subscale binary scores for traceability
            binary_scores = results.get("binary_scores", {})
            if binary_scores:
                with st.expander("ציונים בינאריים לפי תת-סולם (לאימות)", expanded=False):
                    for sub_name, sub_data in subscales.items():
                        item_strs = [
                            f"פריט {n}: {binary_scores.get(n, '?')}"
                            for n in sub_data.get("items", [])
                        ]
                        st.markdown(
                            f"**{sub_name}** (סכום: {sub_data['score']}/10)  \n"
                            + " | ".join(item_strs)
                        )

    elif "subscales" in results and isinstance(list(results["subscales"].values())[0], dict):
        # DASS-21 style
        for sub_name, sub_data in results["subscales"].items():
            severity = sub_data["severity"]
            severity_class = "severe-box" if severity in ("חמור", "חמור ביותר") else \
                             "warning-box" if severity == "בינוני" else "results-box"
            st.markdown(
                f'<div class="{severity_class}">'
                f'<strong>{sub_name}:</strong> {sub_data["score"]}/{sub_data["max"]} — '
                f'רמת חומרה: <strong>{severity}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.metric(label="ציון כללי", value=f"{results['total']}/{results.get('total_max', '')}")

    elif "subscales" in results:
        # MHC-SF style
        cols = st.columns(len(results["subscales"]))
        for col, (sub_name, sub_val) in zip(cols, results["subscales"].items()):
            with col:
                st.metric(label=sub_name, value=sub_val)
        st.metric(label="ציון כללי (ממוצע)", value=results["total"])

    else:
        # SHS / CES-D / PHQ-9 / GAD-7 / ADNM-4 / STO / AQ style
        if "item_scores" in results:
            st.markdown("**ציוני פריטים (לאחר היפוך):**")
            for item_label, val in results["item_scores"].items():
                st.markdown(f"- {item_label}: **{val}**")
        total_label = "ציון כללי"
        if "score_range" in results:
            total_label += f" (טווח: {results['score_range']})"
        st.metric(label=total_label, value=results["total"])
        if "severity" in results:
            severity = results["severity"]
            severity_class = "severe-box" if severity in ("גבוה", "גבוה מאוד", "חמור", "בינוני-חמור") else \
                             "warning-box" if severity in ("מתון", "בינוני") else "results-box"
            st.markdown(
                f'<div class="{severity_class}">'
                f'<strong>רמת חומרה:</strong> {severity}'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Clinical notes (PHQ-9, C-SSRS, TTBQ2-CG31) ---
    if "clinical_note" in results:
        st.markdown(
            f'<div class="severe-box">'
            f'⚠️ <strong>הערה קלינית:</strong> {results["clinical_note"]}'
            f'</div>',
            unsafe_allow_html=True,
        )
    if "dsm_screening" in results:
        st.markdown(
            f'<div class="warning-box">'
            f'<strong>סינון DSM:</strong> {results["dsm_screening"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # --- Interpretation ---
    if "interpretation" in results:
        st.markdown("### פירוש קליני")
        st.markdown(
            f'<div class="results-box">'
            f'{results["interpretation"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # --- Scoring explanation per questionnaire ---
    st.markdown("### הסבר אופן הציון")
    if q_code == "MHC-SF":
        st.markdown("""
**שיטת ציון:** ממוצע פריטים לכל תת-סולם.
- **רווחה נפשית רגשית** (פריטים 1-3): נוכחות רגשות חיוביים (כגון: הרגשתי מסופק בחיי, הרגשתי שמח/ה).
- **רווחה נפשית חברתית** (פריטים 4-8): תפקוד חברתי חיובי (כגון: הרגשתי שייך לקהילה, חשבתי שאנשים הם טובים).
- **רווחה נפשית פסיכולוגית** (פריטים 9-14): תפקוד חיובי בחיי האדם כפרט (כגון: הרגשתי שחוויתי צמיחה, שלחיי יש משמעות).
- **ציון כללי**: ממוצע כל 14 הפריטים — מדד לרווחה נפשית כללית.

**פירוש:** רוב האנשים חווים תחושות רווחה בין פעם בשבוע (4) לפעמיים-שלוש בשבוע (5). תשובות גבוהות/נמוכות מאלו יעידו על רווחה נפשית גבוהה/נמוכה יחסית לכלל האוכלוסייה. ניתן להשוות בין ציוני הסולמות השונים לגבי כל אדם.
""")
    elif q_code == "SHS":
        st.markdown("""
**שיטת ציון:** ממוצע 4 הפריטים. **פריט 4 הינו פריט הפוך** (ציון = 8 - ציון גולמי).

**פירוש:** ככל שציונו של האדם גבוה יותר כך הוא מדווח על רמת אושר ורווחה נפשית גבוהה יותר. אין נקודת חתך ל"אושר תקין". ממוצע באוכלוסייה האמריקאית: 4.5-5.5 (סטיית תקן = 1).
- ציון **6 ומעלה**: אושר סובייקטיבי גבוה מהממוצע.
- ציון **3.5 ומטה**: אושר סובייקטיבי נמוך מהממוצע.
""")
    elif q_code == "CES-D":
        st.markdown("""
**שיטת ציון:** סכום כלל הפריטים (טווח 0-60). **פריטים 4, 8, 12, 16 הינם פריטים הפוכים** (ציון = 3 - ציון גולמי).

פריטי השאלון מחולקים ל-3 גורמי דיכאון: אפקט שלילי, העדר אפקט חיובי, תופעות פסיכו-סומטיות וקושי בינאישי.

**פירוש:**
- ציון **0-10**: תסמיני דיכאון נמוכים.
- ציון **11-16**: תסמיני דיכאון מתונים.
- ציון **17 ומעלה**: תסמיני דיכאון ברמה גבוהה (Blumstein et al., 2012).
- ציון **20 ומעלה**: נקודת חתך מחמירה לדיכאון ברמה גבוהה, בפרט לאוכלוסייה מבוגרת (Stanbury et al., 2006; Shmotkin et al., 2003).
""")
    elif q_code == "DASS-21":
        st.markdown("""
**שיטת ציון:** סכימת דירוגי הנבחן בכל אחד מהסולמות. ציון כללי = סכום כל 21 הפריטים.

**חלוקה לסולמות:**
- **דיכאון** (פריטים 3, 5, 10, 13, 16, 17, 21): דיספוריה, פגיעה בדימוי העצמי, היעדר תקווה, חוסר עניין, אנהדוניה.
- **חרדה** (פריטים 2, 4, 7, 9, 15, 19, 20): חרדה סומטית, חרדה מצבית, חוויה סובייקטיבית של חרדה.
- **לחץ** (פריטים 1, 6, 8, 11, 12, 14, 18): עוררות רגשית, קושי להירגע, נטייה לכעס, חוסר סבלנות.

**טבלת רמות חומרה לכל תת-סולם:**

| | תקין | קל | בינוני | חמור | חמור ביותר |
|---|---|---|---|---|---|
| **דיכאון** | 0-4 | 5-6 | 7-10 | 11-13 | 14+ |
| **חרדה** | 0-3 | 4-5 | 6-7 | 8-9 | 10+ |
| **לחץ** | 0-7 | 8-9 | 10-12 | 13-16 | 17+ |
""")
    elif q_code == "PHQ-9":
        st.markdown("""
**שיטת ציון:** סכימת ציוני כל 9 הפריטים (טווח 0-27). אין פריטים הפוכים.

**סולם:** 0 = כלל לא, 1 = מספר ימים, 2 = יותר ממחצית הימים, 3 = כמעט כל יום.

**פירוש הציונים (Kroenke et al., 2010):**
- ציון **0-4**: היעדר דיכאון.
- ציון **5-9**: דיכאון ברמה תת-סיפית/נמוכה.
- ציון **10-14**: רמת דיכאון בינוני.
- ציון **15-19**: דיכאון בינוני-חמור.
- ציון **20-27**: דיכאון חמור.

**סינון DSM:** אם 5 תסמינים או יותר סומנו כקיימים לפחות "יותר ממחצית הזמן" (ציון ≥2), ואחד מהם הוא אנהדוניה (פריט 1) או מצב רוח דיכאוני (פריט 2) — מסנן חיובי להפרעת דיכאון מג'ורי.

**חשוב:** יש לבחון תמיד את פריט 9 (מחשבות מוות/פגיעה עצמית) ולהעריך סיכון אובדני בראיון קליני.
""")
    elif q_code == "GAD-7":
        st.markdown("""
**שיטת ציון:** סכימת ציוני כל 7 הפריטים (טווח 0-21). אין פריטים הפוכים.

**סולם:** 0 = כלל לא, 1 = כמה ימים, 2 = יותר ממחצית הימים, 3 = כמעט כל יום.

**פירוש הציונים (Robert et al., 2007; Löwe et al., 2008):**
- ציון **מתחת ל-10**: רמת חרדה מתחת לסף הקליני.
- ציון **10 ומעלה**: 'דגל צהוב' — סיכון להפרעת חרדה כללית.
- ציון **15 ומעלה**: 'דגל אדום' — סיכון גבוה להפרעת חרדה כללית.

**הערה:** ציון גבוה יכול לשקף גם הפרעות חרדה נוספות כגון הפרעת פניקה, חרדה חברתית, ו-PTSD, וכן מקרים בהם מתקבלים ציונים גבוהים באוכלוסייה הכללית. לא ניתן להשתמש בשאלון כדרך למתן אבחנה — יש חשיבות לראיון מלא.
""")
    elif q_code == "C-SSRS":
        st.markdown("""
**כלי הערכה:** ראיון חצי מובנה (גרסת סינון) להערכת חומרת האובדנות.

**מחשבות אובדניות — 5 רמות:**
1. הרצון להיות מת/ה
2. מחשבות אובדניות פעילות בלתי ספציפיות
3. מחשבות אובדניות עם שיטה כלשהי (ללא תכנית)
4. מחשבות אובדניות עם כוונה לפעול (ללא תכנית ספציפית)
5. מחשבות אובדניות עם תכנית וכוונה מוגדרות

**התנהגות אובדנית:**
- ניסיון בפועל, ניסיון שסוכל, ניסיון שנזנח, פעולות הכנה.
- בנוסף: פגיעה עצמית שאיננה אובדנית.

**פירוש:** ככל שרמת המחשבות גבוהה יותר ו/או קיימת התנהגות אובדנית, כך הסיכון גבוה יותר. אין ציון סף מספרי — ההערכה הקלינית מבוססת על שיקול דעת המטפל (Posner et al., 2011).

**חשוב:** כלי זה נועד לשימוש על ידי אנשים שעברו הכשרה בשימוש בו. השאלות הינן הצעות לגישוש בלבד.
""")
    elif q_code == "TTBQ2-CG31":
        st.markdown("""
**שיטת ציון:** ממוצע פריטים לכל גורם (לאחר היפוך פריטים המסומנים ב-R). ציון כללי = סכום ציוני כל הגורמים / מספר הפריטים שמולאו.

**היפוך סולם:** בפריטים מסומנים: 1→5, 2→4, 3→3, 4→2, 5→1. לאחר ההיפוך, ציון גבוה = קשיי התמודדות רבים יותר.

**4 גורמים (תת-סולמות):**
- **מסלול I – חוסר תפקוד (I-DF):** 8 פריטים — התמודדות בלתי מסתגלת, בעיות בקשרים, תפישה עצמית שלילית, היעדר משמעות, בריאות גופנית, דיכאון וחרדה.
- **מסלול II – התאבלות אקטיבית וטראומה (II-ARTG):** 16 פריטים — רגשות עזים מהאובדן, כמיהה, קושי לחיות ללא הנפטר, תפישת המוות כטראומטי.
- **מסלול II – אספקטים קונפליקטואליים של הקשר (II-RC):** 5 פריטים — היבטים שליליים בקשר לפני ואחרי האובדן.
- **מסלול II – מערכת יחסים קרובה וחיובית (II-CPR):** 2 פריטים — תפישת הקשר כקרוב ותומך.

**נקודת חתך:** ציון כללי ≥3 מצביע על אבל מורכב עם סיבוכים חמורים (לאחר 64+ חודשים מהאובדן). יש לתת תשומת לב גם לציונים תת-קליניים ולפריטים בודדים עם ציונים גבוהים.

**שימו לב:** יש לבחון בנפרד את הפריט "עכשיו אני מבין אנשים שחושבים לשים קץ לחייהם" כדי לאתר סממנים אובדניים (Rubin & Bar-Nadav, 2016).
""")
    elif q_code == "ADNM-4":
        st.markdown("""
**שיטת ציון:** סכימת 4 הפריטים (טווח 4-16). סולם ליקרט 1-4.

**פירוש:**
- ציון **4-7**: תסמיני הסתגלות נמוכים.
- ציון **8-11**: תסמיני הסתגלות בינוניים — מומלץ מעקב.
- ציון **12-16**: תסמיני הסתגלות גבוהים — חשד להפרעת הסתגלות, מומלץ הערכה קלינית מעמיקה.

**הערה:** השאלון המקוצר (ADNM-4) מהווה כלי סינון בלבד ואינו מחליף אבחנה קלינית מלאה.
""")
    elif q_code == "LEC-5":
        st.markdown("""
**שיטת ציון:** ספירת מאורעות מלחיצים שהנבדק דיווח כי חווה (מתוך 16 קטגוריות). אין ציון מספרי מסכם — הכלי משמש לזיהוי חשיפה לאירועים טראומטיים.

**שימוש:** ה-LEC-5 הוא שאלון מלווה ל-PCL-5 ומהווה בסיס לזיהוי "מאורע הייחוס" (index event) עליו הנבדק ממלא את ה-PCL-5.

**פירוש:** אין נקודת חתך. יש לבחון את סוגי המאורעות, מספרם, ואופי החשיפה (ישירה, עדות, שמיעה) בהקשר הקליני.
""")
    elif q_code == "PCL-5":
        st.markdown("""
**שיטת ציון:** סכימת 20 הפריטים (טווח 0-80). סולם 0-4.

**חלוקה לאשכולות תסמינים (DSM-5):**
- **אשכול B — חודרנות** (פריטים 1-5): זיכרונות פולשניים, חלומות, פלשבקים, מצוקה בחשיפה לגירויים.
- **אשכול C — הימנעות** (פריטים 6-7): הימנעות ממחשבות/רגשות ומגירויים חיצוניים.
- **אשכול D — קוגניציות ומצב רוח** (פריטים 8-14): שינויים שליליים בקוגניציה ובמצב רוח.
- **אשכול E — עוררות ותגובתיות** (פריטים 15-20): עוררות יתר, תגובות בהלה, התנהגות מסוכנת.

**נקודת חתך:** ציון **33 ומעלה** מצביע על חשד ל-PTSD.

**סינון DSM-5 זמני:** נדרש לפחות תסמין אחד בדירוג ≥2 בכל אשכול (B: לפחות 1, C: לפחות 1, D: לפחות 2, E: לפחות 2).

**הפניה:** Weathers et al. (2013). The PTSD Checklist for DSM-5 (PCL-5).
""")
    elif q_code == "PTGI":
        st.markdown("""
**שיטת ציון:** סכימת 21 הפריטים (טווח 21-84). סולם 1-4 (מ"לא חוויתי שינוי" עד "חוויתי שינוי בעוצמה רבה מאוד").

**5 תת-סולמות:**
- **התייחסות לאחרים** (פריטים 6, 8, 9, 15, 16, 20, 21): שינויים בתפיסת יחסים בין-אישיים.
- **אפשרויות חדשות** (פריטים 3, 7, 11, 14, 17): תפיסת הזדמנויות וכיוונים חדשים בחיים.
- **כוח אישי** (פריטים 4, 10, 12, 19): תחושת חוסן וחוזק אישי.
- **שינוי רוחני** (פריטים 5, 18): שינויים בתחום הרוחני/אקזיסטנציאלי.
- **הערכת החיים** (פריטים 1, 2, 13): הערכה מוגברת של החיים.

**פירוש:** ציון גבוה יותר = צמיחה פוסט-טראומטית רבה יותר. אין נקודת חתך — הציונים מספקים תמונה תיאורית ולא אבחנתית.

**הפניה:** Tedeschi & Calhoun (1996).
""")
    elif q_code == "STO":
        st.markdown("""
**שיטת ציון:** סכימת 5 הפריטים (טווח 5-25). סולם ליקרט 1-5.

**נקודת חתך:** ציון **14 ומעלה** מצביע על תפיסה סובייקטיבית גבוהה של הטראומה — כלומר, הנבדק תופס את האירוע כטראומטי באופן משמעותי.

**פירוש:**
- ציון **5-9**: תפיסת טראומה נמוכה.
- ציון **10-13**: תפיסת טראומה בינונית.
- ציון **14-25**: תפיסת טראומה גבוהה — מומלץ הערכה נוספת עם PCL-5/ITQ.

**הערה:** השאלון מודד תפיסה סובייקטיבית ולא חומרה אובייקטיבית של האירוע.
""")
    elif q_code == "ITQ":
        st.markdown("""
**שיטת ציון:** 18 פריטים, סולם 0-4. הציון מחולק לשתי תסמונות:

**PTSD (6 פריטים):** 3 אשכולות, 2 פריטים בכל אחד:
- **חודרנות (Re):** פריטים 1-2
- **הימנעות (Av):** פריטים 3-4
- **עוררות (Th):** פריטים 5-6
- **פגיעה תפקודית:** פריטים 7-9

אבחנת PTSD: לפחות פריט 1 בדירוג ≥2 בכל אשכול + פגיעה תפקודית.

**הפרעות בארגון עצמי — DSO (6 פריטים):** 3 אשכולות:
- **ויסות רגשי (AD):** פריטים 10-11
- **דימוי עצמי שלילי (NSC):** פריטים 12-13
- **קשיים ביחסים (DR):** פריטים 14-15
- **פגיעה תפקודית:** פריטים 16-18

**אבחנה:**
- **PTSD**: עומד/ת בקריטריוני PTSD בלבד.
- **C-PTSD (PTSD מורכב)**: עומד/ת בקריטריוני PTSD + DSO.

**הפניה:** Cloitre et al. (2018). ICD-11 International Trauma Questionnaire.
""")
    elif q_code == "OCI-R":
        st.markdown("""
**שיטת ציון:** סכימת 18 הפריטים (טווח 0-72). סולם 0-4.

**6 תת-סולמות (3 פריטים כל אחד):**
- **שטיפה** (פריטים 5, 11, 17): התנהגויות ניקיון כפייתיות.
- **בדיקה** (פריטים 2, 8, 14): בדיקה חוזרת.
- **סדר** (פריטים 3, 9, 15): צורך בסדר וסימטריה.
- **אובססיות** (פריטים 6, 12, 18): מחשבות פולשניות.
- **אגירה** (פריטים 1, 7, 13): קושי להשליך חפצים.
- **ניטרול** (פריטים 4, 10, 16): ריטואלים מנטליים.

**נקודת חתך:** ציון כללי **21 ומעלה** מצביע על חשד ל-OCD.

**הפניה:** Foa et al. (2002). The Obsessive-Compulsive Inventory: Development and validation of a short version.
""")
    elif q_code == "DES":
        st.markdown("""
**שיטת ציון:** ממוצע אחוזי ההתרחשות של כל 28 הפריטים (טווח 0-100). כל פריט נע בין 0% ל-100%.

**נקודת חתך:** ציון ממוצע **30 ומעלה** מצביע על דיסוציאציה פתולוגית — מומלץ הערכה קלינית מעמיקה.

**פריטים פתולוגיים מרכזיים:** פריטים 3, 5, 7, 8, 12, 13, 22, 27 — ציון גבוה (>30%) בפריטים אלו מחזק חשד לדיסוציאציה פתולוגית (DES-T).

**פירוש:**
- ציון **0-10**: דיסוציאציה נורמטיבית.
- ציון **11-29**: דיסוציאציה בינונית — ייתכנו חוויות דיסוציאטיביות שאינן פתולוגיות.
- ציון **30 ומעלה**: דיסוציאציה פתולוגית — מומלץ הפניה להערכה ממוקדת.

**הפניה:** Bernstein & Putnam (1986). Development, reliability, and validity of a dissociation scale.
""")
    elif q_code == "TAS-20":
        st.markdown("""
**שיטת ציון:** סכימת 20 הפריטים (טווח 20-100). סולם ליקרט 1-5. **פריטים הפוכים:** 4, 5, 10, 18, 19.

**3 תת-סולמות:**
- **DIF — קושי בזיהוי רגשות** (פריטים 1, 3, 6, 7, 9, 13, 14): קושי לזהות ולהבחין בין רגשות לתחושות גופניות.
- **DDF — קושי בתיאור רגשות** (פריטים 2, 4, 11, 12, 17): קושי לתאר ולבטא רגשות בפני אחרים.
- **EOT — חשיבה מוכוונת חיצונית** (פריטים 5, 8, 10, 15, 16, 18, 19, 20): נטייה לחשיבה קונקרטית ולא רפלקטיבית.

**נקודות חתך:**
- ציון **≤51**: אין אלקסיתימיה.
- ציון **52-60**: אלקסיתימיה אפשרית (תת-סיפית).
- ציון **≥61**: אלקסיתימיה.

**הפניה:** Bagby, Parker & Taylor (1994). The Toronto Alexithymia Scale.
""")
    elif q_code == "PQ-B":
        st.markdown("""
**שיטת ציון:** ספירת פריטים שהנבדק אישר (כן/לא). טווח 0-21.

**נקודת חתך:** **8 פריטים מאושרים ומעלה** מצביע על סיכון מוגבר לתסמינים פרודרומליים (מוקדמים) של פסיכוזה.

**פירוש:**
- ציון **0-3**: סיכון נמוך.
- ציון **4-7**: סיכון בינוני — מומלץ מעקב.
- ציון **8-21**: סיכון גבוה — מומלצת הערכה קלינית מעמיקה לסיכון לפסיכוזה.

**הערה:** השאלון מהווה כלי סינון בלבד. ציון גבוה אינו מעיד בהכרח על פסיכוזה מתפתחת — נדרשת הערכה מקצועית.

**הפניה:** Loewy et al. (2011). The Prodromal Questionnaire (PQ-B).
""")
    elif q_code == "EAT-26":
        st.markdown("""
**שיטת ציון:** סולם 0-5 (מ"אף פעם" עד "תמיד"), אך **ציון מיוחד**: רק 3 התשובות הגבוהות ביותר מקבלות ציון (תמיד=3, בדרך כלל=2, לעתים קרובות=1, שאר=0). **פריט 25 הינו פריט הפוך.**

טווח ציון: 0-78.

**3 תת-סולמות:**
- **דיאטה** (13 פריטים): עיסוק בהרזיה, ספירת קלוריות, הימנעות ממזון.
- **בולימיה ועיסוק במזון** (6 פריטים): אכילה כפייתית, הקאות, עיסוק יתר במזון.
- **שליטה באכילה** (7 פריטים): שליטה עצמית ולחץ סביבתי לאכול.

**נקודת חתך:** ציון כללי **20 ומעלה** מצביע על סיכון להפרעת אכילה — מומלצת הערכה קלינית.

**הפניה:** Garner et al. (1982). The Eating Attitudes Test (EAT-26).
""")
    elif q_code == "AQ":
        st.markdown("""
**שיטת ציון:** 50 פריטים, סולם 1-4 (מסכים בהחלט, מסכים במקצת, לא מסכים במקצת, לא מסכים כלל). **ציון בינארי:** כל פריט מקבל 0 או 1 בהתאם לכיוון "אוטיסטי". טווח: 0–50.

**כיוון ציון:**
- פריטי **הסכמה** (24 פריטים): הסכמה ("מסכים בהחלט"/"מסכים במקצת") = 1 נקודה — מאפיין אוטיסטי מתבטא בהסכמה.
- פריטי **אי-הסכמה** (26 פריטים): אי-הסכמה ("לא מסכים במקצת"/"לא מסכים כלל") = 1 נקודה — מאפיין אוטיסטי מתבטא בשלילה.

**5 תת-סולמות (10 פריטים כל אחד, ציון מקסימלי 10):**
- **מיומנויות חברתיות** (פריטים 1, 11, 13, 15, 22, 36, 44, 45, 47, 48)
- **הטיית/שינוי קשב** (פריטים 2, 4, 10, 16, 25, 32, 34, 37, 43, 46)
- **קשב לפרטים** (פריטים 5, 6, 9, 12, 19, 23, 28, 29, 30, 49)
- **תקשורת** (פריטים 7, 17, 18, 26, 27, 31, 33, 35, 38, 39)
- **דמיון** (פריטים 3, 8, 14, 20, 21, 24, 40, 41, 42, 50)

**ציוני סף:**
| מחקר | סף | הערה |
|---|---|---|
| ישראל — Golan & Milua (2006) | ≥22 | רגישות 0.73, ספציפיות 0.82 |
| יפן / אנגליה — Kurita et al. (2005); Woodbury-Smith et al. (2005) | ≥26 | |
| UK מקורי — Baron-Cohen et al. (2001) | ≥32 | |

**הפניה:** Baron-Cohen et al. (2001). The Autism-Spectrum Quotient (AQ): Evidence from Asperger Syndrome/High-Functioning Autism, Males and Females, Scientists and Mathematicians. *Journal of Autism and Developmental Disorders*, 31(1), 5–17.
""")
    elif q_code == "IRI":
        st.markdown("""
**שיטת ציון:** 28 פריטים, סולם ליקרט 1-5. **פריטים הפוכים:** 3, 4, 7, 12, 13, 14, 15, 18, 19. הציון מחושב כממוצע פריטים לכל תת-סולם (אין ציון כללי).

**4 תת-סולמות (7 פריטים כל אחד):**
- **PT — נטילת פרספקטיבה** (פריטים 3, 8, 11, 15, 21, 25, 28): יכולת לאמץ נקודת מבט של האחר — אמפתיה קוגניטיבית.
- **FC — פנטזיה** (פריטים 1, 5, 7, 12, 16, 23, 26): נטייה להזדהות עם דמויות בדיוניות.
- **EC — דאגה אמפתית** (פריטים 2, 4, 9, 14, 18, 20, 22): רגשות חמלה ודאגה כלפי אחרים — אמפתיה רגשית.
- **PD — מצוקה אישית** (פריטים 6, 10, 13, 17, 19, 24, 27): תחושת אי-נוחות ומצוקה כאשר צופים בסבלו של אחר.

**פירוש:** הציון בכל תת-סולם נע בין 1.0 ל-5.0. ציון גבוה ב-PT ו-EC מעיד על אמפתיה גבוהה. ציון גבוה ב-PD מעיד על מצוקה אישית (קשה להיות בנוכחות סבל). ציון גבוה ב-FC מעיד על דמיון אמפתי.

**הפניה:** Davis (1983). Measuring individual differences in empathy: Evidence for a multidimensional approach.
""")
    elif q_code == "DERS":
        st.markdown("""
**שיטת ציון:** סכימת 36 הפריטים (טווח 36-180). סולם ליקרט 1-5. **פריטים הפוכים:** 1, 2, 6, 7, 8, 10, 17, 20, 22, 24, 34 (לאחר היפוך, ציון גבוה = קושי רב יותר בוויסות).

**6 תת-סולמות:**
- **NONACCEPT — אי-קבלת תגובות רגשיות** (פריטים 11, 12, 21, 23, 25, 29): נטייה לתגובות שליליות משניות כלפי רגשות.
- **GOALS — קשיים בהתנהגות מכוונת מטרה** (פריטים 13, 18, 20R, 26, 33): קושי להתרכז ולבצע משימות בעת מצוקה.
- **IMPULSE — קשיי שליטה בדחפים** (פריטים 3, 14, 19, 24R, 27, 32): קושי לשמור על שליטה התנהגותית בעת מצוקה.
- **AWARENESS — חוסר מודעות רגשית** (פריטים 2R, 6R, 8R, 10R, 17R, 34R): חוסר תשומת לב לרגשות.
- **STRATEGIES — גישה מוגבלת לאסטרטגיות ויסות** (פריטים 15, 16, 22R, 28, 30, 31, 35, 36): אמונה שאין דרך להתמודד עם מצוקה.
- **CLARITY — חוסר בהירות רגשית** (פריטים 1R, 4, 5, 7R, 9): קושי לזהות ולהבחין בין רגשות.

**פירוש:** ציון כללי גבוה מעיד על קשיים רבים יותר בוויסות רגשי. ניתן לבחון את הפרופיל בין התת-סולמות כדי לזהות תחומי קושי ספציפיים.

**הפניה:** Gratz & Roemer (2004). Multidimensional assessment of emotion regulation and dysregulation.
""")

    st.divider()


# ============================================================
# QUESTIONNAIRE CATEGORIES
# ============================================================

CATEGORIES = {
    "רווחה נפשית": ["MHC-SF", "SHS"],
    "דיכאון": ["CES-D", "DASS-21", "PHQ-9"],
    "חרדה": ["GAD-7"],
    "אובדנות ואובדן": ["C-SSRS", "TTBQ2-CG31"],
    "טראומה ו-PTSD": ["LEC-5", "PCL-5", "PTGI", "STO", "ITQ", "ADNM-4"],
    "הפרעות נוספות": ["OCI-R", "DES", "TAS-20", "PQ-B", "EAT-26", "AQ", "IRI", "DERS"],
}

Q_DESCRIPTIONS = {
    "MHC-SF": "רצף הבריאות הנפשית המקוצר (14 פריטים)",
    "SHS": "מדד האושר הסובייקטיבי (4 פריטים)",
    "CES-D": "שאלון להערכת דיכאון (20 פריטים)",
    "DASS-21": "דיכאון, חרדה ולחץ (21 פריטים)",
    "PHQ-9": "שאלון בריאות המטופל – דיכאון (9 פריטים)",
    "C-SSRS": "סולם קולומביה – דירוג חומרת אובדנות (6 פריטים)",
    "TTBQ2-CG31": "השאלון הדו-מסלולי – אבל מורכב (31 פריטים)",
    "GAD-7": "חרדה כללית (7 פריטים)",
    "ADNM-4": "הפרעת הסתגלות מקוצר (4 פריטים)",
    "LEC-5": "סקר מאורעות חיים מלחיצים (16 פריטים)",
    "PCL-5": "רשימת מאפיינים ל-PTSD (20 פריטים)",
    "PTGI": "צמיחה פוסט-טראומטית (21 פריטים)",
    "STO": "תפיסה סובייקטיבית של הטראומה (5 פריטים)",
    "ITQ": "שאלון הטראומה הבינלאומי (18 פריטים)",
    "OCI-R": "אובססיביות-קומפולסיביות (18 פריטים)",
    "DES": "סולם חוויות דיסוציאטיביות (28 פריטים)",
    "TAS-20": "סולם אלקסיתימיה טורונטו (20 פריטים)",
    "PQ-B": "שאלון פרודרומלי מקוצר – פסיכוזה (21 פריטים)",
    "EAT-26": "מבחן עמדות אכילה (26 פריטים)",
    "AQ": "מנת הספקטרום האוטיסטי (50 פריטים)",
    "IRI": "מדד התגובתיות הבין-אישית – אמפתיה (28 פריטים)",
    "DERS": "סולם קשיים בוויסות רגשי (36 פריטים)",
}


# ============================================================
# SCREEN 1: THERAPIST SETUP
# ============================================================

def screen_setup():
    st.markdown(
        '<div class="setup-header">'
        '<h1>אוגדן שאלונים לדיווח עצמי</h1>'
        '<p>הגדרת מפגש חדש או צפייה בתוצאות קודמות</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    client_number = st.text_input(
        "מספר מזהה למטופל",
        value="",
        key="setup_client_number",
        placeholder="מספר פנימי לשימוש המטפל בלבד",
    )

    st.markdown("")
    st.markdown("##### בחירת שאלונים")

    # Initialize checkbox state
    if "selected_q_set" not in st.session_state:
        st.session_state.selected_q_set = set()

    for cat_name, cat_keys in CATEGORIES.items():
        valid_keys = [k for k in cat_keys if k in ALL_QUESTIONNAIRES]
        if not valid_keys:
            continue

        with st.expander(f"{cat_name} ({len(valid_keys)} שאלונים)", expanded=True):
            # Select all checkbox for this category
            all_selected = all(k in st.session_state.selected_q_set for k in valid_keys)
            if st.checkbox(
                "בחר הכל",
                value=all_selected,
                key=f"cat_all_{cat_name}",
            ):
                for k in valid_keys:
                    st.session_state.selected_q_set.add(k)
            else:
                if all_selected:
                    for k in valid_keys:
                        st.session_state.selected_q_set.discard(k)

            for q_key in valid_keys:
                desc = Q_DESCRIPTIONS.get(q_key, q_key)
                checked = q_key in st.session_state.selected_q_set
                if st.checkbox(
                    f"**{q_key}** — {desc}",
                    value=checked,
                    key=f"q_check_{q_key}",
                ):
                    st.session_state.selected_q_set.add(q_key)
                else:
                    st.session_state.selected_q_set.discard(q_key)

    selected = [k for k in ALL_QUESTIONNAIRES if k in st.session_state.selected_q_set]

    if selected:
        st.markdown(f"**{len(selected)}** שאלונים נבחרו")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("התחל מפגש", type="primary", use_container_width=True):
            if not client_number.strip():
                st.error("יש להזין מספר מזהה למטופל.")
            elif not selected:
                st.error("יש לבחור לפחות שאלון אחד.")
            else:
                st.session_state.client_number = client_number.strip()
                st.session_state.selected_questionnaires = selected
                st.session_state.current_q_index = 0
                st.session_state.all_responses = {}
                st.session_state.screen = "client"
                st.rerun()

    with col2:
        if st.button("לוח בקרה", use_container_width=True):
            st.session_state.screen = "dashboard"
            st.rerun()


# ============================================================
# DEMO / AUTOFILL HELPER
# ============================================================

def _autofill_demo(q, q_key):
    """Fill all session-state widget keys with representative demo values."""
    if q.get("clinician_mode"):
        # C-SSRS demo: passive ideation recently, more history lifetime; no behavior
        st.session_state[f"clinician_{q_key}_source"] = "ראיון עם הנבדק/ת"
        st.session_state[f"clinician_{q_key}_months"] = 3
        # Ideation items (1-5): recent col / lifetime col
        demo_ideation = {1: (1, 1), 2: (1, 1), 3: (0, 1), 4: (0, 0), 5: (0, 0)}
        for num, (val_r, val_l) in demo_ideation.items():
            st.session_state[f"clinician_{q_key}_{num}_r"] = val_r
            st.session_state[f"clinician_{q_key}_{num}_l"] = val_l
        # Intensity items: middle value for both timeframes
        for iitem in q.get("intensity_items", []):
            inum = iitem["number"]
            opts = sorted(iitem["labels"].keys())
            mid = opts[len(opts) // 2]
            st.session_state[f"clinician_{q_key}_{inum}_r"] = mid
            st.session_state[f"clinician_{q_key}_{inum}_l"] = mid
        # Behavior items 6-10: all No
        for num in range(6, 11):
            st.session_state[f"clinician_{q_key}_{num}_r"] = 0
            st.session_state[f"clinician_{q_key}_{num}_l"] = 0
    else:
        scale_min = q["scale_min"]
        scale_max = q["scale_max"]
        mid = (scale_min + scale_max) // 2
        for item in q["items"]:
            num = item["number"]
            if "labels" in item:
                opts = sorted(item["labels"].keys())
                val = opts[len(opts) // 2]
            elif "alt_scale" in item:
                opts = sorted(item["alt_scale"].keys())
                val = opts[len(opts) // 2]
            else:
                val = mid
            st.session_state[f"client_{q_key}_{num}"] = val
            # PQ-B distress: skip (only appears for endorsed items)
        # Intensity items (non-clinician C-SSRS — not used, but defensive)
        for iitem in q.get("intensity_items", []):
            inum = iitem["number"]
            opts = sorted(iitem["labels"].keys())
            st.session_state[f"client_{q_key}_{inum}"] = opts[len(opts) // 2]
        # EAT-26 behavioral items
        b_mid = ((q.get("behavioral_scale_min", 0) + q.get("behavioral_scale_max", 0)) // 2
                 if q.get("behavioral_items") else 0)
        for bitem in q.get("behavioral_items", []):
            st.session_state[f"client_{q_key}_{bitem['number']}"] = b_mid


# ============================================================
# SCREEN 2: CLIENT FILLING
# ============================================================

def screen_client():
    selected_qs = st.session_state.selected_questionnaires
    idx = st.session_state.current_q_index

    if idx >= len(selected_qs):
        # All questionnaires done — submit
        screen_submit()
        return

    q_key = selected_qs[idx]
    q = ALL_QUESTIONNAIRES[q_key]

    # Custom progress bar
    pct = int((idx / len(selected_qs)) * 100)
    st.markdown(
        f'<div class="q-progress-wrap">'
        f'<span class="q-progress-text">{idx + 1} / {len(selected_qs)}</span>'
        f'<div class="q-progress-bar">'
        f'<div class="q-progress-fill" style="width:{pct}%;"></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # ── Demo autofill ──────────────────────────────────────────────
    with st.expander("🔍 מצב בדיקה — מילוי אוטומטי", expanded=False):
        st.caption("ממלא את השאלון בערכים לדוגמה כדי לראות את הניתוח והעיצוב במהירות.")
        if st.button("מלא אוטומטית", key=f"autofill_{q_key}_{idx}"):
            _autofill_demo(q, q_key)
            st.rerun()

    if q.get("clinician_mode"):
        responses, all_answered = render_questionnaire_clinician(q, q_key)
    else:
        responses, all_answered = render_questionnaire_client(q, q_key)

    st.markdown("")  # spacer

    if idx < len(selected_qs) - 1:
        button_label = "הבא"
    else:
        button_label = "סיום"

    if st.button(button_label, type="primary", use_container_width=True):
        if not all_answered:
            if q.get("clinician_mode"):
                st.error("יש להשלים את כל השדות הנדרשים — ראה רשימת השדות החסרים למעלה.")
            else:
                unanswered = [
                    item["number"]
                    for item in q["items"]
                    if item["number"] not in responses
                ]
                st.error(f"יש לענות על כל הפריטים. פריטים חסרים: {unanswered}")
        else:
            st.session_state.all_responses[q_key] = responses
            st.session_state.current_q_index = idx + 1
            st.rerun()


def screen_submit():
    """Save results and show thank-you with download options."""
    # Save only once
    if "session_saved" not in st.session_state or not st.session_state.session_saved:
        session_data = save_session(
            st.session_state.client_number, st.session_state.all_responses
        )
        st.session_state.session_saved = True
        st.session_state.last_session = session_data

    st.markdown(
        '<div class="thank-you">'
        "<h1>תודה רבה</h1>"
        "<p>התשובות נקלטו בהצלחה.</p>"
        "<p>ניתן להעביר את המכשיר בחזרה למטפל/ת.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Download buttons for the therapist
    session_data = st.session_state.get("last_session")
    if session_data:
        st.markdown("---")
        st.markdown("##### הורדת תוצאות")
        client_id = session_data.get("client_number", "")
        ts = session_data.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts)
            date_str = dt.strftime("%d-%m-%Y_%H%M")
        except (ValueError, TypeError):
            date_str = "session"

        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            csv_bytes = _export_session_csv(session_data)
            st.download_button(
                label="CSV הורדת",
                data=csv_bytes,
                file_name=f"{client_id}_{date_str}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with dl_col2:
            pdf_bytes = _export_session_pdf(session_data)
            st.download_button(
                label="PDF הורדת",
                data=pdf_bytes,
                file_name=f"{client_id}_{date_str}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("חזרה למסך מטפל", use_container_width=True):
            st.session_state.screen = "setup"
            st.session_state.session_saved = False
            st.session_state.all_responses = {}
            st.session_state.current_q_index = 0
            st.rerun()
    with col2:
        if st.button("לוח בקרה", use_container_width=True):
            st.session_state.screen = "dashboard"
            st.session_state.session_saved = False
            st.rerun()


# ============================================================
# EXPORT HELPERS
# ============================================================

_HEBREW_FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "Rubik-Regular.ttf")


def _export_session_csv(session):
    """Export a session to CSV bytes. One row per questionnaire item."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "questionnaire_code", "questionnaire_name", "item_number",
        "item_text", "raw_response", "score_label",
    ])

    for q_code, q_data in session.get("questionnaires", {}).items():
        q_name = q_data.get("name", q_code)
        raw = q_data.get("raw_responses", {})

        # Find module to get item texts
        q_module = None
        for qm in ALL_QUESTIONNAIRES.values():
            if qm["code"] == q_code:
                q_module = qm
                break

        if q_module:
            scale_labels = q_module.get("scale_labels", {})
            for item in q_module["items"]:
                num = item["number"]
                val = raw.get(str(num), "")
                try:
                    label = scale_labels.get(int(val), str(val))
                except (ValueError, TypeError):
                    label = str(val)
                writer.writerow([q_code, q_name, num, item["text"], val, label])

            # Behavioral items (EAT-26)
            if q_module.get("behavioral_items"):
                b_labels = q_module.get("behavioral_scale_labels", {})
                for bitem in q_module["behavioral_items"]:
                    bnum = bitem["number"]
                    bval = raw.get(str(bnum), "")
                    try:
                        bl = b_labels.get(int(bval), str(bval))
                    except (ValueError, TypeError):
                        bl = str(bval)
                    writer.writerow([q_code, q_name, bnum, bitem["text"], bval, bl])

            # Intensity items (C-SSRS)
            if q_module.get("intensity_items"):
                for iitem in q_module["intensity_items"]:
                    inum = iitem["number"]
                    ival = raw.get(str(inum), "")
                    try:
                        il = iitem["labels"].get(int(ival), str(ival))
                    except (ValueError, TypeError):
                        il = str(ival)
                    writer.writerow([q_code, q_name, inum, iitem["text"], ival, il])

            # Distress items (PQ-B)
            if q_module.get("has_distress_followup"):
                d_labels = q_module.get("distress_scale_labels", {})
                for item in q_module["items"]:
                    d_key = f"{item['number']}_distress"
                    d_val = raw.get(d_key, "")
                    if d_val not in ("", None):
                        try:
                            dl = d_labels.get(int(d_val), str(d_val))
                        except (ValueError, TypeError):
                            dl = str(d_val)
                        writer.writerow([
                            q_code, q_name, d_key,
                            f"מצוקה — {item['text']}", d_val, dl,
                        ])
        else:
            for num, val in raw.items():
                writer.writerow([q_code, q_name, num, "", val, ""])

    # Summary rows
    writer.writerow([])
    writer.writerow(["--- סיכום ציונים ---"])
    for q_code, q_data in session.get("questionnaires", {}).items():
        results = q_data.get("results", {})
        writer.writerow([q_code, q_data.get("name", q_code)])
        for key, val in results.items():
            if key not in ("endorsed_items",) and not isinstance(val, (dict, list)):
                writer.writerow(["", "", key, "", val])

    return buf.getvalue().encode("utf-8-sig")  # BOM for Excel Hebrew support


def _hex_to_rgb(hex_color):
    """Convert '#rrggbb' to (r, g, b) tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _export_session_pdf(session):
    """Export a session to a visually rich PDF matching the dashboard view."""
    pdf = FPDF()
    pdf.add_font("Heb", "", _HEBREW_FONT_PATH)
    pdf.add_font("Heb", "B", _HEBREW_FONT_PATH)
    pdf.set_text_shaping(use_shaping_engine=True)
    pdf.set_auto_page_break(auto=True, margin=20)

    PAGE_W = 190  # usable width (A4 - margins)
    BAR_W = 30    # width of the visual bar
    LH = 5        # line height

    def _w(text, size=10, bold=False, align="R"):
        pdf.set_font("Heb", "B" if bold else "", size)
        pdf.multi_cell(0, size * 0.55, text, new_x="LMARGIN", new_y="NEXT", align=align)

    def _line():
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    def _colored_header(text, hex_color):
        """Draw a colored subscale header bar."""
        r, g, b = _hex_to_rgb(hex_color)
        y = pdf.get_y()
        pdf.set_fill_color(r, g, b)
        pdf.rect(10, y, PAGE_W, 7, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Heb", "B", 9)
        pdf.set_xy(10, y + 0.5)
        pdf.cell(PAGE_W, 6, text, align="R")
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(y + 8)

    def _item_row(num, text, val, scale_min, scale_max, hex_color, is_rev=False, is_high=False):
        """Draw a single item row with visual bar."""
        if pdf.get_y() > 270:
            pdf.add_page()
        y = pdf.get_y()

        # Background for high items
        if is_high:
            pdf.set_fill_color(254, 242, 242)
            pdf.rect(10, y, PAGE_W, LH + 1, "F")
        else:
            pdf.set_fill_color(250, 251, 252)
            pdf.rect(10, y, PAGE_W, LH + 1, "F")

        # Item number
        pdf.set_font("Heb", "B", 7)
        pdf.set_text_color(100, 100, 100)
        pdf.set_xy(10, y)
        pdf.cell(8, LH, f"{num}.", align="R")

        # Item text (truncated)
        pdf.set_font("Heb", "", 7)
        pdf.set_text_color(50, 50, 50)
        pdf.set_xy(18, y)
        display_text = text[:70]
        if is_rev:
            display_text += "  [הפוך]"
        pdf.cell(PAGE_W - BAR_W - 30, LH, display_text, align="R")

        # Value badge
        r, g, b = _hex_to_rgb(hex_color)
        pdf.set_fill_color(r, g, b)
        val_str = str(val) if val is not None else "—"
        badge_x = PAGE_W - BAR_W - 5
        pdf.set_xy(badge_x, y)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Heb", "B", 7)
        pdf.cell(12, LH, val_str, align="C", fill=True)

        # Visual bar
        if val is not None and scale_max > scale_min:
            pct = (val - scale_min) / (scale_max - scale_min)
            bar_x = badge_x + 14
            # Background bar
            pdf.set_fill_color(232, 232, 240)
            pdf.rect(bar_x, y + 1.5, BAR_W, 2, "F")
            # Fill bar
            bar_color = _severity_bar_color(val, scale_min, scale_max,
                                            (scale_min + scale_max) / 2)
            cr, cg, cb = _hex_to_rgb(bar_color)
            pdf.set_fill_color(cr, cg, cb)
            pdf.rect(bar_x, y + 1.5, BAR_W * pct, 2, "F")

        pdf.set_text_color(0, 0, 0)
        pdf.set_y(y + LH + 1)

    # ---- Title page ----
    pdf.add_page()
    _w("דוח תוצאות שאלונים", size=20, bold=True)
    pdf.ln(4)

    client = session.get("client_number", "")
    ts = session.get("timestamp", "")
    try:
        dt = datetime.fromisoformat(ts)
        date_str = dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        date_str = ts
    _w(f"מטופל: {client}     תאריך: {date_str}", size=11)
    _line()
    pdf.ln(2)

    # ---- Per-questionnaire ----
    for q_code, q_data in session.get("questionnaires", {}).items():
        q_name = q_data.get("name", q_code)
        results = q_data.get("results", {})
        raw = q_data.get("raw_responses", {})

        # Find module
        q_module = None
        for qm in ALL_QUESTIONNAIRES.values():
            if qm["code"] == q_code:
                q_module = qm
                break

        # New page for each questionnaire
        if pdf.get_y() > 60:
            pdf.add_page()

        # ---- Questionnaire title ----
        _w(f"{q_code} — {q_name}", size=14, bold=True)
        pdf.ln(1)

        # ---- Score summary ----
        if "total" in results:
            _w(f"ציון כללי: {results['total']}  (טווח: {results.get('score_range', '')})", size=11)
        if "total_endorsed" in results:
            _w(f"פריטים מאושרים: {results['total_endorsed']}", size=11)
        if "total_distress" in results:
            _w(f"ציון מצוקה: {results['total_distress']}", size=11)
        if "ideation_level" in results:
            _w(f"רמת מחשבות אובדניות: {results['ideation_level']}/5 — "
               f"{results.get('ideation_description', '')}", size=11)
        if "total_mean" in results:
            _w(f"ציון ממוצע: {results['total_mean']}", size=11)
        if "total_score" in results:
            _w(f"ציון כללי: {results['total_score']}", size=11)

        if "severity" in results:
            _w(f"רמת חומרה: {results['severity']}", size=11, bold=True)
        if "interpretation" in results:
            _w(f"פירוש: {results['interpretation']}", size=9)
        if "clinical_note" in results:
            _w(f"הערה קלינית: {results['clinical_note']}", size=9, bold=True)
        if "behavior_summary" in results:
            _w(f"התנהגות (לאחרונה): {results['behavior_summary']}", size=9)
        # C-SSRS lifetime fields
        if "ideation_level_lifetime" in results:
            _w(f"מחשבות אובדניות (חיים): {results['ideation_level_lifetime']}/5 — "
               f"{results.get('ideation_description_lifetime', '')}", size=11)
        if "behavior_summary_lifetime" in results:
            _w(f"התנהגות אובדנית (חיים): {results['behavior_summary_lifetime']}", size=9)
        if results.get("attempt_count_recent"):
            _w(f"מספר ניסיונות (לאחרונה): {results['attempt_count_recent']}", size=9)
        if results.get("attempt_count_lifetime"):
            _w(f"מספר ניסיונות (חיים): {results['attempt_count_lifetime']}", size=9)
        if results.get("lethality") is not None:
            _w(f"תוצאה קטלנית: {results['lethality']}/5 — "
               f"{results.get('lethality_description', '')}", size=9)
        if results.get("intensity_total"):
            _w(f"עוצמת מחשבות (לאחרונה): {results['intensity_total']}/25", size=9)
        if results.get("intensity_total_lifetime"):
            _w(f"עוצמת מחשבות (חיים): {results['intensity_total_lifetime']}/25", size=9)

        # ---- AQ-specific: cutoff comparison ----
        if q_code == "AQ":
            total_aq = results.get("total", 0)
            pdf.ln(1)
            _w("ציוני סף:", size=10, bold=True)
            for cutoff_name, threshold in [
                ("ישראל — Golan & Milua (2006)", 22),
                ("יפן / אנגליה — Kurita et al. (2005)", 26),
                ("UK מקורי — Baron-Cohen et al. (2001)", 32),
            ]:
                status = "מעל הסף" if total_aq >= threshold else "מתחת לסף"
                _w(f"  {cutoff_name} (≥{threshold}): {status}", size=9)

        # ---- Subscale scores summary ----
        subscales = results.get("subscales", {})
        if subscales:
            pdf.ln(1)
            _w("תת-סולמות:", size=10, bold=True)
            for sub_name, sub_val in subscales.items():
                if isinstance(sub_val, dict):
                    if q_code == "AQ":
                        _w(f"  {sub_name}: {sub_val.get('score', '')}/10", size=9)
                    else:
                        parts = [f"{k}: {v}" for k, v in sub_val.items()
                                 if k not in ("items",)]
                        _w(f"  {sub_name} — {', '.join(parts)}", size=9)
                else:
                    _w(f"  {sub_name}: {sub_val}", size=9)

        clusters = results.get("clusters", {})
        if clusters:
            pdf.ln(1)
            _w("אשכולות:", size=10, bold=True)
            for ckey, cdata in clusters.items():
                _w(f"  {ckey} — {cdata.get('name', '')}: "
                   f"{cdata.get('score', '')}/{cdata.get('max', '')}", size=9)

        # ---- Visual item view grouped by subscale ----
        if q_module:
            pdf.ln(3)
            _w("תצוגת פריטים מלאה:", size=10, bold=True)
            pdf.ln(1)

            items = q_module["items"]
            scale_min = q_module["scale_min"]
            scale_max = q_module["scale_max"]
            reversed_items = set(q_module["reversed_items"])
            mid = (scale_min + scale_max) / 2

            subscale_map, subscale_order = _get_subscale_map(q_module)

            if subscale_map and subscale_order:
                # Grouped by subscale
                assigned = set()
                for sub_name, sub_color in subscale_order:
                    sub_items = [it for it in items
                                 if it["number"] in subscale_map
                                 and subscale_map[it["number"]][0] == sub_name]
                    if not sub_items:
                        continue
                    if pdf.get_y() > 260:
                        pdf.add_page()
                    _colored_header(sub_name, sub_color)
                    for item in sub_items:
                        num = item["number"]
                        val_raw = raw.get(str(num))
                        try:
                            val = int(val_raw) if val_raw is not None else None
                        except (ValueError, TypeError):
                            val = None
                        is_rev = num in reversed_items
                        effective = (scale_max - val + scale_min) if (is_rev and val is not None) else val
                        is_high = (effective is not None and effective > mid)
                        _item_row(num, item["text"], val, scale_min, scale_max,
                                  sub_color, is_rev, is_high)
                        assigned.add(num)

                # Unassigned items
                unassigned = [it for it in items if it["number"] not in assigned]
                if unassigned:
                    _colored_header("כללי", "#888888")
                    for item in unassigned:
                        num = item["number"]
                        val_raw = raw.get(str(num))
                        try:
                            val = int(val_raw) if val_raw is not None else None
                        except (ValueError, TypeError):
                            val = None
                        is_rev = num in reversed_items
                        effective = (scale_max - val + scale_min) if (is_rev and val is not None) else val
                        is_high = (effective is not None and effective > mid)
                        _item_row(num, item["text"], val, scale_min, scale_max,
                                  "#888888", is_rev, is_high)
            else:
                # No subscales — flat list with section grouping
                current_section = None
                for item in items:
                    if "section" in item and item["section"] != current_section:
                        current_section = item["section"]
                        if pdf.get_y() > 260:
                            pdf.add_page()
                        _colored_header(current_section, "#4a90d9")
                    num = item["number"]
                    val_raw = raw.get(str(num))
                    try:
                        val = int(val_raw) if val_raw is not None else None
                    except (ValueError, TypeError):
                        val = None
                    is_rev = num in reversed_items
                    effective = (scale_max - val + scale_min) if (is_rev and val is not None) else val
                    is_high = (effective is not None and effective > mid)
                    _item_row(num, item["text"], val, scale_min, scale_max,
                              "#4a90d9", is_rev, is_high)

            # PQ-B distress
            if q_module.get("has_distress_followup"):
                endorsed = [(it, raw.get(f"{it['number']}_distress"))
                            for it in items if raw.get(str(it["number"])) in (1, "1")]
                if endorsed:
                    pdf.ln(2)
                    _colored_header("פריטים שאושרו — דירוג מצוקה", "#e74c3c")
                    d_labels = q_module.get("distress_scale_labels", {})
                    for item, d_val in endorsed:
                        d_int = None
                        try:
                            d_int = int(d_val) if d_val is not None else None
                        except (ValueError, TypeError):
                            pass
                        d_text = f"{item['text']}  [מצוקה: {d_int or '—'}]"
                        _item_row(item["number"], d_text, d_int, 1, 5,
                                  "#e74c3c", is_high=True)

            # EAT-26 behavioral
            if q_module.get("behavioral_items"):
                pdf.ln(2)
                _colored_header("התנהגויות בששת החודשים האחרונים", "#c0392b")
                b_labels = q_module.get("behavioral_scale_labels", {})
                for bitem in q_module["behavioral_items"]:
                    bnum = bitem["number"]
                    bval_raw = raw.get(str(bnum))
                    try:
                        bval = int(bval_raw) if bval_raw is not None else None
                    except (ValueError, TypeError):
                        bval = None
                    _item_row(bnum, bitem["text"], bval, 0, 5,
                              "#c0392b", is_high=(bval is not None and bval >= 1))

            # C-SSRS intensity
            if q_module.get("intensity_items"):
                intensity = results.get("intensity", {})
                if intensity:
                    pdf.ln(2)
                    _colored_header("עוצמת המחשבות האובדניות", "#8e44ad")
                    for iitem in q_module["intensity_items"]:
                        inum = iitem["number"]
                        idata = intensity.get(inum)
                        if idata:
                            _item_row(inum, idata["label"], idata["value"], 1, 5,
                                      "#8e44ad", is_high=True)

        _line()
        pdf.ln(2)

    return bytes(pdf.output())


# ============================================================
# SCREEN 3: THERAPIST DASHBOARD
# ============================================================

def screen_dashboard():
    st.markdown(
        '<div class="setup-header">'
        '<h1>לוח בקרה</h1>'
        '<p>צפייה בתוצאות מטופלים</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button("חזרה", use_container_width=True):
        st.session_state.screen = "setup"
        st.rerun()

    st.markdown("---")

    sessions = load_all_sessions()

    if not sessions:
        st.info("אין עדיין תוצאות שמורות.")
        return

    # Group by client number
    clients = {}
    for s in sessions:
        cn = s.get("client_number", "לא ידוע")
        if cn not in clients:
            clients[cn] = []
        clients[cn].append(s)

    col_a, col_b = st.columns(2)
    with col_a:
        selected_client = st.selectbox(
            "מטופל",
            options=list(clients.keys()),
            key="dashboard_client",
        )

    if selected_client:
        client_sessions = clients[selected_client]

        session_labels = []
        for s in client_sessions:
            ts = s.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts)
                label = dt.strftime("%d/%m/%Y %H:%M")
            except (ValueError, TypeError):
                label = ts
            qs = ", ".join(s.get("questionnaires", {}).keys())
            session_labels.append(f"{label} — {qs}")

        with col_b:
            selected_idx = st.selectbox(
                "מפגש",
                options=range(len(client_sessions)),
                format_func=lambda i: session_labels[i],
                key="dashboard_session",
            )

        if selected_idx is not None:
            session = client_sessions[selected_idx]
            st.markdown("---")

            client_id = session.get("client_number", selected_client)
            date_label = session_labels[selected_idx].split(" — ")[0]

            st.markdown(
                f'<div class="results-box">'
                f'<strong>מטופל:</strong> {client_id} &nbsp;&nbsp; '
                f'<strong>תאריך:</strong> {date_label}'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Export buttons
            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                csv_bytes = _export_session_csv(session)
                st.download_button(
                    label="CSV ייצוא",
                    data=csv_bytes,
                    file_name=f"{client_id}_{date_label.replace('/', '-')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with exp_col2:
                pdf_bytes = _export_session_pdf(session)
                st.download_button(
                    label="PDF ייצוא",
                    data=pdf_bytes,
                    file_name=f"{client_id}_{date_label.replace('/', '-')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

            st.markdown("---")

            for q_code, q_data in session.get("questionnaires", {}).items():
                render_dashboard_results(q_code, q_data)


# ============================================================
# ROUTER
# ============================================================

screen = st.session_state.screen

if screen == "setup":
    screen_setup()
elif screen == "client":
    screen_client()
elif screen == "dashboard":
    screen_dashboard()
else:
    st.session_state.screen = "setup"
    st.rerun()
