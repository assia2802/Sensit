"""
Financial News Sentiment Analyzer
Powered by the Loughran-McDonald Financial Lexicon
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.lexicon import analyze_sentiment
from src.divergence import compute_divergence
from src.data_fetcher import fetch_news, fetch_stock_prices, fetch_company_name

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Financial News Sentiment Analyzer",
    page_icon="$",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Hide delta arrows on all metrics — color alone conveys direction */
    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        opacity: 0.7;
        margin-top: 0;
    }
    .flag-sentence {
        border-left: 3px solid rgba(255,255,255,0.3);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.05);
        border-radius: 0 6px 6px 0;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    .divergence-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 1.5rem;
    }
    .divergence-box h3 {
        margin-top: 0;
    }
    .divergence-box p {
        margin: 0.4rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Configuration")

    ticker = st.text_input("Ticker Symbol", value="AAPL").strip().upper()

    period = st.selectbox(
        "Time Period",
        ["5d", "1mo", "3mo"],
        index=1,
        format_func=lambda x: {"5d": "5 Days", "1mo": "1 Month", "3mo": "3 Months"}[x],
    )

    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

    st.divider()
    st.caption("No API key needed. All data is fetched from free public sources (Google News, Yahoo Finance).")

    st.divider()
    with st.expander("About the methodology"):
        st.markdown("""
        **Loughran-McDonald Financial Lexicon**

        Unlike general NLP tools (VADER, TextBlob), the LM lexicon is designed
        specifically for financial text. Words like *"liability"*, *"tax"*, or
        *"capital"* are neutral in finance despite being negative in everyday language.

        **Categories analyzed:**
        - **Positive / Negative** -- directional sentiment
        - **Uncertainty** -- hedging and vague language
        - **Litigious** -- legal and regulatory language
        - **Constraining** -- obligations and restrictions

        **Divergence Detection:**
        Compares the news sentiment tone against actual stock price
        movement to flag cases where the narrative doesn't match
        the market reality.

        *Reference: Loughran & McDonald (2011), Journal of Finance*
        """)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<p class="main-header">Financial News Sentiment Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Detect divergence between news sentiment and stock price movement using the Loughran-McDonald lexicon</p>', unsafe_allow_html=True)
st.markdown("")

# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------
if analyze_btn:
    if not ticker:
        st.error("Please enter a ticker symbol.")
        st.stop()

    # Fetch all data
    with st.spinner(f"Fetching data for {ticker}..."):
        company_name = fetch_company_name(ticker)
        news = fetch_news(ticker, company_name, period)
        prices = fetch_stock_prices(ticker, period)

    if not news:
        st.error(f"Could not fetch news for {ticker}. Check the ticker symbol.")
        st.stop()

    if not prices:
        st.error(f"Could not fetch stock prices for {ticker}. Check the ticker symbol.")
        st.stop()

    # Run sentiment on all headlines combined
    # Use full text (title + description) for richer sentiment signal
    all_text = " . ".join(a["text"] for a in news)
    result = analyze_sentiment(all_text)

    # Also score each headline individually for the table
    headline_scores = []
    for a in news:
        h_result = analyze_sentiment(a["text"])
        headline_scores.append({
            "Headline": a["title"],
            "Source": a["source"],
            "Sentiment": h_result.net_score,
        })

    # --- Row 1: Key Metrics ---
    st.markdown(f"### {company_name} ({ticker})")
    st.markdown("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if result.net_score > 0.2:
            tone = "Positive Tone"
        elif result.net_score < -0.2:
            tone = "Negative Tone"
        elif result.net_score > 0.05:
            tone = "Slightly Positive"
        elif result.net_score < -0.05:
            tone = "Slightly Negative"
        else:
            tone = "Mixed Tone"
        st.metric(
            "News Sentiment",
            f"{result.net_score:+.3f}",
            delta=tone,
            delta_color="normal" if result.net_score >= 0 else "inverse",
        )

    with col2:
        st.metric(
            "Stock Price",
            f"${prices['current']:.2f}",
            delta=f"{prices['change_pct']:+.1f}%",
            delta_color="normal",
        )

    with col3:
        st.metric("Headlines Analyzed", len(news))

    with col4:
        pos = len([h for h in headline_scores if h["Sentiment"] > 0.1])
        neg = len([h for h in headline_scores if h["Sentiment"] < -0.1])
        st.metric("Positive / Negative Articles", f"{pos} / {neg}")

    st.caption(
        "⚠️ Scores reflect the language tone of news headlines and summaries, not investment recommendations. "
        "Free RSS sources systematically underrepresent negative language — scores are calibrated accordingly."
    )
    st.markdown("")

    # --- Row 2: Sentiment Gauge + Category Breakdown ---
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### Sentiment Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result.net_score,
            number={"suffix": "", "font": {"size": 36}},
            gauge={
                "axis": {"range": [-1, 1], "tickvals": [-1, -0.5, 0, 0.5, 1]},
                "bar": {"color": "#1a1a2e"},
                "steps": [
                    {"range": [-1, -0.5], "color": "#dc3545"},
                    {"range": [-0.5, -0.15], "color": "#fd7e14"},
                    {"range": [-0.15, 0.15], "color": "#ffc107"},
                    {"range": [0.15, 0.5], "color": "#a3d977"},
                    {"range": [0.5, 1], "color": "#28a745"},
                ],
                "threshold": {
                    "line": {"color": "#1a1a2e", "width": 3},
                    "thickness": 0.8,
                    "value": result.net_score,
                },
            },
        ))
        fig_gauge.update_layout(
            height=280,
            margin=dict(l=30, r=30, t=30, b=10),
            font=dict(family="system-ui"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.markdown("#### Category Breakdown (per 1,000 words)")
        categories = list(result.category_ratios.keys())
        values = list(result.category_ratios.values())
        colors = ["#28a745", "#dc3545", "#fd7e14", "#6f42c1", "#795548", "#1a73e8", "#adb5bd"]

        fig_bar = go.Figure(go.Bar(
            x=values,
            y=categories,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}" for v in values],
            textposition="outside",
        ))
        fig_bar.update_layout(
            height=280,
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis_title="Frequency per 1,000 words",
            yaxis=dict(autorange="reversed"),
            font=dict(family="system-ui"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Row 3: Stock Price Chart ---
    st.markdown("---")
    st.markdown("#### Stock Price")
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=prices["dates"],
        y=prices["closes"],
        mode="lines+markers",
        line=dict(color="#4a90d9", width=2),
        marker=dict(size=4),
        fill="tozeroy",
        fillcolor="rgba(74,144,217,0.1)",
    ))
    fig_price.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis_title="Date",
        yaxis_title="Price ($)",
        font=dict(family="system-ui"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # --- Row 4: Divergence Analysis ---
    st.markdown("---")
    st.markdown("#### Divergence Analysis: News Tone vs. Price Movement")

    div_result = compute_divergence(result.net_score, prices["change_pct"])

    severity_label = {"low": "Low Divergence", "moderate": "Moderate Divergence", "high": "High Divergence"}

    col_d1, col_d2 = st.columns([1, 2])

    with col_d1:
        fig_div = go.Figure()
        fig_div.add_trace(go.Bar(
            x=["News Tone", "Price Movement"],
            y=[result.net_score, prices["change_pct"] / 10],
            marker_color=["#4a90d9", "#28a745" if prices["change_pct"] >= 0 else "#dc3545"],
            text=[f"{result.net_score:+.3f}", f"{prices['change_pct']:+.1f}%"],
            textposition="outside",
        ))
        fig_div.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(range=[-1.2, 1.2], title="Normalized Score"),
            showlegend=False,
            font=dict(family="system-ui"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_div, use_container_width=True)

    with col_d2:
        st.markdown(f"""
