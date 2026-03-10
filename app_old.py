import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk

# -----------------------------
# Page config
# -----------------------------




st.set_page_config(
    page_title="Global Conflict Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59,130,246,0.14), transparent 30%),
            radial-gradient(circle at top right, rgba(168,85,247,0.12), transparent 28%),
            radial-gradient(circle at bottom left, rgba(34,197,94,0.10), transparent 25%),
            linear-gradient(135deg, #06131f 0%, #0b1220 45%, #111827 100%);
        color: #e5eef9;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        padding: 1.1rem 1.1rem 0.9rem 1.1rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.22);
        margin-bottom: 1rem;
    }

    .metric-title {
        font-size: 0.9rem;
        color: rgba(229, 238, 249, 0.72);
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.95rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }

    .metric-sub {
        margin-top: 0.35rem;
        font-size: 0.82rem;
        color: rgba(229, 238, 249, 0.62);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.15rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: rgba(229, 238, 249, 0.74);
        margin-bottom: 1.2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(8, 15, 26, 0.82);
        border-right: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    /* Streamlit widget labels */
    label, .stMarkdown, .stCaption, .stText {
        color: #e5eef9 !important;
    }

    /* Dataframe container */
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.03);
        border-radius: 18px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0)
    df = df.dropna(subset=["event_date", "latitude", "longitude"])
    return df

@st.cache_data
def load_gdelt_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "seendate" in df.columns:
        df["seendate"] = pd.to_datetime(df["seendate"], errors="coerce")

    return df

def metric_card(title: str, value: str, subtext: str = ""):
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_color_map(event_types):
    palette = [
        [99, 102, 241],
        [236, 72, 153],
        [34, 197, 94],
        [245, 158, 11],
        [59, 130, 246],
        [168, 85, 247],
        [239, 68, 68],
        [20, 184, 166],
        [251, 191, 36],
        [244, 114, 182],
    ]
    unique = sorted([e for e in event_types if pd.notna(e)])
    return {event: palette[i % len(palette)] for i, event in enumerate(unique)}


# -----------------------------
# Load data
# -----------------------------
DATA_PATH = "data/processed/acled_events_cleaned.csv"
GDELT_PATH = "data/processed/gdelt_war_news_cleaned.csv"

df = load_data(DATA_PATH)
gdelt_df = load_gdelt_data(GDELT_PATH)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.markdown("## Filters")

countries = sorted(df["country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries[:1] if countries else [],
)

event_types = sorted(df["event_type"].dropna().unique().tolist())
selected_event_types = st.sidebar.multiselect(
    "Event Type",
    options=event_types,
    default=event_types,
)

min_date = df["event_date"].min().date()
max_date = df["event_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

show_only_fatal = st.sidebar.checkbox("Only events with fatalities", value=False)

filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

if selected_event_types:
    filtered_df = filtered_df[filtered_df["event_type"].isin(selected_event_types)]

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        (filtered_df["event_date"].dt.date >= start_date)
        & (filtered_df["event_date"].dt.date <= end_date)
    ]

if show_only_fatal:
    filtered_df = filtered_df[filtered_df["fatalities"] > 0]

filtered_df = filtered_df.sort_values("event_date")

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="hero-title">Global Conflict Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Minimal glass-style dashboard for structured conflict monitoring using ACLED data.</div>',
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.warning("No data matches the current filters. Try widening the date range or removing a filter.")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
total_events = len(filtered_df)
total_fatalities = int(filtered_df["fatalities"].sum())
countries_count = filtered_df["country"].nunique()
latest_event_date = filtered_df["event_date"].max().strftime("%d %b %Y")

k1, k2, k3, k4 = st.columns(4)
with k1:
    metric_card("Total Events", f"{total_events:,}", "Filtered conflict events")
with k2:
    metric_card("Total Fatalities", f"{total_fatalities:,}", "Reported fatalities in current view")
with k3:
    metric_card("Countries", f"{countries_count}", "Countries in filtered dataset")
with k4:
    metric_card("Latest Event", latest_event_date, "Most recent event date")

# -----------------------------
# Prepare map data
# -----------------------------
color_map = build_color_map(filtered_df["event_type"].unique())
map_df = filtered_df.copy()
map_df["color"] = map_df["event_type"].map(color_map)
map_df["radius"] = map_df["fatalities"].fillna(0).clip(lower=0)
map_df["radius"] = (map_df["radius"] * 1200 + 12000).clip(12000, 50000)

view_state = pdk.ViewState(
    latitude=float(map_df["latitude"].mean()),
    longitude=float(map_df["longitude"].mean()),
    zoom=4,
    pitch=35,
)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position="[longitude, latitude]",
    get_fill_color="color",
    get_radius="radius",
    pickable=True,
    opacity=0.72,
    stroked=True,
    filled=True,
    radius_min_pixels=4,
    radius_max_pixels=28,
    line_width_min_pixels=1,
    get_line_color=[255, 255, 255, 90],
)

deck = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=view_state,
    map_provider="carto",
    map_style="light",
    tooltip={
        "html": """
        <b>{event_type}</b><br/>
        <b>Sub-type:</b> {sub_event_type}<br/>
        <b>Location:</b> {location}, {admin1}<br/>
        <b>Date:</b> {event_date}<br/>
        <b>Fatalities:</b> {fatalities}<br/>
        <b>Actor 1:</b> {actor1}<br/>
        <b>Actor 2:</b> {actor2}
        """,
        "style": {
            "backgroundColor": "rgba(15, 23, 42, 0.92)",
            "color": "white",
            "borderRadius": "12px",
        },
    },
)

