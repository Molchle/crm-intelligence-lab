import json
import os
import time
import itertools
from dotenv import load_dotenv
from groq import Groq

# Načtení klíčů
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("CRITICAL ERROR: GROQ_API_KEY nenalezen v .env souboru.")
    exit()

# Inicializace hyper-rychlého Groq klienta
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# Cesty k souborům
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "../data/crms.json")
OUTPUT_AUDITS = os.path.join(BASE_DIR, "../data/enriched_audits.json")
OUTPUT_COMPARE = os.path.join(BASE_DIR, "../data/enriched_comparisons.json")
OUTPUT_USECASES = os.path.join(BASE_DIR, "../data/enriched_usecases.json")

INDUSTRIES = ["B2B SaaS", "Manufacturing", "Real Estate"]

def run_ai_prompt(prompt):
    """Spustí dotaz přes Groq Llama 3 a vynutí striktní JSON výstup."""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a cynical, highly technical enterprise software architect. You strictly analyze systems for technical debt and operational friction. You must output ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.2, # Nízká teplota pro maximální analytickou přesnost
            response_format={"type": "json_object"} # Nativní JSON mode (cheat code)
        )
        # Groq v JSON módu vrací čistý JSON string bez markdownu
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"  [ERROR] Selhání Groq AI generování: {e}")
        return None

def generate_base_audits(crms):
    print("\n=== FÁZE 1: ZÁKLADNÍ TECHNICKÉ AUDITY ===")
    results = []
    for crm in crms:
        print(f"Auditing: {crm['name']}...")
        prompt = f"""
        Analyze the CRM: {crm['name']} (Category: {crm['base_category']}).
        Output strictly valid JSON:
        {{
            "id": "{crm['id']}",
            "name": "{crm['name']}",
            "base_category": "{crm['base_category']}",
            "affiliate_url": "{crm['affiliate_url']}",
            "tech_id": "CRM-2026-{crm['id'][:3].upper()}",
            "executive_summary": "1 sentence technical summary without marketing fluff.",
            "efficiency_coefficient": "A float number between 5.0 and 9.5 based on API quality and UI speed.",
            "resource_requirement": "FTE needed to maintain this (e.g., '0.5 FTE Admin', '1 Full-time Developer').",
            "implementation_window": "Realistic time to deploy (e.g., '2-4 Weeks', '3-6 Months').",
            "core_utility": "2 sentences explaining actual database structure and main architecture advantage.",
            "operational_friction": "2 sentences explaining the biggest technical debt, API rate limit, or scalability issue. Be harsh but accurate.",
            "direct_access_rationale": "1 sentence explaining why a company should deploy this despite the flaws."
        }}
        """
        data = run_ai_prompt(prompt)
        if data:
            results.append(data)
        time.sleep(2.5) # Groq povolí 30 dotazů za minutu. 2.5s je bezpečný interval.
    return results

def generate_comparisons(crms):
    print("\n=== FÁZE 2: SROVNÁVACÍ MATICE (A vs B) ===")
    results = []
    pairs = list(itertools.combinations(crms, 2))
    
    for crm_a, crm_b in pairs:
        print(f"Comparing: {crm_a['name']} vs {crm_b['name']}...")
        prompt = f"""
        Compare {crm_a['name']} and {crm_b['name']} focusing on technical debt and integration friction.
        Output strictly valid JSON:
        {{
            "id": "{crm_a['id']}-vs-{crm_b['id']}",
            "crm_a_id": "{crm_a['id']}",
            "crm_b_id": "{crm_b['id']}",
            "title": "{crm_a['name']} vs {crm_b['name']} Architecture Comparison",
            "verdict_summary": "2 sentences explaining which is technically superior and why.",
            "friction_winner_name": "Name of the CRM with LESS technical debt.",
            "technical_debt_comparison": "2 sentences detailing the specific API or database limits of the loser.",
            "migration_complexity": "How hard is it to migrate data between these two? Be realistic."
        }}
        """
        data = run_ai_prompt(prompt)
        if data:
            results.append(data)
        time.sleep(2.5)
    return results

def generate_usecases(crms):
    print("\n=== FÁZE 3: OBOROVÉ USE-CASE ANALÝZY ===")
    results = []
    
    for crm in crms:
        for industry in INDUSTRIES:
            print(f"Analyzing: {crm['name']} for {industry}...")
            prompt = f"""
            Analyze {crm['name']} for deployment in the '{industry}' sector. Focus on missing features.
            Output strictly valid JSON:
            {{
                "id": "{crm['id']}-for-{industry.lower().replace(' ', '-')}",
                "crm_id": "{crm['id']}",
                "industry": "{industry}",
                "title": "{crm['name']} Deployment in {industry}",
                "viability_score": "Score out of 10.0 for this specific industry.",
                "critical_missing_features": "What data models or workflows are missing out-of-the-box for this industry?",
                "integration_workarounds": "What 3rd party tools must be bought to fix these missing features?",
                "final_verdict": "1 sentence final technical recommendation."
            }}
            """
            data = run_ai_prompt(prompt)
            if data:
                results.append(data)
            time.sleep(2.5)
    return results

def main():
    print("Spouštím GROQ Data Engine (Llama 3 70B)...")
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        crms = json.load(f)

    audits = generate_base_audits(crms)
    with open(OUTPUT_AUDITS, "w", encoding="utf-8") as f:
        json.dump(audits, f, indent=2, ensure_ascii=False)
    
    comparisons = generate_comparisons(crms)
    with open(OUTPUT_COMPARE, "w", encoding="utf-8") as f:
        json.dump(comparisons, f, indent=2, ensure_ascii=False)

    usecases = generate_usecases(crms)
    with open(OUTPUT_USECASES, "w", encoding="utf-8") as f:
        json.dump(usecases, f, indent=2, ensure_ascii=False)

    print("\n[ÚSPĚCH] Generování matice dokončeno!")
    print(f"Vytvořeno: {len(audits)} auditů, {len(comparisons)} srovnání, {len(usecases)} use-case scénářů.")

if __name__ == "__main__":
    main()