<div class="divergence-box">
    <h3>{severity_label[div_result.severity]}</h3>
    <p><strong>Divergence Score:</strong> {div_result.score:+.3f} &nbsp;|&nbsp; <strong>Severity:</strong> {div_result.severity.capitalize()}</p>
    <p><strong>News Tone:</strong> {div_result.tone_label} ({result.net_score:+.3f})</p>
    <p><strong>Price Movement:</strong> {div_result.price_label}</p>
    <p style="margin-top: 0.8rem;">{div_result.interpretation}</p>
</div>
""", unsafe_allow_html=True)

    # --- Row 5: Headline Sentiment Table ---
    st.markdown("---")
    st.markdown("#### Headline Sentiment Breakdown")
    st.caption("Individual sentiment scores for each news headline.")

    df = pd.DataFrame(headline_scores)
    if not df.empty:
        df = df.sort_values("Sentiment", ascending=False).reset_index(drop=True)
        df["Sentiment"] = df["Sentiment"].apply(lambda x: f"{x:+.3f}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Row 6: Key Words Detected ---
    st.markdown("---")
    st.markdown("#### Key Words Detected by Category")

    tab_pos, tab_neg, tab_unc, tab_lit = st.tabs(["Positive", "Negative", "Uncertainty", "Litigious"])

    with tab_pos:
        words = result.word_matches.get("Positive", [])
        if words:
            st.markdown(" ".join(f"`{w}`" for w in words))
        else:
            st.info("No positive LM words detected.")

    with tab_neg:
        words = result.word_matches.get("Negative", [])
        if words:
            st.markdown(" ".join(f"`{w}`" for w in words))
        else:
            st.info("No negative LM words detected.")

    with tab_unc:
        words = result.word_matches.get("Uncertainty", [])
        if words:
            st.markdown(" ".join(f"`{w}`" for w in words))
        else:
            st.info("No uncertainty LM words detected.")

    with tab_lit:
        words = result.word_matches.get("Litigious", [])
        if words:
            st.markdown(" ".join(f"`{w}`" for w in words))
        else:
            st.info("No litigious LM words detected.")

else:
    # Landing state
    st.markdown("")
    st.info("Enter a ticker symbol in the sidebar and click **Analyze** to run the sentiment analysis.")

    st.markdown("#### What this tool does")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **1. Analyze News Tone**

        Collects recent financial news headlines
        from Google News and Yahoo Finance, then
        scores them using the Loughran-McDonald
        financial sentiment lexicon across 6
        categories.
        """)
    with col2:
        st.markdown("""
        **2. Track Price Movement**

        Retrieves real-time stock price data from
        Yahoo Finance to measure how the stock has
        actually performed over the selected
        time period.
        """)
    with col3:
        st.markdown("""
        **3. Detect Divergence**

        Compares the news sentiment against actual
        price movement to flag cases where the
        narrative doesn't match market reality --
        a signal used by quantitative hedge funds.
        """)
