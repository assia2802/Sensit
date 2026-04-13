"""
Financial News Sentiment Analyzer — Loughran-McDonald Financial Lexicon

Reference: Loughran, T. and McDonald, B. (2011). "When Is a Liability Not a Liability?
Textual Analysis, Dictionaries, and 10-Ks." Journal of Finance, 66(1), 35-65.

Scoring method (v3 — density ratio):
    pos_density = pos_count / total_words
    neg_density = neg_count / total_words
    net_score   = (pos_density - neg_density) / (pos_density + neg_density + epsilon)

This spans [-1, +1] naturally:
  - Pure positive text  → close to +1
  - Pure negative text  → close to -1
  - Balanced or sparse  → close to 0
  - epsilon=0.001 dampens noise on very sparse text without collapsing to 0

POSITIVE list is intentionally strict. Generic financial words like "strong",
"growth", "increase", "leading", "best", "better", "support", "stable",
"recovery", "progress", "improve", "expand", "gain", "earn", "advance",
"momentum", "opportunity", "value", "profit", "innovation" have been removed
because they appear in all financial news regardless of actual sentiment.
"""

import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Word Lists
# ---------------------------------------------------------------------------

NEGATIVE = {
    "abandon", "abdicate", "abolish", "abuse", "accident", "adverse",
    "aggravate", "allegation", "allege", "annul", "anomaly",
    "antitrust", "attrition", "bail", "bankrupt", "bankruptcy",
    "beset", "breach", "broken", "burden", "catastrophe",
    "cease", "collapse", "collusion", "complain", "complaint",
    "concern", "condemn", "confiscate", "conspiracy", "contempt",
    "controversy", "convict", "correction", "costly", "crime",
    "criminal", "crisis", "criticize", "curtail", "damage",
    "danger", "dangerous", "deadlock", "death", "debt", "decline",
    "decreased", "default", "defeat", "defect", "deficiency",
    "deficit", "defraud", "degrade", "delay", "delinquent",
    "delist", "demise", "demolish", "demote", "denial", "deny",
    "deplete", "depress", "deprive", "destabilize", "destroy",
    "detrimental", "devalue", "difficult", "difficulty", "diminish",
    "disadvantage", "disappoint", "disappointing", "disappointment",
    "disapprove", "disaster", "discontinue", "discourage",
    "discredit", "discrepancy", "discrimination", "disgrace",
    "dishonest", "dismal", "disparage", "dispute", "disqualify",
    "disrupt", "disruption", "dissatisfy", "dissent", "dissolve",
    "distort", "distress", "disturb", "divest", "doubt",
    "downgrade", "downsize", "downturn", "drop", "dwindle",
    "dysfunction", "erode", "erosion", "error",
    "exacerbate", "excessive", "exhaust",
    "expose", "exposure", "fail", "failure", "fallout", "false",
    "fatal", "fatality", "fault", "fear", "felony", "fine",
    "flaw", "foreclose", "forfeit", "fraud", "fraudulent",
    "freeze", "frustrate", "grievance", "guilty", "halt",
    "hamper", "hardship", "harm", "harsh", "hazard", "hinder",
    "hostile", "hurt", "idle", "illegal", "illicit", "impair",
    "impairment", "impasse", "impeach", "impede", "impossible",
    "improper", "inability", "inaccurate", "inadequate",
    "inappropriate", "incapable", "incompetent", "incomplete",
    "inconsistent", "incorrect", "indebtedness", "indictment",
    "ineffective", "inefficiency", "ineligible", "inferior",
    "infringe", "infringement", "injure", "injury", "insolvency",
    "insolvent", "instability", "insufficient", "interfere",
    "interrupt", "intimidate", "invalid", "investigate",
    "investigation", "involuntary", "irrecoverable", "irregular",
    "jeopardize", "jeopardy", "lack", "lag", "lapse", "late",
    "layoff", "liquidate", "liquidation", "litigation",
    "lose", "loss", "lost", "malfeasance", "malfunction",
    "manipulate", "markdown", "meager", "mislead", "misleading",
    "mismanage", "misrepresent", "misstate", "misstatement",
    "miss", "missed", "mistake", "moratorium", "negate",
    "neglect", "negligence", "nonperformance", "nullify",
    "obsolete", "obstacle", "obstruct", "omission", "omit",
    "onerous", "oppose", "opposition", "outage", "overcapacity",
    "overdue", "overrun", "oversupply", "panic", "penalize",
    "penalty", "peril", "plaintiff", "plummet", "poor", "poorly",
    "postpone", "preclude", "pressure", "problematic", "prohibit",
    "prosecution", "protest", "punish", "punitive",
    "questionable", "reassess", "recall", "recession", "reckless",
    "refusal", "refuse", "reject", "relinquish", "reluctant",
    "repeal", "repossess", "repudiate", "resign", "restate",
    "restatement", "restructure", "restructuring", "retaliate",
    "retract", "revoke", "risk", "risky", "sabotage", "sanction",
    "scandal", "scarcity", "setback", "severe", "shortfall",
    "shrink", "shutdown", "skeptical", "slack", "slippage",
    "slowdown", "slump", "stagnant", "stagnate", "stall",
    "strain", "stress", "struggle", "substandard", "sue",
    "suffer", "susceptible", "suspend", "suspension", "taint",
    "terminate", "termination", "theft", "threat", "threaten",
    "trouble", "turbulence", "turmoil", "unable", "unacceptable",
    "unanticipated", "unavoidable", "uncertain", "uncertainty",
    "undermine", "underperform", "underperformance", "undesirable",
    "unfair", "unfavorable", "unfortunate", "unlawful", "unlikely",
    "unpaid", "unprofitable", "unrealistic", "unreasonable",
    "unrecoverable", "unresolved", "unsafe", "unsatisfactory",
    "unstable", "unsuccessful", "untimely", "unwanted",
    "unwarranted", "vacate", "violate", "violation", "volatile",
    "volatility", "vulnerability", "vulnerable", "warn", "warning",
    "weak", "weaken", "weakness", "worsen", "worsening",
    "worthless", "writedown", "writeoff",
}

