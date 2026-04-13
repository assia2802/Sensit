"""
Divergence Detection — compares news sentiment tone vs. actual stock price movement.

The core idea: if financial news is overwhelmingly positive but the stock is dropping
(or vice versa), there's a divergence between narrative and reality. Quantitative hedge
funds use this signal to detect when media sentiment hasn't caught up to price action,
or when price hasn't caught up to sentiment — both can be alpha signals.
"""

from dataclasses import dataclass
import math


@dataclass
class DivergenceResult:
    score: float            # -2 to +2 (negative = price leads sentiment, positive = sentiment leads price)
    severity: str           # "low", "moderate", "high"
    direction: str          # "aligned", "sentiment_leads", "price_leads"
    tone_label: str         # human-readable tone
    price_label: str        # human-readable price movement
    interpretation: str     # plain-english explanation


def compute_divergence(
    sentiment_score: float,
    price_change_pct: float,
) -> DivergenceResult:
    """
    Compare news sentiment with stock price movement to detect divergence.

    sentiment_score: net sentiment from LM analysis, range [-1, 1]
    price_change_pct: stock price change over the period in percent

    Returns DivergenceResult with score, severity, and interpretation.
    """
    # Normalize price change to [-1, 1] range using tanh
    price_normalized = math.tanh(price_change_pct / 10)

    # Divergence: difference between sentiment and price direction
    # Positive = sentiment more positive than price movement (hype / sentiment leads)
    # Negative = price more positive than sentiment (under-reported rally / price leads)
    divergence = sentiment_score - price_normalized

    # Severity
    abs_div = abs(divergence)
    if abs_div < 0.3:
        severity = "low"
    elif abs_div < 0.7:
        severity = "moderate"
    else:
        severity = "high"

    # Direction
    if abs_div < 0.3:
        direction = "aligned"
    elif divergence > 0:
        direction = "sentiment_leads"
    else:
        direction = "price_leads"

    # Tone label
    if sentiment_score > 0.15:
        tone_label = "Positive"
    elif sentiment_score < -0.15:
        tone_label = "Negative"
    else:
        tone_label = "Neutral"

    # Price label
    if price_change_pct > 1:
        price_label = f"Up {price_change_pct:+.1f}%"
    elif price_change_pct < -1:
        price_label = f"Down {price_change_pct:+.1f}%"
    else:
        price_label = f"Flat ({price_change_pct:+.1f}%)"

    # Interpretations
    interpretations = {
        ("aligned", "Positive"): (
            "News sentiment and stock price are moving in the same positive direction. "
            "The market narrative aligns with price action — no divergence signal."
        ),
        ("aligned", "Negative"): (
            "News sentiment and stock price are both negative. "
            "The bearish narrative matches the price decline — no divergence signal."
        ),
        ("aligned", "Neutral"): (
            "News sentiment is neutral and the stock is relatively flat. "
            "No meaningful divergence detected."
        ),
        ("sentiment_leads", "Positive"): (
            "News sentiment is significantly more positive than price movement suggests. "
            "This could mean the market hasn't fully priced in the positive narrative yet "
            "(potential upside), or that media hype is ahead of fundamentals (risk of correction)."
        ),
        ("sentiment_leads", "Negative"): (
            "News sentiment is less negative than the actual price drop. Media coverage "
            "may be lagging behind the sell-off, or the drop is driven by technical/macro "
            "factors not yet reflected in company-specific news."
        ),
        ("sentiment_leads", "Neutral"): (
            "News sentiment is more positive than the flat price action. "
            "The positive narrative hasn't translated into buying pressure yet — "
            "either the market disagrees, or sentiment could be a leading indicator."
        ),
        ("price_leads", "Positive"): (
            "The stock is rallying but news sentiment hasn't caught up. "
            "This under-reported momentum can be a signal that the move has further "
            "to run, or that informed buyers are acting ahead of public news."
        ),
        ("price_leads", "Negative"): (
            "News sentiment is more negative than the price decline warrants. "
            "Media may be amplifying fear beyond what the market is pricing in. "
            "This pattern sometimes precedes a sentiment-driven overshoot (buying opportunity) "
            "or can signal that the worst is yet to come."
        ),
        ("price_leads", "Neutral"): (
            "The stock is moving but news coverage is neutral. "
            "Price action is being driven by factors not captured in the current news cycle."
        ),
    }

    interpretation = interpretations.get(
        (direction, tone_label),
        "Divergence analysis could not determine a clear pattern."
    )

    return DivergenceResult(
        score=round(divergence, 3),
        severity=severity,
        direction=direction,
        tone_label=tone_label,
        price_label=price_label,
        interpretation=interpretation,
    )
