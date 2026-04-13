"""
Earnings Call Sentiment Analyzer — Loughran-McDonald Financial Lexicon

The Loughran-McDonald (LM) lexicon is specifically designed for financial text analysis.
Unlike general-purpose sentiment tools (VADER, TextBlob), the LM lexicon accounts for
the fact that words like "liability," "tax," or "capital" have neutral meaning in
financial contexts despite being negative in everyday language.

Reference: Loughran, T. and McDonald, B. (2011). "When Is a Liability Not a Liability?
Textual Analysis, Dictionaries, and 10-Ks." Journal of Finance, 66(1), 35-65.

Fixes applied (v2):
- net_score now normalizes against total words, not just matched words
- Removed ambiguous/context-dependent words from POSITIVE
  ("despite", "exploit", "record", "project", "save", "resolve", "invest",
   "dominant", "surge", "top", "promise", "reform", "overcome", "generate")
- Removed overlapping words from secondary lists to avoid double-counting:
  "doubt", "volatile", "volatility", "uncertainty", "unusual", "unforeseen",
  "susceptible", "unpredictable" removed from UNCERTAINTY (already in NEGATIVE)
  "shall" removed from UNCERTAINTY (already in CONSTRAINING/STRONG_MODAL)
  "reassess" removed from UNCERTAINTY (already in NEGATIVE)
"""

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Loughran-McDonald Word Lists (curated for earnings call analysis)
# ---------------------------------------------------------------------------