# STRICT — only unambiguously positive in financial news context.
# Removed all generic descriptors that appear in neutral financial prose:
# strong, growth, increase, leading, best, better, greater, support,
# stable, recovery, progress, improve, improvement, expand, expansion,
# gain, earn, advance, momentum, opportunity, value, profitable, profit,
# innovation, innovative, innovate, invest, generate, record, top, surge.
POSITIVE = {
    "accomplish", "accomplishment", "achieve", "achievement",
    "advantage", "assure", "attain", "attractive",
    "beneficial", "benefit", "bolster", "boom", "boost",
    "breakthrough", "champion", "collaborate", "commend",
    "compelling", "competent", "confident", "constructive",
    "delight", "desirable", "diligent", "distinction",
    "distinguish", "ease", "efficiency", "efficient",
    "empower", "encourage", "encouraging", "endorse",
    "enhance", "enhancement", "enthusiasm", "enthusiastic",
    "exceed", "excel", "excellent", "exceptional", "excite",
    "excitement", "exemplary", "expert", "extraordinary",
    "favorable", "flagship", "flourish",
    "guarantee", "honor", "ideal", "impressive",
    "incredible", "influential", "ingenuity",
    "integrity", "invent", "invention", "inventive",
    "leadership", "lucrative", "mastery", "maximize",
    "merit", "milestone", "notable", "noteworthy",
    "nurture", "optimal", "optimism", "optimistic",
    "outpace", "outperform", "outperformance", "outstanding",
    "pioneer", "pleased", "pleasure", "popular",
    "praise", "premium", "proactive", "proficiency",
    "proficient", "profitability", "prominent",
    "promising", "propel", "prosper", "prosperity",
    "prosperous", "proud", "rebound", "refine",
    "remarkable", "resilient", "respect", "restore",
    "revitalize", "revolution", "revolutionize",
    "reward", "rewarding", "robust", "satisfaction",
    "satisfy", "solid", "solution", "stellar",
    "strengthen", "succeed", "success",
    "successful", "superior", "surpass", "sustainable",
    "synergy", "talent", "thrive", "transform",
    "transformation", "tremendous", "triumph", "trust",
    "unmatched", "unparalleled", "upgrade", "upside",
    "upturn", "versatile", "vibrant", "victory",
    "vigorous", "visionary", "win", "winner", "winning",
    "worthwhile",
}

UNCERTAINTY = {
    "almost", "anticipate", "apparent", "appear", "approximate",
    "approximately", "assume", "assumption", "believe", "cautious",
    "conceivable", "conditional", "contingent", "could", "depend",
    "depending", "estimate", "estimated", "eventual", "eventually",
    "expect", "expectation", "fluctuate", "fluctuation", "forecast",
    "foreseeable", "hope", "hopeful", "hopefully", "if", "imprecise",
    "indefinite", "indeterminate", "inexact", "intend", "intention",
    "likelihood", "likely", "may", "maybe", "might", "nearly",
    "occasionally", "ought", "outlook", "pending", "perceive",
    "perhaps", "possible", "possibly", "potential", "potentially",
    "predict", "prediction", "preliminary", "presumably", "presume",
    "probable", "probably", "projected", "projection", "prospect",
    "random", "reconsider", "roughly", "seem", "seldom", "should",
    "sometimes", "somewhat", "soon", "speculate", "speculation",
    "suggest", "suppose", "tend", "tentative", "unclear",
    "undecided", "undefined", "undetermined", "unknown", "unproven",
    "unspecified", "variable", "variability", "vary", "would",
}