# -----------------------------
# Main layout
# -----------------------------
left, right = st.columns([1.7, 1.0], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Conflict Event Map")
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Event Type Breakdown")
    event_type_counts = (
        filtered_df["event_type"]
        .value_counts()
        .reset_index()
    )
    event_type_counts.columns = ["event_type", "count"]

    fig_bar = px.bar(
        event_type_counts,
        x="event_type",
        y="count",
        color="event_type",
        text="count",
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Events",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Lower charts
# -----------------------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Daily Event Trend")

    daily_df = (
        filtered_df.groupby(filtered_df["event_date"].dt.date)
        .size()
        .reset_index(name="events")
    )
    daily_df["event_date"] = pd.to_datetime(daily_df["event_date"])

    fig_line = px.line(
        daily_df,
        x="event_date",
        y="events",
        markers=True,
    )
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Events",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Fatalities by Region")

    region_df = (
        filtered_df.groupby("admin1", dropna=False)["fatalities"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    region_df["admin1"] = region_df["admin1"].fillna("Unknown")

    fig_region = px.bar(
        region_df,
        x="fatalities",
        y="admin1",
        color="admin1",
        orientation="h",
    )
    fig_region.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Fatalities",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_region, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Recent events table
# -----------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Recent Events")
show_cols = [
    "event_date",
    "event_type",
    "sub_event_type",
    "country",
    "admin1",
    "location",
    "actor1",
    "actor2",
    "fatalities",
    "source",
]
recent_df = filtered_df.sort_values("event_date", ascending=False)[show_cols].head(20).copy()
recent_df["event_date"] = recent_df["event_date"].dt.strftime("%Y-%m-%d")
st.dataframe(recent_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# GDELT Recent War News Pulse
# -----------------------------
st.markdown('<div class="hero-title" style="font-size:1.8rem; margin-top:2rem;">Recent War News Pulse</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Near-real-time media signal layer from GDELT.</div>',
    unsafe_allow_html=True,
)

if gdelt_df.empty:
    st.warning("No GDELT recent news data available.")
else:
    gdelt_total_articles = len(gdelt_df)
    gdelt_unique_countries = gdelt_df["sourcecountry"].nunique() if "sourcecountry" in gdelt_df.columns else 0
    gdelt_unique_domains = gdelt_df["domain"].nunique() if "domain" in gdelt_df.columns else 0
    latest_seen = gdelt_df["seendate"].max().strftime("%d %b %Y %H:%M") if "seendate" in gdelt_df.columns else "Unknown"

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        metric_card("Recent Articles", f"{gdelt_total_articles:,}", "Filtered GDELT article count")
    with g2:
        metric_card("Source Countries", f"{gdelt_unique_countries}", "Countries of publication/source")
    with g3:
        metric_card("News Domains", f"{gdelt_unique_domains}", "Unique publishing domains")
    with g4:
        metric_card("Latest Seen", latest_seen, "Most recent GDELT timestamp")

    gleft, gright = st.columns([1.2, 1.0], gap="large")

    with gleft:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Conflict Topic Breakdown")

        topic_counts = (
            gdelt_df["conflict_topic"]
            .value_counts()
            .reset_index()
        )
        topic_counts.columns = ["conflict_topic", "count"]

        fig_topics = px.bar(
            topic_counts,
            x="conflict_topic",
            y="count",
            color="conflict_topic",
            text="count",
        )
        fig_topics.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Articles",
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        fig_topics.update_traces(textposition="outside")
        st.plotly_chart(fig_topics, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with gright:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Top Source Countries")

        country_counts = (
            gdelt_df["sourcecountry"]
            .fillna("Unknown")
            .replace("", "Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )
        country_counts.columns = ["sourcecountry", "count"]

        fig_countries = px.pie(
            country_counts,
            names="sourcecountry",
            values="count",
        )
        fig_countries.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_countries, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    h1, h2 = st.columns(2, gap="large")

    with h1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Publishing Trend")

        trend_df = (
            gdelt_df.groupby(gdelt_df["seendate"].dt.floor("H"))
            .size()
            .reset_index(name="articles")
            .sort_values("seendate")
        )

        fig_trend = px.line(
            trend_df,
            x="seendate",
            y="articles",
            markers=True,
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Seen Time",
            yaxis_title="Articles",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with h2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Top Domains")

        domain_counts = (
            gdelt_df["domain"]
            .fillna("Unknown")
            .replace("", "Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )
        domain_counts.columns = ["domain", "count"]

        fig_domains = px.bar(
            domain_counts,
            x="count",
            y="domain",
            color="domain",
            orientation="h",
        )
        fig_domains.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Articles",
            yaxis_title="",
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_domains, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Latest Headlines")

    headline_cols = [col for col in [
        "seendate", "title", "conflict_topic", "sourcecountry", "domain", "language", "url"
    ] if col in gdelt_df.columns]

    headlines_df = gdelt_df[headline_cols].copy().sort_values("seendate", ascending=False).head(20)

    if "seendate" in headlines_df.columns:
        headlines_df["seendate"] = pd.to_datetime(headlines_df["seendate"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M")

    st.dataframe(headlines_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)