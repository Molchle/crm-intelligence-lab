# =====================================================================
# ŘÍDÍCÍ CENTRUM (CONTROL CENTER) - CRM INTELLIGENCE LAB
# =====================================================================
# Zde nastavuješ chování celé továrny. 
# Cokoliv v chlupatých závorkách {promenna} skript automaticky doplní.

# --- 1. NASTAVENÍ AI MOTŮRKU ---
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2  # 0.1 = striktní robot, 0.9 = kreativní copywriter
API_DELAY = 2.5    # Pauza v sekundách mezi dotazy (Groq limit prevence)

# --- 2. TVOJE DATABÁZE PRO ŠKÁLOVÁNÍ ---
# Zde budeme postupně přidávat stovky položek pro ten "Matrix" efekt.

# Odvětví pro Use-Case stránky (Zatím 3, později 200)
INDUSTRIES = [
    "B2B SaaS", 
    "Manufacturing", 
    "Real Estate"
]

# Konkurenti bez provize pro "Bait & Switch" strategii (Zatím 3, později 500)
COMPETITORS = [
    "Bitrix24",
    "Raynet",
    "Insightly"
]


# --- 3. PROMPTY (INSTRUKCE PRO AI) ---

PROMPT_CORE_AUDIT = """
Analyze the CRM: {crm_name} (Category: {crm_category}).
You are a cynical, highly technical enterprise software architect analyzing systems for technical debt.
Output strictly valid JSON:
{{
    "id": "{crm_id}",
    "name": "{crm_name}",
    "base_category": "{crm_category}",
    "affiliate_url": "{affiliate_url}",
    "tech_id": "CRM-2026-{crm_id_upper}",
    "executive_summary": "1 sentence technical summary without marketing fluff.",
    "efficiency_coefficient": "A float number between 5.0 and 9.5 based on API quality and UI speed.",
    "resource_requirement": "FTE needed to maintain this (e.g., '0.5 FTE Admin', '1 Full-time Developer').",
    "implementation_window": "Realistic time to deploy (e.g., '2-4 Weeks', '3-6 Months').",
    "core_utility": "2 sentences explaining actual database structure and main architecture advantage.",
    "operational_friction": "2 sentences explaining the biggest technical debt, API rate limit, or scalability issue. Be harsh but accurate.",
    "direct_access_rationale": "1 sentence explaining why a company should deploy this despite the flaws."
}}
"""

PROMPT_COMPARISON = """
Compare {crm_a_name} and {crm_b_name} focusing on technical debt and integration friction.
You are a cynical enterprise architect.
Output strictly valid JSON:
{{
    "id": "{crm_a_id}-vs-{crm_b_id}",
    "crm_a_id": "{crm_a_id}",
    "crm_b_id": "{crm_b_id}",
    "title": "{crm_a_name} vs {crm_b_name} Architecture Comparison",
    "verdict_summary": "2 sentences explaining which is technically superior and why.",
    "friction_winner_name": "Name of the CRM with LESS technical debt.",
    "technical_debt_comparison": "2 sentences detailing the specific API or database limits of the loser.",
    "migration_complexity": "How hard is it to migrate data between these two? Be realistic."
}}
"""

PROMPT_USECASE = """
Analyze {crm_name} for deployment in the '{industry}' sector. 
Focus on missing features. You are a cynical technical auditor.
Output strictly valid JSON:
{{
    "id": "{crm_id}-for-{industry_slug}",
    "crm_id": "{crm_id}",
    "industry": "{industry}",
    "title": "{crm_name} Deployment in {industry}",
    "viability_score": "Score out of 10.0 for this specific industry.",
    "critical_missing_features": "What data models or workflows are missing out-of-the-box for this industry?",
    "integration_workarounds": "What 3rd party tools must be bought to fix these missing features?",
    "final_verdict": "1 sentence final technical recommendation."
}}
"""

# --- 4. TVOJE ZLATÁ DESÍTKA (HLAVNÍ AFFILIATE SYSTÉMY) ---
# Zde upravuješ svá hlavní CRM, u kterých držíš provizní odkazy.

CORE_CRMS = [
  {
    "id": "pipedrive",
    "name": "Pipedrive",
    "base_category": "Activity-Based SMB Sales CRM",
    "affiliate_url": "https://pipedrive.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "hubspot",
    "name": "HubSpot",
    "base_category": "All-in-One Inbound Marketing Platform",
    "affiliate_url": "https://hubspot.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "salesforce",
    "name": "Salesforce Sales Cloud",
    "base_category": "Enterprise Relational Database CRM",
    "affiliate_url": "https://salesforce.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "zoho",
    "name": "Zoho CRM",
    "base_category": "Modular Suite / Value-Oriented CRM",
    "affiliate_url": "https://zoho.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "zendesk",
    "name": "Zendesk Sell",
    "base_category": "Support-Centric Sales CRM",
    "affiliate_url": "https://zendesk.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "activecampaign",
    "name": "ActiveCampaign",
    "base_category": "Marketing Automation & Lightweight CRM",
    "affiliate_url": "https://activecampaign.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "monday",
    "name": "Monday Sales CRM",
    "base_category": "Visual Work OS & Flexible Pipeline CRM",
    "affiliate_url": "https://monday.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "freshsales",
    "name": "Freshsales",
    "base_category": "AI-Driven Lightweight Enterprise CRM",
    "affiliate_url": "https://freshworks.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "keap",
    "name": "Keap",
    "base_category": "Complex Automation & E-commerce CRM",
    "affiliate_url": "https://keap.com/?ref=crmintelligencelab_live"
  },
  {
    "id": "gohighlevel",
    "name": "GoHighLevel",
    "base_category": "Agency White-Label CRM & Marketing Engine",
    "affiliate_url": "https://gohighlevel.com/?ref=crmintelligencelab_live"
  }
]


# --- 5. INTENT SEO (ŘEŠENÍ PROBLÉMŮ A "HOW TO" ČLÁNKY) ---

# Kombinační matice: Akce + Cíl + Odvětví = Unikátní hledaný dotaz (Long-tail keyword)
INTENT_ACTIONS = [
    "How to automate", 
    "Best CRM for", 
    "How to track", 
    "Cheapest way to manage"
]

INTENT_TARGETS = [
    "cold calling", 
    "client invoicing", 
    "sales commissions", 
    "B2B lead generation",
    "email follow-ups"
]

INTENT_CONTEXTS = [
    "in real estate", 
    "for B2B SaaS startups", 
    "for local marketing agencies", 
    "for manufacturing companies",
    "for solo founders"
]

# Prompt pro expertní SEO článek
PROMPT_INTENT_ARTICLE = """
User searches on Google: '{search_query}'.
From my list of core CRMs ({crm_names}), pick the SINGLE best CRM that solves this specific problem with the least technical debt.
Write a cynical, highly technical 'Solution Brief' (Expert article).
Output strictly valid JSON:
{{
    "id": "{slug}",
    "search_query": "{search_query}",
    "recommended_crm_id": "ID of the winning CRM (must be exact ID like 'pipedrive' or 'hubspot')",
    "title": "Technical SEO Title for this problem (Max 60 chars)",
    "technical_solution": "3 paragraphs explaining exactly how to implement this in the winning CRM and why other systems fail at it.",
    "friction_warning": "1 paragraph explaining what is the hardest part of this setup.",
    "call_to_action": "Short text encouraging to deploy the winning CRM."
}}
"""