NEGATIVE = {
    "abandon", "abdicate", "abolish", "abuse", "accident", "acquit", "adverse",
    "against", "aggravate", "allegation", "allege", "annul", "anomaly",
    "antitrust", "argue", "attrition", "bad", "bail", "bankrupt", "bankruptcy",
    "beset", "breach", "break", "broken", "burden", "catastrophe", "caution",
    "cease", "challenge", "claim", "close", "closing", "collapse", "collusion",
    "complain", "complaint", "concern", "condemn", "confiscate", "conspiracy",
    "contempt", "contention", "contingency", "controversy", "convict",
    "correction", "costly", "crime", "criminal", "crisis", "critical",
    "criticize", "curtail", "cut", "damage", "danger", "dangerous", "deadlock",
    "death", "debarment", "debt", "decline", "decreased", "default", "defeat",
    "defect", "deficiency", "deficit", "defraud", "degrade", "delay", "delete",
    "delinquent", "delist", "demise", "demolish", "demote", "denial", "deny",
    "deplete", "depress", "deprive", "derogate", "destabilize", "destroy",
    "detain", "deter", "detrimental", "devalue", "deviate", "difficult",
    "difficulty", "diminish", "disadvantage", "disappoint", "disappointing",
    "disappointment", "disapprove", "disaster", "disclaim", "discontinue",
    "discourage", "discredit", "discrepancy", "discrimination", "disgrace",
    "dishonest", "dismal", "dismiss", "disparage", "displace", "dispute",
    "disqualify", "disregard", "disrupt", "disruption", "dissatisfy",
    "dissent", "dissolve", "distort", "distress", "disturb", "divert",
    "divest", "doubt", "downgrade", "downsize", "downturn", "drop", "drought",
    "dwindle", "dysfunction", "erode", "erosion", "error", "evict",
    "exacerbate", "exaggerate", "excessive", "exclude", "exhaust",
    "expose", "exposure", "fail", "failure", "fallout", "false", "fatal",
    "fatality", "fault", "fear", "felony", "fine", "flaw", "flee", "flood",
    "forbid", "force", "foreclose", "forfeit", "fraud", "fraudulent",
    "freeze", "frustrate", "grave", "grievance", "guilty", "halt", "hamper",
    "hardship", "harm", "harsh", "hazard", "hinder", "hindrance", "hostile",
    "hurt", "idle", "ignorance", "ignore", "illegal", "illicit", "impair",
    "impairment", "impasse", "impeach", "impede", "impediment", "impossible",
    "improper", "inability", "inaccurate", "inadequate", "inadvertent",
    "inappropriate", "incapable", "incompetent", "incomplete", "inconsistent",
    "incorrect", "indebtedness", "indictment", "ineffective", "inefficiency",
    "ineligible", "inevitable", "inferior", "infringe", "infringement",
    "inhibit", "injunction", "injure", "injury", "insolvency", "insolvent",
    "instability", "insufficient", "interfere", "interrupt", "intimidate",
    "invalid", "investigate", "investigation", "involuntary", "irrecoverable",
    "irregular", "jeopardize", "jeopardy", "lack", "lag", "lapse", "late",
    "layoff", "legacy", "liable", "liquidate", "liquidation", "litigation",
    "lose", "loss", "lost", "malfeasance", "malfunction", "manipulate",
    "markdown", "meager", "mislead", "misleading", "mismanage",
    "misrepresent", "misstate", "misstatement", "miss", "missed", "mistake",
    "monopoly", "moratorium", "negate", "negative", "neglect", "negligence",
    "nonperformance", "nuisance", "nullify", "objection", "obligate",
    "obscure", "obsolete", "obstacle", "obstruct", "offend", "omission",
    "omit", "onerous", "oppose", "opposition", "outage", "overbuild",
    "overburden", "overcapacity", "overdue", "overload", "overlook",
    "overrun", "oversaturate", "oversupply", "overturn", "panic", "penal",
    "penalize", "penalty", "peril", "persist", "petition", "plaintiff",
    "plead", "plummet", "poor", "poorly", "postpone", "precipitate",
    "preclude", "pressure", "problematic", "prohibit", "prosecution",
    "protest", "punish", "punitive", "purport", "questionable",
    "reassess", "recall", "recession", "reckless", "recoup", "redress",
    "refusal", "refuse", "reject", "relinquish", "reluctant", "remediate",
    "repeal", "repossess", "repudiate", "resign", "restate", "restatement",
    "restructure", "restructuring", "retaliate", "retract", "retribution",
    "revoke", "risk", "risky", "sabotage", "sacrifice", "sanction",
    "scandal", "scarcity", "sequester", "setback", "severe", "sharply",
    "shortfall", "shrink", "shrinkage", "shutdown", "skeptic", "skeptical",
    "slack", "slippage", "slow", "slowdown", "slump", "stagnant",
    "stagnate", "stall", "strain", "stress", "stringent", "struggle",
    "subpoena", "substandard", "sue", "suffer", "summon", "surplus",
    "susceptible", "suspect", "suspend", "suspension", "taint", "terminate",
    "termination", "theft", "threat", "threaten", "tighten", "toll",
    "trouble", "turbulence", "turmoil", "unable", "unacceptable",
    "unanticipated", "unavoidable", "uncertain", "uncertainty",
    "unconstitutional", "undercount", "underestimate", "undermine",
    "underperform", "underperformance", "understaffed", "undesirable",
    "undisclosed", "unfair", "unfavorable", "unforeseen", "unfortunate",
    "unlawful", "unlikely", "unpaid", "unpredictable", "unprofitable",
    "unqualified", "unrealistic", "unreasonable", "unrecoverable",
    "unresolved", "unsafe", "unsatisfactory", "unstable", "unsuccessful",
    "unsupported", "untimely", "unusual", "unwanted", "unwarranted",
    "usurp", "vacancy", "vacate", "violate", "violation", "volatile",
    "volatility", "vulnerability", "vulnerable", "warn", "warning", "weak",
    "weaken", "weakness", "worsen", "worsening", "worthless", "writedown",
    "writeoff",
}

