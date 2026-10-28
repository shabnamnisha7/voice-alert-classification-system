"""Bento Grid dashboard for Real-Time Voice-Based Alert Classification."""

from pathlib import Path
import html

import pandas as pd
import streamlit as st

LOG_FILE = Path(__file__).resolve().parent / "alert_history.csv"

st.set_page_config(
    page_title="Real-Time Voice-Based Alert Classification Using Python and Arduino",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME + RESPONSIVE BENTO GRID STYLES
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        color-scheme: light;
        --bg: #f4f6fb;
        --surface: #ffffff;
        --surface-soft: #edf1f8;
        --text: #172033;
        --muted: #5e6a80;
        --border: #dce2ec;
        --accent: #4257d6;
        --accent-soft: #e8ebff;
        --high: #b42318;
        --high-bg: #feeceb;
        --medium: #875400;
        --medium-bg: #fff2cf;
        --low: #176b45;
        --low-bg: #def7e9;
        --shadow: 0 8px 28px rgba(29, 43, 75, .06);
        --radius: 22px;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            color-scheme: dark;
            --bg: #10141d;
            --surface: #191f2b;
            --surface-soft: #222a39;
            --text: #f0f3fa;
            --muted: #aab5c8;
            --border: #303a4c;
            --accent: #a8b2ff;
            --accent-soft: #2a3154;
            --high: #ffaaa4;
            --high-bg: #452323;
            --medium: #ffda86;
            --medium-bg: #46371c;
            --low: #8ee0b5;
            --low-bg: #173b2d;
            --shadow: 0 8px 28px rgba(0, 0, 0, .18);
        }
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1500px;
        padding: 1.6rem clamp(1rem, 3vw, 2.8rem) 3rem;
    }

    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div {
        background: transparent;
    }

    h1, h2, h3, p, label {
        color: var(--text);
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 22px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        color: var(--text);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -.6px;
    }

    .brand-icon {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        border-radius: 14px;
        background: var(--accent);
        color: white;
        font-size: 21px;
    }

    .system-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border: 1px solid var(--border);
        border-radius: 999px;
        background: var(--surface);
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
        white-space: nowrap;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #2eaf72;
        display: inline-block;
    }

    .bento-card {
        height: 100%;
        padding: 22px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        overflow: hidden;
    }

    .bento-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(29, 43, 75, .10);
        border-color: var(--accent);
    }

    .hero-card {
        min-height: 250px;
        padding: clamp(24px, 4vw, 42px);
        background: var(--accent);
        color: white;
        border: 1px solid transparent;
        position: relative;
    }

    .hero-card * { color: white; }

    .hero-kicker {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        opacity: .84;
        margin-bottom: 18px;
    }

    .hero-title {
        max-width: 700px;
        margin: 0 0 14px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(34px, 5vw, 61px);
        font-weight: 700;
        line-height: 1.02;
        letter-spacing: -2.5px;
    }

    .hero-description {
        max-width: 600px;
        font-size: 15px;
        line-height: 1.65;
        opacity: .9;
    }

    .hero-visual {
        height: 100%;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--surface-soft);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        position: relative;
    }

    .hero-orb {
        width: 132px;
        height: 132px;
        border-radius: 36px;
        background: linear-gradient(145deg, #8e9aff, #4257d6);
        transform: rotate(-12deg);
        box-shadow: 18px 18px 0 rgba(66, 87, 214, .13);
        position: relative;
    }

    .hero-orb::before, .hero-orb::after {
        content: "";
        position: absolute;
        border: 2px solid rgba(255,255,255,.8);
        border-radius: 28px;
        inset: 16px;
    }

    .hero-orb::after {
        inset: 34px;
        border-radius: 18px;
        background: rgba(255,255,255,.16);
    }

    .visual-caption {
        position: absolute;
        bottom: 14px;
        left: 16px;
        color: var(--muted);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .section-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin: 30px 0 14px;
    }

    .section-label h2 {
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -.5px;
    }

    .section-label span {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .8px;
        text-transform: uppercase;
    }

    .metric-card {
        min-height: 150px;
        padding: 19px;
        border: 1px solid var(--border);
        border-radius: 20px;
        background: var(--surface);
        box-shadow: var(--shadow);
        transition: transform .2s ease, border-color .2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--accent);
    }

    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
    }

    .metric-icon {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        border-radius: 11px;
        background: var(--surface-soft);
        color: var(--text);
        font-size: 16px;
    }

    .metric-value {
        margin: 17px 0 5px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(32px, 3vw, 43px);
        font-weight: 700;
        line-height: 1;
        letter-spacing: -1.5px;
        color: var(--text);
    }

    .metric-note {
        color: var(--muted);
        font-size: 11px;
    }

    .metric-high { background: var(--high-bg); }
    .metric-medium { background: var(--medium-bg); }
    .metric-low { background: var(--low-bg); }

    .metric-high .metric-value, .metric-high .metric-icon { color: var(--high); }
    .metric-medium .metric-value, .metric-medium .metric-icon { color: var(--medium); }
    .metric-low .metric-value, .metric-low .metric-icon { color: var(--low); }

    .card-title {
        margin: 0 0 5px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px;
        font-weight: 700;
        letter-spacing: -.3px;
        color: var(--text);
    }

    .card-subtitle {
        margin-bottom: 20px;
        color: var(--muted);
        font-size: 12px;
    }

    .priority-row {
        display: grid;
        grid-template-columns: 76px minmax(0, 1fr) 42px;
        align-items: center;
        gap: 12px;
        margin: 19px 0;
        color: var(--text);
        font-size: 12px;
        font-weight: 600;
    }

    .priority-name {
        display: flex;
        align-items: center;
        gap: 7px;
    }

    .priority-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot-high { background: var(--high); }
    .dot-medium { background: #d79b16; }
    .dot-low { background: #219568; }

    .priority-track {
        width: 100%;
        height: 9px;
        border-radius: 999px;
        background: var(--surface-soft);
        overflow: hidden;
    }

    .priority-fill {
        height: 100%;
        border-radius: 999px;
        animation: fill-in .8s ease both;
    }

    .fill-high { background: var(--high); }
    .fill-medium { background: #d79b16; }
    .fill-low { background: #219568; }

    .mini-stat {
        padding: 16px;
        border-radius: 16px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
    }

    .mini-stat-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .mini-stat-value {
        margin-top: 8px;
        font-size: 23px;
        font-weight: 700;
        color: var(--text);
    }

    .feed-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        padding: 12px 15px;
        border-radius: 14px;
        background: var(--surface-soft);
        margin-bottom: 14px;
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .stTextInput input, .stMultiSelect [data-baseweb="select"] > div {
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        min-height: 44px;
    }

    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-soft) !important;
    }

    .stButton > button, .stDownloadButton > button {
        min-height: 42px;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        color: var(--text) !important;
        font-weight: 700 !important;
        transition: transform .2s ease, border-color .2s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        transform: translateY(-1px);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 14px !important;
    }

    .footer-note {
        margin-top: 28px;
        padding: 18px 20px;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: var(--surface);
        color: var(--muted);
        font-size: 12px;
        line-height: 1.7;
    }

    .footer-note strong { color: var(--text); }

    @keyframes fill-in {
        from { width: 0; }
    }

    @media (max-width: 900px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.2rem 1.1rem 2rem;
        }
        .hero-title { font-size: clamp(34px, 6vw, 48px); }
    }

    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem .8rem 2rem;
        }
        .topbar {
            align-items: flex-start;
            flex-direction: column;
        }
        .hero-card { min-height: 0; padding: 24px; }
        .hero-title { font-size: 39px; letter-spacing: -1.7px; }
        .section-label h2 { font-size: 18px; }
        .bento-card { padding: 17px; }
        .system-pill { white-space: normal; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
            scroll-behavior: auto !important;
            transition-duration: .01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="font-size:12px;font-weight:700;letter-spacing:1px;
        color:var(--muted);margin-bottom:8px">COMMAND CENTER</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:27px;
        font-weight:700;line-height:1.05;margin-bottom:22px">
        Alert<br>Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("↻  Refresh data", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown("**DATA SOURCE**")
    st.code(LOG_FILE.name, language=None)
    st.caption("Run `control.py` separately to capture announcements.")
    st.markdown("---")
    st.caption("BUILD 02.0 · BENTO GRID")
    st.caption("Python · Speech Recognition · Arduino")

# ============================================================
# TOP BAR + HERO BENTO
# ============================================================

st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">⌁</div>
           <div>
    Real-Time Voice-Based Alert Classification
    <span style="color:var(--muted);font-weight:500">
        / Project Dashboard
    </span>
</div>
        </div>
        <div class="system-pill"><span class="status-dot"></span> Dashboard interface ready</div>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([1.75, 1], gap="medium")

with hero_left:
    st.markdown(
        """
        <div class="bento-card hero-card">
            <div class="hero-kicker">
    PROJECT DASHBOARD · PYTHON + ARDUINO
</div>

<div class="hero-title">
    Real-Time Voice-Based Alert Classification
</div>

<div class="hero-description">
    Using Python and Arduino to recognize spoken announcements,
    assign HIGH, MEDIUM, or LOW priority through rule-based
    classification, and display alerts through hardware indicators.
</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div class="hero-visual">
            <div class="hero-orb"></div>
            <div class="visual-caption">Signal processing · Module 001</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# LOAD AND VALIDATE CSV
# ============================================================

if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
    st.markdown('<div class="section-label"><h2>System overview</h2><span>01 / Status</span></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="bento-card" style="background:var(--surface-soft)">
            <div class="card-title">No alert history yet</div>
            <div style="color:var(--muted);font-size:14px;line-height:1.6">
                Start <b>control.py</b> and speak a test announcement.
                Recorded alerts will appear here automatically after refreshing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

try:
    df = pd.read_csv(LOG_FILE, encoding="utf-8-sig")
except (
    pd.errors.EmptyDataError,
    PermissionError,
    OSError,
    UnicodeDecodeError,
) as error:
    st.error(f"Could not read alert history: {error}")
    st.stop()

required = {"Timestamp", "Announcement", "Priority"}

if not required.issubset(df.columns):
    st.error("CSV columns are missing. Expected: Timestamp, Announcement, Priority.")
    st.stop()

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df["Priority"] = df["Priority"].astype(str).str.upper().str.strip()
df["Announcement"] = df["Announcement"].fillna("").astype(str)
df = df[df["Announcement"].str.strip().ne("")].copy()

# ============================================================
# METRIC BENTO CARDS
# ============================================================

total_count = len(df)
high_count = int((df["Priority"] == "HIGH").sum())
medium_count = int((df["Priority"] == "MEDIUM").sum())
low_count = int((df["Priority"] == "LOW").sum())

st.markdown(
    '<div class="section-label"><h2>System overview</h2><span>01 / Live metrics</span></div>',
    unsafe_allow_html=True,
)

metrics = [
    ("Total announcements", total_count, "All recorded events", "↗", ""),
    ("High priority", high_count, "Requires attention", "!", "metric-high"),
    ("Medium priority", medium_count, "Caution / review", "◷", "metric-medium"),
    ("Low priority", low_count, "Routine information", "✓", "metric-low"),
]

metric_cols = st.columns([1.15, 1, 1, 1], gap="medium")

for col, (label, value, note, icon, css_class) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card {css_class}">
                <div class="metric-top">
                    <span>{html.escape(label)}</span>
                    <span class="metric-icon">{html.escape(icon)}</span>
                </div>
                <div class="metric-value">{value:,}</div>
                <div class="metric-note">{html.escape(note)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# ANALYTICS BENTO GRID
# ============================================================

st.markdown(
    '<div class="section-label"><h2>Alert analytics</h2><span>02 / Distribution</span></div>',
    unsafe_allow_html=True,
)

analytics_col, summary_col = st.columns([1.65, 1], gap="medium")

priority_order = ["HIGH", "MEDIUM", "LOW"]
counts = df["Priority"].value_counts().reindex(priority_order, fill_value=0)
max_count = max(int(counts.max()), 1)

priority_styles = {
    "HIGH": ("dot-high", "fill-high"),
    "MEDIUM": ("dot-medium", "fill-medium"),
    "LOW": ("dot-low", "fill-low"),
}

bar_parts = []

for priority in priority_order:
    count = int(counts[priority])
    width = count / max_count * 100
    dot_class, fill_class = priority_styles[priority]
    bar_parts.append(
        f"""
        <div class="priority-row">
            <div class="priority-name">
                <span class="priority-dot {dot_class}"></span>{priority.title()}
            </div>
            <div class="priority-track">
                <div class="priority-fill {fill_class}" style="width:{width:.2f}%"></div>
            </div>
            <div style="text-align:right">{count}</div>
        </div>
        """
    )

with analytics_col:
    st.html(
        """
        <div class="bento-card">
            <div class="card-title">Priority distribution</div>
            <div class="card-subtitle">Announcement count by assigned class</div>
            """
        + "".join(bar_parts)
        + """
            <div style="margin-top:22px;padding-top:15px;border-top:1px solid var(--border);
            color:var(--muted);font-size:11px">
                Counts reflect the records currently stored in the CSV log.
            </div>
        </div>
        """
    )

with summary_col:
    high_share = (high_count / total_count * 100) if total_count else 0
    medium_share = (medium_count / total_count * 100) if total_count else 0
    low_share = (low_count / total_count * 100) if total_count else 0

    st.markdown(
        f"""
        <div class="bento-card" style="margin-bottom:16px">
            <div class="card-title">High-priority share</div>
            <div class="metric-value" style="font-size:39px">{high_share:.1f}%</div>
            <div class="card-subtitle" style="margin:7px 0 0">
                {high_count} of {total_count} recorded announcements
            </div>
        </div>
        <div class="bento-card">
            <div class="card-title">Priority mix</div>
            <div style="display:grid;gap:12px;margin-top:16px">
                <div class="mini-stat">
                    <div class="mini-stat-label">Medium share</div>
                    <div class="mini-stat-value">{medium_share:.1f}%</div>
                </div>
                <div class="mini-stat">
                    <div class="mini-stat-label">Low share</div>
                    <div class="mini-stat-value">{low_share:.1f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# ALERT HISTORY: FILTER, SEARCH, SORT, EXPORT
# ============================================================

st.markdown(
    '<div class="section-label"><h2>Alert history</h2><span>03 / Incident log</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="bento-card" style="margin-bottom:16px">
        <div class="card-title">Find an announcement</div>
        <div class="card-subtitle" style="margin-bottom:0">
            Filter by priority or search announcement text.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

filter_col, search_col = st.columns([1, 1.5], gap="medium")
priority_options = ["HIGH", "MEDIUM", "LOW"]

with filter_col:
    selected_priorities = st.multiselect(
        "Filter by priority",
        options=priority_options,
        default=priority_options,
    )

with search_col:
    search_text = st.text_input(
        "Search announcement",
        placeholder="Search for words or phrases...",
    )

filtered = df[df["Priority"].isin(selected_priorities)].copy()

if search_text.strip():
    filtered = filtered[
        filtered["Announcement"].str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

display_df = filtered.sort_values(
    "Timestamp",
    ascending=False,
    na_position="last",
).copy()

st.markdown(
    f"""
    <div class="feed-header">
        <span>Filtered results</span>
        <span>{len(display_df)} record(s) · Newest first</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=390,
)

csv_bytes = display_df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="Download filtered history as CSV",
    data=csv_bytes,
    file_name="filtered_alert_history.csv",
    mime="text/csv",
    use_container_width=True,
)

# ============================================================
# SAFETY NOTE
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        <strong>System limitations</strong><br>
        This educational prototype uses keyword-based rules, not a trained AI model.
        Speech recognition requires an online service and may mishear speech.
        Unfamiliar wording can cause classification errors. Do not rely on this
        prototype as the sole means of communicating or responding to emergencies.
    </div>
    """,
    unsafe_allow_html=True,
)