LITIGIOUS = {
    "acquit", "adjudicate", "allegation", "allege", "amend", "appeal",
    "attorney", "claim", "claimant", "compliance", "complainant",
    "complaint", "contravene", "counsel", "counterclaim", "court",
    "damages", "decree", "defendant", "defense", "deposition",
    "directive", "discovery", "dismiss", "docket", "enforce",
    "enforcement", "enjoin", "evidence", "examiner", "federal",
    "filing", "finding", "guilty", "hearing", "illegal", "immunity",
    "indemnify", "indemnification", "indict", "indictment",
    "infringement", "injunction", "inspect", "inspection", "judge",
    "judgment", "judicial", "jurisdiction", "jury", "lawsuit",
    "lawyer", "legal", "legislate", "legislation", "liable",
    "liability", "litigate", "litigation", "magistrate", "mandate",
    "motion", "negligence", "oath", "objection", "obligation",
    "offense", "ordinance", "overrule", "penalty", "petition",
    "plaintiff", "plea", "plead", "precedent", "proceeding",
    "prosecute", "prosecution", "punitive", "recourse", "regulate",
    "regulation", "regulator", "regulatory", "remedy", "repeal",
    "ruling", "sanction", "sentence", "settle", "settlement",
    "statute", "statutory", "subpoena", "sue", "summon", "testify",
    "testimony", "tort", "trial", "tribunal", "uphold", "verdict",
    "violate", "violation", "warrant", "witness",
}

CONSTRAINING = {
    "abide", "bound", "cap", "ceiling", "commit", "commitment",
    "compel", "comply", "condition", "confine", "consent",
    "constrain", "constraint", "contingent", "contract", "covenant",
    "curb", "custody", "embargo", "encumber", "enforce", "forbid",
    "hinder", "impede", "impose", "inhibit", "injunction", "insist",
    "limit", "limitation", "mandate", "maximum", "minimum",
    "moratorium", "must", "necessitate", "obligate", "obligation",
    "obstruct", "preclude", "prevent", "prohibit", "prohibition",
    "quota", "require", "requirement", "restrain", "restraint",
    "restrict", "restriction", "shall", "stringent", "subordinate",
    "tighten",
}

STRONG_MODAL = {
    "always", "clearly", "definitely", "must", "never", "shall", "will",
}

WEAK_MODAL = {
    "almost", "apparently", "approximately", "conceivably", "could",
    "fairly", "generally", "hopefully", "likely", "mainly", "may",
    "maybe", "might", "mostly", "nearly", "occasionally", "ought",
    "perhaps", "possibly", "presumably", "probably", "roughly",
    "seldom", "seem", "should", "sometimes", "somewhat", "suggest",
    "tend", "tentative", "typically", "usually", "would",
}

