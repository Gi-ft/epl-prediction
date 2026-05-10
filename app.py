import os
import pickle
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib.patches import Patch
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(
    page_title="PL Simulator",
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ARSENAL = "#ef233c"
CITY = "#6cabdd"
GOLD = "#f7c948"
INK = "#f6f7fb"
MUTED = "#9aa3b2"
PANEL = "#121826"
PANEL_SOFT = "#182033"
GRID = "#2b3448"
SUCCESS = "#67d391"
WARNING = "#f6ad55"


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: "Inter", sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 18% 8%, rgba(239, 35, 60, 0.20), transparent 28rem),
            radial-gradient(circle at 86% 2%, rgba(108, 171, 221, 0.18), transparent 24rem),
            linear-gradient(180deg, #080b12 0%, #0d111c 46%, #090c13 100%);
        color: {INK};
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 2.4rem;
        padding-bottom: 2.6rem;
        max-width: 1220px;
    }}

    .hero {{
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 1.6rem 1.8rem;
        background: linear-gradient(135deg, rgba(18, 24, 38, 0.92), rgba(18, 24, 38, 0.62));
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
    }}

    .eyebrow {{
        color: {GOLD};
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }}

    .hero-title {{
        color: {INK};
        font-size: clamp(2.15rem, 5vw, 4.2rem);
        font-weight: 800;
        line-height: 0.98;
        margin: 0;
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 1rem;
        margin: 0.8rem 0 0;
        max-width: 56rem;
    }}

    .section-label {{
        color: {MUTED};
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        margin: 1.65rem 0 0.85rem;
    }}

    .race-card {{
        position: relative;
        min-height: 9.2rem;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: linear-gradient(180deg, rgba(24, 32, 51, 0.96), rgba(18, 24, 38, 0.96));
        overflow: hidden;
    }}

    .race-card:before {{
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 0.35rem;
        background: var(--accent);
    }}

    .race-card-title {{
        color: {MUTED};
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        margin: 0 0 0.65rem;
    }}

    .race-card-value {{
        color: var(--accent);
        font-size: clamp(2.4rem, 6vw, 4.4rem);
        font-weight: 800;
        line-height: 1;
        margin: 0;
    }}

    .race-card-note {{
        color: {MUTED};
        font-size: 0.84rem;
        margin: 0.7rem 0 0;
    }}

    .race-card-bar {{
        height: 0.5rem;
        border-radius: 99px;
        background: rgba(255, 255, 255, 0.08);
        overflow: hidden;
        margin-top: 1rem;
    }}

    .race-card-fill {{
        width: var(--pct);
        height: 100%;
        border-radius: inherit;
        background: var(--accent);
    }}

    .stat-card {{
        height: 100%;
        padding: 1rem 1.05rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(18, 24, 38, 0.9);
    }}

    .stat-card-label {{
        color: {MUTED};
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0;
    }}

    .stat-card-value {{
        color: {INK};
        font-size: 2rem;
        font-weight: 800;
        margin: 0.35rem 0 0.2rem;
        line-height: 1.05;
    }}

    .stat-card-note {{
        color: {MUTED};
        font-size: 0.82rem;
        margin: 0;
    }}

    .chart-panel {{
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(18, 24, 38, 0.88);
    }}

    .insight-box {{
        padding: 1rem 1.05rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: linear-gradient(180deg, rgba(24, 32, 51, 0.92), rgba(18, 24, 38, 0.92));
    }}

    .insight-title {{
        color: {INK};
        font-size: 0.92rem;
        font-weight: 700;
        margin: 0 0 0.3rem;
    }}

    .insight-copy {{
        color: {MUTED};
        font-size: 0.88rem;
        margin: 0;
        line-height: 1.5;
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        overflow: hidden;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.45rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        color: {MUTED};
        padding: 0.6rem 1rem;
    }}

    .stTabs [aria-selected="true"] {{
        background: rgba(24, 32, 51, 1);
        color: {INK};
    }}

    hr {{
        border-color: rgba(255, 255, 255, 0.08);
        margin: 1.7rem 0 0.2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


plt.rcParams.update(
    {
        "figure.facecolor": PANEL,
        "axes.facecolor": PANEL,
        "axes.edgecolor": GRID,
        "axes.labelcolor": MUTED,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "grid.color": GRID,
        "grid.alpha": 0.45,
        "text.color": INK,
        "legend.facecolor": PANEL_SOFT,
        "legend.edgecolor": GRID,
        "font.family": "sans-serif",
    }
)


@st.cache_data(show_spinner=False)
def load_simulation_data():
    # Get the directory where app.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "sim_results.pkl")
    
    with open(file_path, "rb") as f:
        return pickle.load(f)


def get_active_simulation_data():
    if "live_sim_data" in st.session_state:
        return st.session_state["live_sim_data"], True
    return load_simulation_data(), False


def build_strength_lookup(standings_df):
    if "strength" in standings_df.columns:
        return dict(zip(standings_df["team_id"], standings_df["strength"]))

    if {"points", "played", "goal_difference"}.issubset(standings_df.columns):
        played = standings_df["played"].replace(0, np.nan)
        ppg = standings_df["points"] / played
        gd_pg = standings_df["goal_difference"] / played
        strength_series = (0.65 * ppg.fillna(0)) + (0.35 * gd_pg.fillna(0))
        return dict(zip(standings_df["team_id"], strength_series))

    raise ValueError(
        "The standings table must include either a `strength` column or the fields "
        "`points`, `played`, and `goal_difference`."
    )


def render_live_results(results):
    if isinstance(results, pd.DataFrame):
        st.dataframe(results, use_container_width=True, hide_index=True)
        return

    if isinstance(results, dict):
        simple_metrics = {}

        for key, value in results.items():
            if isinstance(value, pd.DataFrame):
                st.markdown(f"**{str(key).replace('_', ' ').title()}**")
                st.dataframe(value, use_container_width=True, hide_index=True)
            elif isinstance(value, (list, tuple)) and value and isinstance(value[0], dict):
                st.markdown(f"**{str(key).replace('_', ' ').title()}**")
                st.dataframe(pd.DataFrame(value), use_container_width=True, hide_index=True)
            else:
                simple_metrics[key] = value

        if simple_metrics:
            st.write(simple_metrics)
        return

    st.write(results)


def normalize_live_results(results, standings_df):
    if not isinstance(results, dict):
        return results

    normalized = results.copy()
    if (
        "team_probs" in normalized
        and isinstance(normalized["team_probs"], pd.DataFrame)
        and "team_name" not in normalized["team_probs"].columns
    ):
        name_col = "team_name" if "team_name" in standings_df.columns else "name" if "name" in standings_df.columns else None
        if name_col is not None:
            name_lookup = dict(zip(standings_df["team_id"], standings_df[name_col]))
            normalized["team_probs"] = normalized["team_probs"].copy()
            normalized["team_probs"]["team_name"] = normalized["team_probs"]["team_id"].map(name_lookup)

    return normalized


def save_simulation_data(simulation_data):
    with open("sim_results.pkl", "wb") as f:
        pickle.dump(simulation_data, f)


def get_default_database_url():
    default_db_url = "mysql+pymysql://user:password@localhost/your_db"
    try:
        if "database_url" in st.secrets:
            return st.secrets["database_url"]

        if "database" in st.secrets and "url" in st.secrets["database"]:
            return st.secrets["database"]["url"]

        return default_db_url
    except StreamlitSecretNotFoundError:
        return default_db_url


# Try to load simulation data (from pickle or live session state)
sim_data = None
using_live_data = False

if "live_sim_data" in st.session_state:
    sim_data = st.session_state["live_sim_data"]
    using_live_data = True
else:
    try:
        sim_data, _ = load_simulation_data()
    except FileNotFoundError:
        sim_data = None

# Validate loaded data
if sim_data is not None:
    required_keys = [
        "arsenal_points",
        "city_points",
        "point_diff",
        "arsenal_progress",
        "city_progress",
    ]
    missing_keys = [key for key in required_keys if key not in sim_data]
    if missing_keys:
        st.warning(f"Simulation data missing keys: {', '.join(missing_keys)}")
        sim_data = None

# Extract data if available
if sim_data is not None:
    arsenal_points = np.asarray(sim_data["arsenal_points"])
    city_points = np.asarray(sim_data["city_points"])
    point_diff = np.asarray(sim_data["point_diff"])
    arsenal_progress = np.asarray(sim_data["arsenal_progress"])
    city_progress = np.asarray(sim_data["city_progress"])
    results_df = sim_data.get("results", pd.DataFrame())
    team_probs = sim_data.get("team_probs")

    if team_probs is None and isinstance(results_df, pd.DataFrame):
        if {"title_probability", "team_name"}.issubset(results_df.columns):
            team_probs = results_df.copy()

    diff_series = pd.Series(point_diff)
    simulation_count = len(diff_series)

if sim_data is None:
    # No simulation data available - show fallback UI
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Premier League Simulator</div>
            <h1 class="hero-title">No Simulation Data Available</h1>
            <p class="hero-subtitle">
                The simulation results file was not found. 
                Run a live simulation from your MySQL database to generate fresh predictions.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Live Database Simulation</div>', unsafe_allow_html=True)
    
    default_db_url = get_default_database_url()
    
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.caption("Run a fresh title simulation from the current MySQL standings and scheduled fixtures.")
    
    live_col1, live_col2 = st.columns([3, 1])
    with live_col1:
        db_url = st.text_input(
            "Database URL",
            value=default_db_url,
            type="password",
            help="Example: mysql+pymysql://root:password@localhost/epl_database",
        )
    with live_col2:
        live_simulations = st.number_input(
            "Simulations",
            min_value=100,
            max_value=50000,
            value=1000,
            step=100,
        )
    
    if st.button("Run Live Simulation", type="primary", use_container_width=True):
        try:
            from simulation_engine import run_simulation
            from sqlalchemy import create_engine
            
            engine = create_engine(db_url)
            standings = pd.read_sql("SELECT * FROM standings", engine)
            matches = pd.read_sql(
                """
                SELECT * FROM matches
                WHERE status IN ('SCHEDULED', 'TIMED')
                """,
                engine,
            )
            
            if standings.empty:
                st.error("Standings table is empty.")
            elif matches.empty:
                st.error("No upcoming matches found in the database.")
            else:
                points = dict(zip(standings["team_id"], standings["points"]))
                goal_diff = dict(zip(standings["team_id"], standings["goal_difference"]))
                team_strength = build_strength_lookup(standings)

                live_results = run_simulation(
                    matches,
                    points,
                    goal_diff,
                    team_strength,
                    simulations=int(live_simulations),
                )
                normalized_live_results = normalize_live_results(live_results, standings)
                save_simulation_data(normalized_live_results)
                load_simulation_data.clear()
                st.session_state["live_sim_data"] = normalized_live_results
                st.session_state["live_sim_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()
        except Exception as e:
            st.error(f"Live simulation failed: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # Stop here - don't try to render dashboard without data

# Continue with normal dashboard if we have data
arsenal_win = float((diff_series > 0).mean() * 100)
city_win = float((diff_series < 0).mean() * 100)
draw_finish = float((diff_series == 0).mean() * 100)

mean_arsenal = float(np.mean(arsenal_points))
mean_city = float(np.mean(city_points))
std_arsenal = float(np.std(arsenal_points))
std_city = float(np.std(city_points))
median_arsenal = float(np.median(arsenal_points))
median_city = float(np.median(city_points))
p25_arsenal, p75_arsenal = np.percentile(arsenal_points, [25, 75])
p25_city, p75_city = np.percentile(city_points, [25, 75])

average_gap = mean_arsenal - mean_city
gap_color = ARSENAL if average_gap > 0 else CITY if average_gap < 0 else GOLD
close_race_pct = float((np.abs(point_diff) <= 3).mean() * 100)
arsenal_95_plus = float((arsenal_points >= 95).mean() * 100)
city_95_plus = float((city_points >= 95).mean() * 100)
volatility = float(np.std(point_diff))
max_points = int(max(arsenal_points.max(), city_points.max()))
lead_margin = abs(arsenal_win - city_win)
frontrunner = "Arsenal" if arsenal_win >= city_win else "Man City"
frontrunner_color = ARSENAL if frontrunner == "Arsenal" else CITY
race_profile = (
    "tight run-in"
    if lead_margin < 10
    else "clear edge"
    if lead_margin < 25
    else "strong favorite"
)

matchdays = np.arange(1, len(arsenal_progress) + 1)
arsenal_momentum = pd.Series(arsenal_progress).diff().rolling(window=5, min_periods=1).mean().fillna(0)
city_momentum = pd.Series(city_progress).diff().rolling(window=5, min_periods=1).mean().fillna(0)


st.markdown(
    f"""
    <section class="hero">
        <div class="eyebrow">Monte Carlo title race model</div>
        <h1 class="hero-title">Premier League Simulator</h1>
        <p class="hero-subtitle">
            Arsenal vs Manchester City probability, season trajectory, statistical ranges,
            and simulation-backed match context from {simulation_count:,} runs.
        </p>
        <p class="hero-subtitle" style="margin-top: 0.55rem;">
            <span style="color: {frontrunner_color}; font-weight: 700;">{frontrunner}</span>
            projects as the {race_profile} with a title-odds gap of {lead_margin:.1f} percentage points.
        </p>
        <p class="hero-subtitle" style="margin-top: 0.55rem;">
            Source:
            <span style="color: {GOLD}; font-weight: 700;">{"Live database simulation" if using_live_data else "Saved simulation snapshot"}</span>
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-label">Title Race Odds</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="race-card" style="--accent: {ARSENAL};">
            <p class="race-card-title">Arsenal</p>
            <p class="race-card-value">{arsenal_win:.1f}%</p>
            <div class="race-card-bar">
                <div class="race-card-fill" style="--pct: {arsenal_win:.1f}%;"></div>
            </div>
            <p class="race-card-note">Average finish: {mean_arsenal:.1f} pts | Median: {median_arsenal:.0f} pts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="race-card" style="--accent: {CITY};">
            <p class="race-card-title">Man City</p>
            <p class="race-card-value">{city_win:.1f}%</p>
            <div class="race-card-bar">
                <div class="race-card-fill" style="--pct: {city_win:.1f}%;"></div>
            </div>
            <p class="race-card-note">Average finish: {mean_city:.1f} pts | Median: {median_city:.0f} pts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Key Statistics</div>', unsafe_allow_html=True)

stat_cols = st.columns(4)

stat_cards = [
    ("Average Gap", f"{average_gap:+.1f}", f"Arsenal - City expected point difference", gap_color),
    ("Level Finish", f"{draw_finish:.1f}%", "Simulations ending on equal points", GOLD),
    ("Close Race", f"{close_race_pct:.1f}%", "Finishes decided by 3 points or fewer", WARNING),
    ("Max Points", f"{max_points}", "Highest final points total observed", SUCCESS),
]

for col, (label, value, note, color) in zip(stat_cols, stat_cards):
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <p class="stat-card-label">{label}</p>
                <p class="stat-card-value" style="color: {color};">{value}</p>
                <p class="stat-card-note">{note}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


tab1, tab2, tab3 = st.tabs(
    ["Race Progression", "Distribution Analysis", "League Outlook"]
)

with tab1:
    st.markdown('<div class="section-label">Season Trajectory</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(12, 6.6),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1.4]},
    )

    ax1.plot(matchdays, arsenal_progress, linewidth=3, color=ARSENAL, label="Arsenal")
    ax1.plot(matchdays, city_progress, linewidth=3, color=CITY, label="Man City")
    ax1.fill_between(matchdays, arsenal_progress, color=ARSENAL, alpha=0.10)
    ax1.fill_between(matchdays, city_progress, color=CITY, alpha=0.10)
    ax1.set_ylabel("Points")
    ax1.set_title("Average Season Trajectory", pad=12, fontweight="700")
    ax1.grid(axis="y")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", framealpha=0.85)

    ax2.plot(matchdays, arsenal_momentum, linewidth=2.4, color=ARSENAL, label="Arsenal momentum")
    ax2.plot(matchdays, city_momentum, linewidth=2.4, color=CITY, label="Man City momentum")
    ax2.axhline(0, color=GRID, linewidth=1.2, linestyle="--")
    ax2.fill_between(matchdays, arsenal_momentum, 0, color=ARSENAL, alpha=0.10)
    ax2.fill_between(matchdays, city_momentum, 0, color=CITY, alpha=0.10)
    ax2.set_xlabel("Matchday")
    ax2.set_ylabel("PPG swing")
    ax2.set_title("5-match rolling momentum", pad=10, fontweight="700")
    ax2.grid(axis="y")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    insight_cols = st.columns(3)
    insights = [
        (
            "Arsenal ceiling",
            f"{arsenal_95_plus:.1f}% of simulations finish with Arsenal on 95 or more points.",
        ),
        (
            "City ceiling",
            f"{city_95_plus:.1f}% of simulations finish with Man City on 95 or more points.",
        ),
        (
            "Race tension",
            f"{close_race_pct:.1f}% of runs finish within a single late swing of 3 points.",
        ),
    ]

    for col, (title, copy) in zip(insight_cols, insights):
        with col:
            st.markdown(
                f"""
                <div class="insight-box">
                    <p class="insight-title">{title}</p>
                    <p class="insight-copy">{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab2:
    st.markdown('<div class="section-label">Outcome Distributions</div>', unsafe_allow_html=True)
    dist_col1, dist_col2 = st.columns(2)

    with dist_col1:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(7, 4.6))
        ax1.hist(arsenal_points, bins=24, alpha=0.74, label="Arsenal", color=ARSENAL, edgecolor=PANEL)
        ax1.hist(city_points, bins=24, alpha=0.70, label="Man City", color=CITY, edgecolor=PANEL)
        ax1.axvline(mean_arsenal, color=ARSENAL, linestyle="--", linewidth=1.8)
        ax1.axvline(mean_city, color=CITY, linestyle="--", linewidth=1.8)
        ax1.set_title("Points Distribution", pad=14, fontweight="700")
        ax1.set_xlabel("Final points")
        ax1.set_ylabel("Simulations")
        ax1.grid(axis="y")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.legend(framealpha=0.85)
        fig1.tight_layout()
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)
        st.markdown("</div>", unsafe_allow_html=True)

    with dist_col2:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(7, 4.6))
        counts, edges = np.histogram(point_diff, bins=24)
        centers = (edges[:-1] + edges[1:]) / 2
        colors = [ARSENAL if center > 0 else CITY if center < 0 else GOLD for center in centers]
        ax2.bar(centers, counts, width=(edges[1] - edges[0]) * 0.9, color=colors, alpha=0.88)
        ax2.axvline(0, color=GOLD, linewidth=1.8, linestyle="--")
        ax2.set_title("Point Difference (Arsenal - City)", pad=14, fontweight="700")
        ax2.set_xlabel("Point difference")
        ax2.set_ylabel("Simulations")
        ax2.grid(axis="y")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.legend(
            handles=[
                Patch(color=ARSENAL, label="Arsenal ahead"),
                Patch(color=CITY, label="Man City ahead"),
                Patch(color=GOLD, label="Level finish"),
            ],
            framealpha=0.85,
        )
        fig2.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    summary_cols = st.columns(4)
    summary_cards = [
        ("Arsenal Range", f"{p25_arsenal:.0f}-{p75_arsenal:.0f}", f"IQR | sd {std_arsenal:.1f}", ARSENAL),
        ("City Range", f"{p25_city:.0f}-{p75_city:.0f}", f"IQR | sd {std_city:.1f}", CITY),
        ("Gap Volatility", f"{volatility:.1f}", "Std deviation of title margin", GOLD),
        ("Likely Winner", "Arsenal" if arsenal_win >= city_win else "Man City", "Based on simulated title share", ARSENAL if arsenal_win >= city_win else CITY),
    ]

    for col, (label, value, note, color) in zip(summary_cols, summary_cards):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <p class="stat-card-label">{label}</p>
                    <p class="stat-card-value" style="color: {color};">{value}</p>
                    <p class="stat-card-note">{note}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab3:
    st.markdown('<div class="section-label">League Outlook</div>', unsafe_allow_html=True)

    if isinstance(team_probs, pd.DataFrame) and not team_probs.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Full League Title Probabilities</div>', unsafe_allow_html=True)

        team_probs = team_probs.sort_values("title_probability", ascending=False)
        team_label_col = "team_name" if "team_name" in team_probs.columns else "team_id"
        display_df = team_probs.copy()
        if team_label_col == "team_name":
            display_df["team_name"] = display_df["team_name"].astype(str).str.replace(" FC", "", regex=False)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "team_name": st.column_config.TextColumn("Team"),
                "team_id": st.column_config.TextColumn("Team ID"),
                "title_probability": st.column_config.ProgressColumn(
                    "Title Probability",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            },
        )

        fig3, ax3 = plt.subplots(figsize=(9, 5.4))
        plot_df = display_df.iloc[::-1]
        bar_colors = [
            ARSENAL
            if "Arsenal" in str(team)
            else CITY
            if "City" in str(team)
            else GOLD
            for team in plot_df[team_label_col]
        ]

        ax3.barh(plot_df[team_label_col].astype(str), plot_df["title_probability"], color=bar_colors, alpha=0.88)
        ax3.set_xlabel("Win %")
        ax3.set_title("Title Probability by Team", pad=14, fontweight="700")
        ax3.grid(axis="x")
        ax3.grid(axis="y", alpha=0)
        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)

        max_prob = float(display_df["title_probability"].max())
        ax3.set_xlim(0, max(max_prob * 1.15, 1))

        for index, value in enumerate(plot_df["title_probability"]):
            ax3.text(value + max_prob * 0.02, index, f"{value:.1f}%", va="center", color=INK, fontsize=10)

        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        top_two = display_df.head(2)
        if len(top_two) == 2:
            first_team = str(top_two.iloc[0][team_label_col]).replace(" FC", "")
            second_team = str(top_two.iloc[1][team_label_col]).replace(" FC", "")
            first_prob = float(top_two.iloc[0]["title_probability"])
            second_prob = float(top_two.iloc[1]["title_probability"])
            st.markdown(
                f"""
                <div class="insight-box" style="margin-top: 1rem;">
                    <p class="insight-title">League takeaway</p>
                    <p class="insight-copy">
                        {first_team} leads the wider title picture at {first_prob:.1f}%,
                        ahead of {second_team} on {second_prob:.1f}%. Everyone else is currently in long-shot territory.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif isinstance(results_df, pd.DataFrame) and not results_df.empty:
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        st.info("Additional simulation output is available above, but no dedicated `team_probs` table was found.")
    else:
        st.info("No league-wide title probability table is available in `sim_results.pkl`.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Live Database Simulation</div>', unsafe_allow_html=True)

    default_db_url = get_default_database_url()

    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.caption("Run a fresh title simulation from the current MySQL standings and scheduled fixtures.")

    live_col1, live_col2 = st.columns([3, 1])
    with live_col1:
        db_url = st.text_input(
            "Database URL",
            value=default_db_url,
            type="password",
            help="Example: mysql+pymysql://root:password@localhost/epl_database",
        )
    with live_col2:
        live_simulations = st.number_input(
            "Simulations",
            min_value=100,
            max_value=50000,
            value=1000,
            step=100,
        )

    if st.button("Run Live Simulation", type="primary", use_container_width=True):
        try:
            from simulation_engine import run_simulation
            from sqlalchemy import create_engine

            engine = create_engine(db_url)
            standings = pd.read_sql("SELECT * FROM standings", engine)
            matches = pd.read_sql(
                """
                SELECT * FROM matches
                WHERE status IN ('SCHEDULED', 'TIMED')
                """,
                engine,
            ).sort_values("match_date")

            if matches.empty:
                st.warning(
                    "No future fixtures were found with status `SCHEDULED` or `TIMED`, "
                    "so a live simulation cannot be run yet."
                )
                st.stop()

            points = dict(zip(standings["team_id"], standings["points"]))
            goal_diff = dict(zip(standings["team_id"], standings["goal_difference"]))
            team_strength = build_strength_lookup(standings)

            with st.spinner("Running live simulation from current database state..."):
                live_results = run_simulation(
                    matches,
                    points,
                    goal_diff,
                    team_strength,
                    simulations=int(live_simulations),
                )

            normalized_live_results = normalize_live_results(live_results, standings)
            save_simulation_data(normalized_live_results)
            load_simulation_data.clear()
            st.session_state["live_sim_data"] = normalized_live_results
            st.session_state["live_sim_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()
        except Exception as exc:
            st.error(f"Live simulation failed: {exc}")

    if using_live_data:
        status_col, action_col = st.columns([2, 1])
        with status_col:
            timestamp = st.session_state.get("live_sim_timestamp")
            if timestamp:
                st.success(f"Dashboard is currently showing live simulation results from {timestamp}.")
            else:
                st.success("Dashboard is currently showing live simulation results.")
        with action_col:
            if st.button("Clear Live Simulation", use_container_width=True):
                st.session_state.pop("live_sim_data", None)
                st.session_state.pop("live_sim_timestamp", None)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
