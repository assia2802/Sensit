"""
Sample earnings call transcripts and EPS data for demo mode.
These are simulated transcripts for educational purposes — they illustrate
different sentiment/EPS divergence patterns.
"""

SAMPLE_TRANSCRIPTS = {
    "AAPL": {
        "ticker": "AAPL",
        "date": "2024-10-31",
        "year": 2024,
        "quarter": 4,
        "content": """
Operator: Good afternoon, and welcome to Apple's Fourth Quarter Fiscal Year 2024 Earnings Conference Call. I would now like to turn the call over to the CEO.

CEO Prepared Remarks:

Thank you, and good afternoon everyone. We are thrilled to report an outstanding quarter that exceeded our expectations across every major product category. Revenue reached a new all-time record, driven by strong demand for iPhone, incredible growth in Services, and better-than-expected performance from our Mac lineup.

Our installed base of active devices has reached an all-time high, and customer satisfaction and loyalty remain the best in the industry. We're seeing tremendous enthusiasm for our latest products, and our innovation pipeline has never been stronger.

iPhone revenue grew significantly year over year, driven by strong demand for the iPhone 16 lineup. We're particularly pleased with the adoption of Apple Intelligence features, which are resonating deeply with our customers and driving meaningful upgrades. The customer response has been exceptional across all geographies.

Services revenue set another all-time record, with over a billion paid subscriptions across our platform. This segment continues to demonstrate robust growth, and we're confident in the long-term trajectory as we expand our offerings and deepen customer engagement.

Mac revenue also delivered strong results, with the transition to Apple Silicon continuing to attract new customers to the Mac. We're seeing impressive gains in both consumer and enterprise adoption.

Looking ahead, we remain incredibly optimistic about the opportunity in front of us. Our investments in artificial intelligence, augmented reality, and custom silicon position us to lead the next generation of personal technology.

CFO Prepared Remarks:

Thank you. Let me provide more detail on our financial performance. Total revenue for the quarter was $94.9 billion, up 6 percent year over year and above the high end of our guidance range. Gross margin was 46.2 percent, a new record for the September quarter, reflecting both favorable mix and operational efficiencies.

Operating expenses were well-managed at $14.3 billion, reflecting our continued discipline in spending while investing in key growth areas. We generated operating cash flow of $26.8 billion and returned over $29 billion to shareholders through dividends and share repurchases.

Earnings per share were $1.64, up 12 percent year over year, representing our best fourth quarter earnings performance ever. We are very pleased with these results and the momentum we carry into the holiday quarter.

For the December quarter, we expect revenue to grow in the mid-to-high single digits year over year. We're confident in the strength of our product lineup and excited about the holiday season ahead.

Q&A Session:

Analyst: Can you talk about the competitive landscape for AI features and whether that's driving upgrade cycles?

CEO: Great question. We're seeing clear evidence that Apple Intelligence is becoming a meaningful driver of upgrades. Our approach of on-device processing combined with Private Cloud Compute gives us a unique advantage that competitors cannot easily replicate. We believe we're just at the beginning of what AI can do on our platform, and customer feedback has been overwhelmingly positive.

Analyst: Margins have been impressive. How sustainable is this trajectory?

CFO: We feel very good about our margin profile going forward. The shift toward Services, which carries higher margins, combined with the efficiencies from Apple Silicon, creates a favorable structural tailwind. We'll continue to invest in innovation, but we expect to maintain strong profitability.

Analyst: Any concerns about China demand?

CEO: We're monitoring the China market carefully. We did see some softness earlier in the year, but the response to iPhone 16 has been encouraging. Going forward, we're cautiously optimistic, but we continue to evaluate the competitive dynamics in that market. It remains to be seen how some of the macro factors will play out.
""",
    },
    "TSLA": {
        "ticker": "TSLA",
        "date": "2024-10-23",
        "year": 2024,
        "quarter": 3,
        "content": """
Operator: Good afternoon, and welcome to Tesla's Third Quarter 2024 Earnings Conference Call. I would now like to turn the call over to the CEO.

CEO Prepared Remarks:

Thanks everyone. This was an incredible quarter, truly one of the best in Tesla's history. I am extremely excited about what lies ahead. We are on the verge of a revolution in autonomous transportation, and Tesla is leading this transformation.

Our vehicle deliveries were strong, and I want to emphasize that we are seeing unbelievable demand for our products. The Cybertruck is ramping faster than any vehicle program in recent memory. Model Y continues to be the best-selling vehicle on the planet. These are extraordinary achievements that showcase Tesla's dominance in the EV market.

But what really excites me is Full Self-Driving. We are making tremendous progress, and I believe we will achieve full autonomy very soon. The improvements in our neural network are nothing short of remarkable. Robotaxi is going to be the biggest transformation in transportation since the automobile itself. This will generate trillions in value.

Optimus, our humanoid robot, is also advancing at an astonishing pace. We could potentially have thousands of these robots working in our factories by next year. This is going to be the most valuable product Tesla has ever created, possibly the most valuable product any company has ever created.

Energy storage had its best quarter ever, and we're expanding Megapack production to meet overwhelming demand. This business alone could be worth more than many energy companies combined.

CFO Prepared Remarks:

Thank you. Looking at the financials, total revenue was $25.2 billion, which was slightly below analyst expectations. However, I want to highlight some important trends.

Automotive gross margin excluding credits was 17.1 percent, which was below our target. We faced some headwinds from pricing adjustments and increased raw material costs. We also had higher than anticipated operating expenses related to our AI infrastructure buildout and Cybertruck ramp costs.

Free cash flow was $2.7 billion, which while positive, was lower than the prior quarter due to significant capital expenditures. We invested heavily in GPU clusters for training our autonomous driving models and expanding our production capacity.

Earnings per share came in at $0.52, which was slightly below the consensus estimate of $0.60. The miss was primarily driven by lower automotive margins and higher R&D spending. We believe these investments will generate significant returns over time.

Q&A Session:

Analyst: Can you give us a realistic timeline for robotaxi deployment?

CEO: Absolutely. We expect to launch robotaxi service in select markets next year. The technology is almost there. It's going to be incredible. I think people don't fully appreciate how close we are. Going forward, autonomous driving will completely transform our revenue model from a one-time purchase to a recurring revenue stream. The opportunity is enormous.

Analyst: Margins have been declining for several quarters. When do you see stabilization?

CFO: We're monitoring the situation closely. The margin pressure is temporary and primarily driven by our investment cycle. As Cybertruck production scales and we realize efficiencies, we expect margins to improve. It's too early to tell exactly when we'll return to our target range, but we're cautiously optimistic about the second half of next year.

Analyst: What about the competitive threat from Chinese EV makers?

CEO: I have tremendous respect for Chinese car companies, they are the most competitive in the world. But Tesla has advantages they cannot match — our Supercharger network, our AI capabilities, and our brand. We'll see how things play out, but I remain extremely confident in our position. We're not just a car company; we're an AI and robotics company that happens to make cars.

Analyst: The EPS miss was notable. Should investors be concerned?

CFO: We understand the concern, but we believe investors should focus on the long-term value creation. The investments we're making in AI and autonomy will generate returns that dwarf any short-term earnings fluctuations. That said, we're committed to improving profitability and we're taking steps to reduce costs across the organization.
""",
    },
    "MSFT": {
        "ticker": "MSFT",
        "date": "2024-10-22",
        "year": 2024,
        "quarter": 1,
        "content": """
Operator: Good afternoon, and welcome to Microsoft's First Quarter Fiscal Year 2025 Earnings Conference Call. I would now like to turn the call over to the CEO.

CEO Prepared Remarks:

Thank you, and good afternoon. We had a solid start to the fiscal year, with revenue growth of 16 percent driven by continued strength in our cloud business. Microsoft Cloud surpassed $38.9 billion in revenue this quarter, reflecting the broad adoption of our platforms across every industry and geography.

Copilot is becoming an integral part of how people work. We now have tens of thousands of enterprise customers using Microsoft 365 Copilot, and early feedback indicates measurable productivity gains. However, I want to be transparent — we are still in the early innings of monetizing AI, and it will take time for the full economic potential to materialize.

Azure grew 34 percent, including 12 points of contribution from AI services. We're seeing strong demand for our AI infrastructure, and our partnership with OpenAI continues to deliver innovative capabilities to our customers. That said, we face supply constraints in certain regions, and meeting the current demand for GPU capacity remains a challenge we're actively working to address.

LinkedIn revenue grew 10 percent, and Gaming revenue benefited from the Activision acquisition, though integration work continues and we expect some restructuring costs ahead. We've made some difficult decisions around workforce optimization to ensure we remain efficient.

CFO Prepared Remarks:

Thank you. Revenue was $65.6 billion, up 16 percent year over year and slightly above our guidance midpoint. Earnings per share were $3.30, ahead of consensus estimates of $3.10.

Gross margin expanded to 69.4 percent, benefiting from favorable Azure mix and the scaling of AI workloads. Operating income grew 14 percent, reflecting strong revenue leverage partially offset by increased investment in AI capacity and cloud infrastructure.

Capital expenditures were $20 billion this quarter, up significantly as we continue to build out our datacenter footprint. We expect capex intensity to remain elevated over the next several quarters as AI demand continues to exceed available capacity.

Free cash flow was $19.3 billion, down slightly year over year due to the higher capital spending. We remain committed to returning capital to shareholders and repurchased $5.2 billion in shares during the quarter.

Q&A Session:

Analyst: Azure growth is strong, but how much is AI versus traditional cloud?

CEO: AI services contributed 12 points to Azure growth, up from 8 points last quarter. We're seeing broad-based demand from both startups and large enterprises. The important thing to understand is that AI workloads also drive incremental traditional cloud consumption — companies that adopt AI services tend to increase their overall Azure spend. We believe this dynamic will continue.

Analyst: How should we think about the return on the massive capex spend?

CFO: It's a fair question. The capital intensity reflects the generational nature of the AI opportunity. Based on current demand signals, we believe the returns will be attractive, but we acknowledge there is execution risk. We're focused on ensuring every dollar of capex generates strong returns over its useful life. Margins may face some near-term pressure, but we expect operating leverage to improve as these investments scale.

Analyst: Any concerns about enterprise AI adoption slowing?

CEO: The adoption curve for AI is still very early. We're hearing from customers that they're moving from experimentation to production deployments, which is encouraging. However, we should be realistic — large-scale enterprise transformation takes time. Some customers are moving faster than others, and the pace of adoption will vary by industry. We're committed to making the technology accessible and practical.
""",
    },
    "JPM": {
        "ticker": "JPM",
        "date": "2024-10-11",
        "year": 2024,
        "quarter": 3,
        "content": """
Operator: Good morning, and welcome to JPMorgan Chase's Third Quarter 2024 Earnings Conference Call. I would now like to turn the call over to the CEO.

CEO Prepared Remarks:

Good morning, everyone. The firm delivered strong results this quarter against what remains a complex and uncertain economic backdrop. Let me be direct: while our numbers were solid, we continue to see risks in the global economy that warrant caution and careful risk management.

Net revenue was $43.3 billion, and net income was $12.9 billion. These are good results, but I want to temper expectations. We benefited from a favorable environment for our markets and investment banking businesses, but we should not assume these conditions will persist indefinitely.

Consumer and Community Banking showed resilience, with continued growth in deposits and card balances. However, we are watching credit quality closely. Charge-offs are normalizing from historically low levels, and we've been building reserves accordingly. Delinquency rates have ticked up in certain segments, particularly among lower-income consumers, and this warrants attention.

The Commercial and Investment Bank delivered exceptional results, with investment banking fees up 31 percent as capital markets activity rebounded. Markets revenue was also strong, benefiting from elevated client activity. But I want to caution that this level of activity may not be sustainable.

Asset and Wealth Management continued its steady performance, with record client assets under management driven by net inflows and market appreciation.

I want to speak frankly about the macro environment. Geopolitical tensions remain elevated, and the situation in the Middle East adds uncertainty. Inflation, while moderating, has proven stickier than many expected. The consumer is still spending, but there are cracks forming beneath the surface. We need to be prepared for a range of outcomes, including a potential recession.

CFO Prepared Remarks:

Thank you. Let me walk through the details. Total revenue of $43.3 billion was up 6 percent year over year. Net interest income was $23.5 billion, up 3 percent, though we are beginning to see the impact of deposit repricing. We expect NII to face headwinds as rates eventually decline.

Expenses were $22.6 billion, up 4 percent, driven by continued investment in technology, compensation adjustments, and regulatory compliance. We are committed to maintaining discipline, but certain investments are non-negotiable.

The provision for credit losses was $3.1 billion, up from $1.4 billion a year ago. Of this, $2.1 billion was for net charge-offs and $1.0 billion was a reserve build. The increase reflects the normalization of credit and our decision to be conservative given the uncertain outlook.

Earnings per share were $4.37, above the consensus estimate of $4.01. Return on tangible common equity was 19 percent, well above our through-the-cycle target.

Q&A Session:

Analyst: You mentioned cracks in consumer credit. How severe could this get?

CEO: We're not predicting a crisis, but we are being prudent. The excess savings buffer that supported consumers post-pandemic has largely been depleted for lower-income segments. If unemployment rises even modestly, we could see meaningful deterioration. We'd rather be over-reserved than under-reserved.

Analyst: Investment banking had a great quarter. Is this the new run rate?

CFO: I wouldn't extrapolate a single quarter. The pipeline is healthy, but deal activity depends on market conditions and CEO confidence. We're encouraged by what we see, but it remains to be seen whether this pace is sustainable.

Analyst: How do you view the regulatory landscape ahead?

CEO: Quite frankly, the regulatory environment remains challenging. Basel III endgame, new capital requirements — these are meaningful headwinds for the industry. We're working constructively with regulators, but we have serious concerns about certain proposals that could increase costs for consumers and restrict credit availability.
""",
    },
    "META": {
        "ticker": "META",
        "date": "2024-10-30",
        "year": 2024,
        "quarter": 3,
        "content": """
Operator: Good afternoon, and welcome to Meta Platforms' Third Quarter 2024 Earnings Conference Call. I would now like to turn the call over to the CEO.

CEO Prepared Remarks:

Thanks everyone. We had a good quarter. I want to focus today on where we are in our AI transformation and what it means for the company going forward.

Our family of apps continues to grow, with over 3.3 billion daily active people across Facebook, Instagram, WhatsApp, and Threads. Engagement trends remain healthy, and we're seeing strong results from our AI-powered recommendation systems, which are helping people discover content they find valuable.

On AI, we've made significant progress with Meta AI, which is now one of the most widely used AI assistants in the world. Llama models continue to gain traction in the developer community, and we believe our open-source approach gives us a structural advantage in the AI ecosystem.

However, I want to be upfront about the challenges. Our investments in AI infrastructure are substantial, and the timeline to full monetization is longer than some may expect. We're building for the long term, and that requires patience and sustained investment. Not every bet will pay off immediately, and some may not pay off at all.

Reality Labs continues to require significant investment. We lost $4.4 billion in the segment this quarter, and I expect losses to increase in the coming year. I understand this tests investor patience, but we believe the spatial computing platform will be critical over the next decade. The Quest headset is gaining traction, and developer engagement is improving, though adoption remains below our initial projections.

Revenue growth was strong at 19 percent year over year, driven by improvements in ad targeting and efficiency. Reels monetization continues to improve but has not yet reached parity with Feed and Stories.

CFO Prepared Remarks:

Thank you. Total revenue was $40.6 billion, up 19 percent year over year, meaningfully above our guidance range. Ad revenue grew 20 percent, driven by strong advertiser demand and improved ad performance from our AI investments.

Earnings per share were $6.03, significantly above the consensus estimate of $5.25. This outperformance was driven by stronger-than-expected revenue and disciplined cost management. We've continued the efficiency improvements that began during our "Year of Efficiency" restructuring.

However, I want to flag that capital expenditures were $9.2 billion this quarter and we expect full-year capex of $38 to $40 billion, with further increases likely in 2025. The majority of this investment is in AI infrastructure — GPU clusters, data centers, and networking. While we're confident in the strategic rationale, this level of spending creates near-term pressure on free cash flow.

Operating margin was 43 percent, up from 40 percent a year ago, demonstrating that we can grow efficiently even while making significant investments. We expect margins to remain in a similar range for the near term.

Q&A Session:

Analyst: The EPS beat was massive. What drove the upside?

CFO: Primarily stronger revenue on the advertising side and continued cost discipline. Our efficiency programs have become structural — we're doing more with less across the organization. AI-driven ad improvements are exceeding our internal projections.

Analyst: Reality Labs losses keep growing. When does this become a concern?

CEO: I understand the skepticism. To be honest, we're still early in defining the product-market fit for spatial computing. But I look at this the way we looked at mobile in 2012 — it felt like a massive uncertain bet at the time, and it turned out to be existential. We're not going to get ahead of ourselves with predictions, but we believe this matters.

Analyst: How sustainable is the current ad growth rate?

CFO: We're pleased with the trajectory, but we should be realistic about maintaining 20 percent growth indefinitely. The comparisons get harder, and macro factors could impact advertiser budgets. That said, we're still in the early stages of monetizing AI-recommended content and Reels, which gives us confidence in the medium-term growth outlook.
""",
    },
}