# FIX: Removed ambiguous words that fire too easily on neutral headlines:
# "despite", "exploit", "record", "project", "save", "resolve", "invest",
# "dominant", "surge", "top", "promise", "reform", "overcome", "generate"
POSITIVE = {
    "abundance", "abundant", "accomplish", "accomplishment",
    "achieve", "achievement", "adequate", "advance", "advantage",
    "alliance", "assure", "attain", "attract", "attractive",
    "beneficial", "benefit", "benefiting", "best", "better", "bolster",
    "boom", "boost", "breakthrough", "bright", "champion", "collaborate",
    "commend", "commitment", "compelling", "competent", "complement",
    "compliment", "confident", "constructive", "creative", "creativity",
    "delight", "deliver", "desirable", "diligent", "distinction",
    "distinguish", "earn", "ease", "easier", "easy", "efficiency",
    "efficient", "empower", "enable", "encourage", "encouraging", "endorse",
    "enhance", "enhancement", "enjoy", "enormous", "enthusiasm",
    "enthusiastic", "exceed", "excel", "excellent", "exceptional", "excite",
    "excitement", "exclusive", "exemplary", "expand", "expansion", "expert",
    "extraordinary", "favorable", "flagship", "flourish", "gain",
    "good", "great", "greater", "greatest", "grow", "growing",
    "growth", "guarantee", "happy", "honor", "ideal",
    "imagination", "impressive", "improve", "improvement", "increase",
    "incredible", "influential", "ingenuity", "innovate", "innovation",
    "innovative", "insight", "instrumental", "integrity", "invent",
    "invention", "inventive", "leadership", "leading", "lucrative",
    "mastery", "maximize", "merit", "milestone", "momentum", "notable",
    "noteworthy", "nurture", "opportunity", "optimal", "optimism",
    "optimistic", "outpace", "outperform", "outperformance", "outstanding",
    "perfect", "pioneer", "pleased", "pleasure", "popular",
    "positive", "praise", "premium", "proactive", "proficiency",
    "proficient", "profit", "profitable", "profitability", "progress",
    "prominent", "promising", "propel", "prosper", "prosperity",
    "prosperous", "proud", "rebound", "recovery", "refine",
    "remarkable", "resilient", "respect", "restore",
    "revitalize", "revolution", "revolutionize", "reward", "rewarding",
    "robust", "satisfaction", "satisfy", "smooth", "solid",
    "solution", "solve", "stability", "stable", "stellar", "strength",
    "strengthen", "strong", "stronger", "strongest", "succeed", "success",
    "successful", "superior", "support", "surpass", "sustainable",
    "synergy", "talent", "thrive", "transform", "transformation",
    "tremendous", "triumph", "trust", "unmatched", "unparalleled", "upgrade",
    "upside", "upturn", "valuable", "value", "versatile", "vibrant",
    "victory", "vigorous", "visionary", "win", "winner", "winning",
    "worthwhile",
}

# FIX: Removed words already present in NEGATIVE to avoid double-counting:
# "doubt", "volatile", "volatility", "uncertainty", "unusual", "unforeseen",
# "susceptible", "unpredictable", "reassess"
# Also removed "shall" (already in CONSTRAINING and STRONG_MODAL)
UNCERTAINTY = {
    "almost", "anticipate", "apparent", "appear", "approximate",
    "approximately", "assume", "assumption", "believe", "cautious",
    "conceivable", "conditional", "contingent", "could", "depend",
    "depending", "estimate", "estimated", "eventual", "eventually",
    "expect", "expectation", "fluctuate", "fluctuation", "forecast",
    "foreseeable", "hope", "hopeful", "hopefully", "if", "imprecise",
    "imprecision", "indefinite", "indeterminate", "inexact", "intend",
    "intention", "likelihood", "likely", "may", "maybe", "might", "nearly",
    "occasionally", "ought", "outlook", "pending", "perceive", "perhaps",
    "possible", "possibly", "potential", "potentially", "predict",
    "prediction", "predictive", "preliminary", "presumably", "presume",
    "probable", "probably", "projected", "projection", "prospect",
    "random", "reconsider", "roughly", "seem", "seldom",
    "should", "sometimes", "somewhat", "soon", "speculate",
    "speculation", "suggest", "suppose", "tend", "tentative",
    "unclear", "undecided", "undefined",
    "undetermined", "unforeseeable",
    "unknown", "unproven", "unquantifiable", "unspecified",
    "variable", "variability", "vary", "would",
}