EVASIVE_PHRASES = [
    "going forward", "as i mentioned", "as we mentioned",
    "at the end of the day", "to be honest", "quite frankly",
    "let me get back to you", "we'll get back to you",
    "it's too early to tell", "too early to say",
    "we're monitoring", "we are monitoring", "remains to be seen",
    "we're cautiously optimistic", "we are cautiously optimistic",
    "we're not going to speculate", "don't want to get ahead of",
    "do not want to get ahead of", "difficult to predict",
    "hard to predict", "difficult to quantify", "hard to quantify",
    "we're working through", "we are working through",
    "that's a great question", "that is a great question",
    "i appreciate the question", "we'll see how things play out",
    "we will see how things play out", "not in a position to comment",
    "we continue to evaluate", "taking a wait and see",
    "in the process of assessing", "subject to change",
    "no further comment", "we're comfortable with",
    "we are comfortable with", "normalized basis", "one-time charge",
    "non-recurring", "nonrecurring", "adjusted basis",
    "excluding items", "on a pro forma basis",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FlaggedSentence:
    text: str
    category: str
    score: float


@dataclass
class SentimentResult:
    net_score: float
    positive_count: int
    negative_count: int
    uncertainty_count: int
    litigious_count: int
    constraining_count: int
    strong_modal_count: int
    weak_modal_count: int
    evasive_count: int
    total_words: int
    category_ratios: dict
    flagged_sentences: list
    word_matches: dict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def _score_sentence(tokens: list[str]) -> tuple[str, float]:
    if not tokens:
        return "neutral", 0.0
    pos = sum(1 for t in tokens if t in POSITIVE)
    neg = sum(1 for t in tokens if t in NEGATIVE)
    unc = sum(1 for t in tokens if t in UNCERTAINTY)
    total = len(tokens)
    density = (pos + neg + unc) / total
    if neg > pos and neg > unc:
        return "negative", density
    elif pos > neg and pos > unc:
        return "positive", density
    elif unc > 0:
        return "uncertainty", density
    return "neutral", density


# ---------------------------------------------------------------------------
# Main scoring
# ---------------------------------------------------------------------------

def analyze_sentiment(text: str) -> SentimentResult:
    """
    Analyze text using the Loughran-McDonald financial lexicon.

    net_score = (pos_density - neg_density) / (pos_density + neg_density + epsilon)

    Density ratio: compares how often positive vs negative words appear
    relative to total words. epsilon=0.001 prevents division by zero
    and slightly dampens noise when both counts are very low.
    """
    tokens = _tokenize(text)
    total = len(tokens) or 1

    pos_matches = [t for t in tokens if t in POSITIVE]
    neg_matches = [t for t in tokens if t in NEGATIVE]
    unc_matches = [t for t in tokens if t in UNCERTAINTY]
    lit_matches = [t for t in tokens if t in LITIGIOUS]
    con_matches = [t for t in tokens if t in CONSTRAINING]
    sm_matches  = [t for t in tokens if t in STRONG_MODAL]
    wm_matches  = [t for t in tokens if t in WEAK_MODAL]

    pos_count = len(pos_matches)
    neg_count = len(neg_matches)
    unc_count = len(unc_matches)
    lit_count = len(lit_matches)
    con_count = len(con_matches)
    sm_count  = len(sm_matches)
    wm_count  = len(wm_matches)

    text_lower = text.lower()
    evasive_count = sum(1 for phrase in EVASIVE_PHRASES if phrase in text_lower)

    # Density ratio scoring — spans [-1, +1] naturally
    # Negative words are systematically underrepresented in RSS headlines/descriptions
    # (journalists write in neutral/informational tone even for crisis stocks).
    # A 1.5x weight on negative density compensates for this structural bias.
    NEG_WEIGHT = 1.5
    epsilon = 0.001
    pos_density = pos_count / total
    neg_density = neg_count / total
    weighted_neg = NEG_WEIGHT * neg_density
    net_score = (pos_density - weighted_neg) / (pos_density + weighted_neg + epsilon)
    net_score = round(max(-1.0, min(1.0, net_score)), 4)

    category_ratios = {
        "Positive":     round(pos_density * 1000, 2),
        "Negative":     round(neg_density * 1000, 2),
        "Uncertainty":  round(unc_count / total * 1000, 2),
        "Litigious":    round(lit_count / total * 1000, 2),
        "Constraining": round(con_count / total * 1000, 2),
        "Strong Modal": round(sm_count  / total * 1000, 2),
        "Weak Modal":   round(wm_count  / total * 1000, 2),
    }

    sentences = _split_sentences(text)
    flagged = []
    for sent in sentences:
        sent_tokens = _tokenize(sent)
        cat, density = _score_sentence(sent_tokens)
        if density > 0.05 and cat != "neutral":
            flagged.append(FlaggedSentence(text=sent, category=cat, score=density))

    for sent in sentences:
        sent_lower = sent.lower()
        for phrase in EVASIVE_PHRASES:
            if phrase in sent_lower:
                flagged.append(FlaggedSentence(text=sent, category="evasive", score=0.5))
                break

    flagged.sort(key=lambda x: x.score, reverse=True)
    flagged = flagged[:10]

    word_matches = {
        "Positive":     sorted(set(pos_matches)),
        "Negative":     sorted(set(neg_matches)),
        "Uncertainty":  sorted(set(unc_matches)),
        "Litigious":    sorted(set(lit_matches)),
        "Constraining": sorted(set(con_matches)),
    }

    return SentimentResult(
        net_score=net_score,
        positive_count=pos_count,
        negative_count=neg_count,
        uncertainty_count=unc_count,
        litigious_count=lit_count,
        constraining_count=con_count,
        strong_modal_count=sm_count,
        weak_modal_count=wm_count,
        evasive_count=evasive_count,
        total_words=total,
        category_ratios=category_ratios,
        flagged_sentences=flagged,
        word_matches=word_matches,
    )
