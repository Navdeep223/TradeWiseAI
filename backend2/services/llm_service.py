import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================================================
# 1️⃣ HS CLASSIFICATION EXPLANATION
# =========================================================

def generate_hs_explanation(top_matches: list) -> str:

    hs_section = ""
    for i, item in enumerate(top_matches[:3], start=1):
        hs_section += f"""
Rank {i}:
HS Code: {item.get("hs_code")}
Description: {item.get("description")}
Confidence: {item.get("confidence")}
"""

    prompt = f"""
You are a trade classification analyst.

Explain why the top-ranked HS code is the strongest match
based purely on semantic similarity ranking.

Do NOT discuss route or tariff logic.

HS DATA:
{hs_section}

Respond in 1–2 professional paragraphs only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You provide precise, analytical trade classification insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message.content


# =========================================================
# 2️⃣ AI ROUTE EXPLANATION
# =========================================================

def generate_ai_route_explanation(data: dict) -> str:

    prompt = f"""
You are a trade optimization strategist.

Explain why {data.get("recommended_country")} is the optimal sourcing origin.

Use ONLY the following values:

Landed Cost: {data.get("landed_cost_recommended")}
Comparison Cost: {data.get("landed_cost_comparison")}
Tariff Rate: {data.get("tariff_rate_recommended")}
Freight Cost: {data.get("freight_cost_recommended")}
Cost Advantage: {data.get("cost_difference_percent")}

Provide:
- Route Optimization Insight
- Strategic Recommendation

Be concise and executive in tone.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You provide executive-level trade intelligence summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content


# =========================================================
# 3️⃣ MANUAL ROUTE EXPLANATION
# =========================================================

def generate_manual_route_explanation(data: dict) -> str:

    prompt = f"""
You are a trade cost analyst.

Explain the cost structure of the selected manual route.

Use ONLY:

Origin: {data.get("recommended_country")}
Landed Cost: {data.get("landed_cost_recommended")}
Tariff Rate: {data.get("tariff_rate_recommended")}
Freight Cost: {data.get("freight_cost_recommended")}
Risk Driver: {data.get("main_risk_driver")}

Provide:
- Manual Route Insight
- Risk Commentary

Keep it analytical and concise.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You provide structured trade cost analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content