LITIGIOUS = {
    "acquit", "adjudicate", "allegation", "allege", "amend", "appeal",
    "attorney", "claim", "claimant", "class", "code", "commission",
    "commissioner", "committee", "complainant", "complaint", "comply",
    "compliance", "compulsory", "concurrence", "consent", "contravene",
    "counsel", "counterclaim", "court", "damages", "decree", "defendant",
    "defense", "deposition", "directive", "discovery", "dismiss", "docket",
    "enforce", "enforcement", "enjoin", "enact", "evidence", "examination",
    "examiner", "federal", "file", "filing", "finding", "guilty", "hearing",
    "illegal", "immunity", "indemnify", "indemnification", "indict",
    "indictment", "infringe", "infringement", "injunction", "inspect",
    "inspection", "judge", "judgment", "judicial", "jurisdiction", "jury",
    "law", "lawsuit", "lawyer", "legal", "legislate", "legislation",
    "legislature", "liable", "liability", "litigate", "litigation",
    "magistrate", "mandate", "motion", "negligence", "oath", "object",
    "objection", "obligation", "offense", "order", "ordinance", "overrule",
    "penalty", "petition", "plaintiff", "plea", "plead", "precedent",
    "proceeding", "prohibit", "prohibition", "prosecute", "prosecution",
    "prove", "provision", "punitive", "recourse", "regulate", "regulation",
    "regulator", "regulatory", "remedy", "repeal", "resolve", "resolution",
    "rule", "ruling", "sanction", "sentence", "settle", "settlement",
    "statute", "statutory", "subpoena", "sue", "summon", "testify",
    "testimony", "tort", "trial", "tribunal", "uphold", "verdict",
    "violate", "violation", "warrant", "witness",
}

CONSTRAINING = {
    "abide", "bound", "cap", "ceiling", "commit", "commitment", "compel",
    "comply", "condition", "confine", "consent", "constrain", "constraint",
    "contingent", "contract", "covenant", "curb", "custody", "embargo",
    "encumber", "enforce", "forbid", "hinder", "impede", "impose",
    "inhibit", "injunction", "insist", "limit", "limitation", "mandate",
    "maximum", "minimum", "moratorium", "must", "necessitate", "obligate",
    "obligation", "obstruct", "preclude", "prevent", "prohibit",
    "prohibition", "quota", "require", "requirement", "restrain",
    "restraint", "restrict", "restriction", "shall", "stringent",
    "subordinate", "tighten", "toll",
}

STRONG_MODAL = {
    "always", "best", "clearly", "definitely", "highest", "must",
    "never", "shall", "strongest", "will",
}

WEAK_MODAL = {
    "almost", "apparently", "approximately", "conceivably", "could",
    "doubt", "fairly", "generally", "hopefully", "likely", "mainly",
    "may", "maybe", "might", "mostly", "nearly", "occasionally",
    "ought", "perhaps", "possibly", "presumably", "probably",
    "roughly", "seldom", "seem", "should", "sometimes", "somewhat",
    "suggest", "tend", "tentative", "typically", "usually", "would",
}