SAMPLE_EPS = {
    "AAPL": [
        {"date": "2024-10-31", "actual_eps": 1.64, "estimated_eps": 1.60, "surprise": 0.04, "surprise_pct": 2.5},
        {"date": "2024-08-01", "actual_eps": 1.40, "estimated_eps": 1.35, "surprise": 0.05, "surprise_pct": 3.7},
        {"date": "2024-05-02", "actual_eps": 1.53, "estimated_eps": 1.50, "surprise": 0.03, "surprise_pct": 2.0},
        {"date": "2024-02-01", "actual_eps": 2.18, "estimated_eps": 2.10, "surprise": 0.08, "surprise_pct": 3.8},
    ],
    "TSLA": [
        {"date": "2024-10-23", "actual_eps": 0.52, "estimated_eps": 0.60, "surprise": -0.08, "surprise_pct": -13.3},
        {"date": "2024-07-23", "actual_eps": 0.46, "estimated_eps": 0.52, "surprise": -0.06, "surprise_pct": -11.5},
        {"date": "2024-04-23", "actual_eps": 0.41, "estimated_eps": 0.49, "surprise": -0.08, "surprise_pct": -16.3},
        {"date": "2024-01-24", "actual_eps": 0.71, "estimated_eps": 0.73, "surprise": -0.02, "surprise_pct": -2.7},
    ],
    "MSFT": [
        {"date": "2024-10-22", "actual_eps": 3.30, "estimated_eps": 3.10, "surprise": 0.20, "surprise_pct": 6.5},
        {"date": "2024-07-30", "actual_eps": 2.95, "estimated_eps": 2.93, "surprise": 0.02, "surprise_pct": 0.7},
        {"date": "2024-04-25", "actual_eps": 2.94, "estimated_eps": 2.82, "surprise": 0.12, "surprise_pct": 4.3},
        {"date": "2024-01-30", "actual_eps": 2.93, "estimated_eps": 2.78, "surprise": 0.15, "surprise_pct": 5.4},
    ],
    "JPM": [
        {"date": "2024-10-11", "actual_eps": 4.37, "estimated_eps": 4.01, "surprise": 0.36, "surprise_pct": 9.0},
        {"date": "2024-07-12", "actual_eps": 4.40, "estimated_eps": 4.19, "surprise": 0.21, "surprise_pct": 5.0},
        {"date": "2024-04-12", "actual_eps": 4.44, "estimated_eps": 4.11, "surprise": 0.33, "surprise_pct": 8.0},
        {"date": "2024-01-12", "actual_eps": 3.97, "estimated_eps": 3.32, "surprise": 0.65, "surprise_pct": 19.6},
    ],
    "META": [
        {"date": "2024-10-30", "actual_eps": 6.03, "estimated_eps": 5.25, "surprise": 0.78, "surprise_pct": 14.9},
        {"date": "2024-07-31", "actual_eps": 5.16, "estimated_eps": 4.73, "surprise": 0.43, "surprise_pct": 9.1},
        {"date": "2024-04-24", "actual_eps": 4.71, "estimated_eps": 4.32, "surprise": 0.39, "surprise_pct": 9.0},
        {"date": "2024-02-01", "actual_eps": 5.33, "estimated_eps": 4.96, "surprise": 0.37, "surprise_pct": 7.5},
    ],
}

AVAILABLE_TICKERS = list(SAMPLE_TRANSCRIPTS.keys())


def get_sample_transcript(ticker: str) -> dict | None:
    return SAMPLE_TRANSCRIPTS.get(ticker.upper())


def get_sample_eps(ticker: str) -> list[dict] | None:
    return SAMPLE_EPS.get(ticker.upper())