# Evasive / hedging phrases commonly used by management to deflect
EVASIVE_PHRASES = [
    "going forward",
    "as i mentioned",
    "as we mentioned",
    "at the end of the day",
    "to be honest",
    "quite frankly",
    "let me get back to you",
    "we'll get back to you",
    "it's too early to tell",
    "too early to say",
    "we're monitoring",
    "we are monitoring",
    "remains to be seen",
    "we're cautiously optimistic",
    "we are cautiously optimistic",
    "we're not going to speculate",
    "don't want to get ahead of",
    "do not want to get ahead of",
    "difficult to predict",
    "hard to predict",
    "difficult to quantify",
    "hard to quantify",
    "we're working through",
    "we are working through",
    "that's a great question",
    "that is a great question",
    "i appreciate the question",
    "we'll see how things play out",
    "we will see how things play out",
    "not in a position to comment",
    "we continue to evaluate",
    "taking a wait and see",
    "in the process of assessing",
    "subject to change",
    "no further comment",
    "we're comfortable with",
    "we are comfortable with",
    "normalized basis",
    "one-time charge",
    "non-recurring",
    "nonrecurring",
    "adjusted basis",
    "excluding items",
    "on a pro forma basis",
]


# ---------------------------------------------------------------------------
# Sentiment Scoring
# ---------------------------------------------------------------------------

@dataclass
class FlaggedSentence:
    text: str
    category: str  # "positive", "negative", "uncertainty", "evasive"
    score: float   # density of sentiment words in the sentence


@dataclass
class SentimentResult:
    net_score: float                    # -1 to 1
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
    word_matches: dict                  # category -> list of matched words


def _tokenize(text: str) -> list[str]:
    """Lowercase tokenization, stripping punctuation."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def _score_sentence(tokens: list[str]) -> tuple[str, float]:
    """Return dominant category and sentiment density for a sentence."""
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


def analyze_sentiment(text: str) -> SentimentResult:
    """
    Analyze text using the Loughran-McDonald financial lexicon.
    Returns a SentimentResult with scores, counts, ratios, and flagged sentences.
    """
    tokens = _tokenize(text)
    total = len(tokens) or 1

    # Count words in each category
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

    # Count evasive phrases
    text_lower = text.lower()
    evasive_count = sum(1 for phrase in EVASIVE_PHRASES if phrase in text_lower)

    # FIX: Net sentiment score normalised against ALL words, not just matched ones.
    # Old formula: (pos - neg) / (pos + neg)  → inflates score on sparse text
    # New formula: (pos - neg) / total         → honest signal, naturally closer to 0
    net_score = (pos_count - neg_count) / total

    # Category ratios (per 1000 words for readability)
    category_ratios = {
        "Positive":    round(pos_count / total * 1000, 2),
        "Negative":    round(neg_count / total * 1000, 2),
        "Uncertainty": round(unc_count / total * 1000, 2),
        "Litigious":   round(lit_count / total * 1000, 2),
        "Constraining":round(con_count / total * 1000, 2),
        "Strong Modal":round(sm_count  / total * 1000, 2),
        "Weak Modal":  round(wm_count  / total * 1000, 2),
    }

    # Flagged sentences — top 10 most sentiment-dense
    sentences = _split_sentences(text)
    flagged = []
    for sent in sentences:
        sent_tokens = _tokenize(sent)
        cat, density = _score_sentence(sent_tokens)
        if density > 0.05 and cat != "neutral":
            flagged.append(FlaggedSentence(text=sent, category=cat, score=density))

    # Check sentences for evasive phrases
    for sent in sentences:
        sent_lower = sent.lower()
        for phrase in EVASIVE_PHRASES:
            if phrase in sent_lower:
                flagged.append(FlaggedSentence(text=sent, category="evasive", score=0.5))
                break

    # Sort by score descending, take top 10
    flagged.sort(key=lambda x: x.score, reverse=True)
    flagged = flagged[:10]

    # Unique matched words per category
    word_matches = {
        "Positive":    sorted(set(pos_matches)),
        "Negative":    sorted(set(neg_matches)),
        "Uncertainty": sorted(set(unc_matches)),
        "Litigious":   sorted(set(lit_matches)),
        "Constraining":sorted(set(con_matches)),
    }

    return SentimentResult(
        net_score=round(net_score, 4),
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
