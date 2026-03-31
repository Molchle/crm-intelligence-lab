import json
import os
import time
from dotenv import load_dotenv
from groq import Groq

# 1. NASTAVENÍ A CESTY
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "../frontend/src/content")

DIR_CRMS = os.path.join(CONTENT_DIR, "crms")
DIR_INTEGRATIONS = os.path.join(CONTENT_DIR, "integrations")
DIR_COMPARISONS = os.path.join(CONTENT_DIR, "comparisons")

# Vytvoření složek, pokud neexistují
for d in [DIR_CRMS, DIR_INTEGRATIONS, DIR_COMPARISONS]:
    os.makedirs(d, exist_ok=True)

# 2. TVRDÁ DATA (Žádná AI halucinace! Přesné ceny a affiliate linky)
CORE_CRMS = [
    {"id": "pipedrive", "name": "Pipedrive", "affiliate_url": "https://pipedrive.com/?ref=crmintelligencelab_live", "starting_price": 14, "has_free_tier": False, "primary_category": "Sales CRM", "features": ["Pipeline Management", "Email Tracking", "API Access"]},
    {"id": "hubspot", "name": "HubSpot", "affiliate_url": "https://hubspot.com/?ref=crmintelligencelab_live", "starting_price": 15, "has_free_tier": True, "primary_category": "All-in-One CRM", "features": ["Marketing Hub", "Ticketing", "Custom Objects"]},
    # (Zde si pak doplníš zbytek desítky, pro test necháme tyto dva)
]

# Zkušební seznamy pro tvorbu Matrixu
APPS_TO_INTEGRATE = ["Shopify", "Slack", "QuickBooks"]
COMPETITORS = ["Salesforce", "Zoho", "Bitrix24"]

DIR_USECASES = os.path.join(CONTENT_DIR, "usecases")
os.makedirs(DIR_USECASES, exist_ok=True) # Vytvoří složku, pokud chybí

# Ukázkové obory (Tady jich pak můžeš mít 500)
INDUSTRIES = [
    "Real Estate Brokerages",
    "B2B SaaS Startups",
    "Plumbing and HVAC Contractors"
]



# 3. ZÁPIS TVRDÝCH DAT (Základní kámen)
def build_core_crms():
    print("\n[1/3] Buduji tvrdou databázi CRM systémů...")
    for crm in CORE_CRMS:
        filepath = os.path.join(DIR_CRMS, f"{crm['id']}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(crm, f, indent=2)
        print(f"  -> Uloženo: {crm['id']}.json")


# 4. AI GENERÁTOR PRO INTEGRACE (Model 1)
def build_integrations():
    print("\n[2/3] Spouštím AI pro model: Ekosystém & Integrace...")
    
    prompt_template = """
    Analyze the integration between {core_name} and {app_name}.
    You are a cynical B2B software architect.
    Provide a UNIQUE, highly specific analysis. Do not repeat generic values. 
    
    Output strictly valid JSON with the following keys and rules:
    - "core_crm_id": "{core_id}"
    - "app_name": "{app_name}"
    - "seo_title": String (Max 65 chars)
    - "sync_direction": String (Choose exactly one: 'One-way', 'Two-way', 'Native', or 'Zapier-only')
    - "ai_technical_analysis": String (2 cynically honest paragraphs explaining data mapping and API limits)
    - "friction_rating": Integer (1 to 10, where 10 is terrible. Be accurate, vary the scores based on reality!)
    - "setup_time": String (Realistic time, e.g., '15 Minutes', '4 Hours', '2 Days'. Vary this based on actual complexity!)
    - "pros": Array of 3 short strings
    - "cons": Array of 3 short strings
    - "technical_warning": String (1 sentence highlighting the biggest risk)
    - "integration_steps": Array of 3 short implementation steps
    """
    
    for crm in CORE_CRMS:
        for app in APPS_TO_INTEGRATE:
            filename = f"{crm['id']}-with-{app.lower().replace(' ', '-')}.json"
            filepath = os.path.join(DIR_INTEGRATIONS, filename)
            
            if os.path.exists(filepath):
                continue # Přeskočíme, co už máme (Paměť továrny)
                
            print(f"  -> Analyzuji: {crm['name']} + {app}")
            prompt = prompt_template.format(core_name=crm['name'], core_id=crm['id'], app_name=app)
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                time.sleep(2.5) # Prevence Groq rate limitu
            except Exception as e:
                print(f"     [CHYBA] {e}")


# (Vlož toto pod funkci build_integrations)

def build_comparisons():
    print("\n[3/3] Spouštím AI pro model: Versus (Souboje)...")
    
    prompt_template = """
    Compare {core_name} and {competitor_name}. 
    You are a cynical B2B software architect. You MUST output unique, specific data. Do not repeat generic phrases.
    
    Output strictly valid JSON matching this exact schema:
    {{
      "core_crm_id": "{core_id}",
      "competitor_name": "{competitor_name}",
      "seo_title": "{core_name} vs {competitor_name}: Architecture Comparison (Max 65 chars)",
      "winner": "Must be exactly one of: 'Core', 'Competitor', or 'Tie'",
      "ai_verdict": "2 cynically honest paragraphs explaining database limits and UX of both.",
      "migration_difficulty": "Must be exactly one of: 'Easy', 'Moderate', or 'Nightmare'",
      "core_pros": ["Specific technical pro 1", "Specific pro 2", "Specific pro 3"],
      "competitor_pros": ["Specific technical pro 1", "Specific pro 2", "Specific pro 3"],
      "technical_warning": "1 strict sentence explaining the biggest technical debt of {competitor_name}.",
      "ideal_for_core": "Short phrase describing the exact ideal customer for {core_name} (e.g., 'Mid-market B2B SaaS')"
    }}
    """
    
    for crm in CORE_CRMS:
        for competitor in COMPETITORS:
            # Nechceme porovnávat systém sám se sebou (např. HubSpot vs HubSpot)
            if crm['name'].lower() == competitor.lower():
                continue
                
            filename = f"{crm['id']}-vs-{competitor.lower().replace(' ', '-')}.json"
            filepath = os.path.join(DIR_COMPARISONS, filename)
            
            if os.path.exists(filepath):
                continue
                
            print(f"  -> Analyzuji souboj: {crm['name']} vs {competitor}")
            prompt = prompt_template.format(core_name=crm['name'], core_id=crm['id'], competitor_name=competitor)
            
            try:
                # Zvedneme temperature na 0.4, aby AI generovalo více unikátní výhody a texty
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.4, 
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                time.sleep(2.5)
            except Exception as e:
                print(f"     [CHYBA] {e}")

# ... (Ujisti se, že dole v main() máš tuto funkci přidanou) ...


def build_usecases():
    print("\n[4/4] Spouštím AI pro model: Industry Use-Cases...")
    
    prompt_template = """
    Analyze how {core_name} CRM should be architected and deployed for the '{industry}' industry.
    You are a highly technical B2B solutions architect. Do not use generic marketing fluff.
    
    Output strictly valid JSON matching this exact schema:
    {{
      "core_crm_id": "{core_id}",
      "industry": "{industry}",
      "seo_title": "Best CRM for {industry}: {core_name} Architecture (Max 65 chars)",
      "setup_time": "Realistic deployment time (e.g., '2-3 Weeks', '48 Hours')",
      "compliance_standard": "Primary data compliance for this industry (e.g., 'HIPAA', 'GDPR', 'PCI-DSS', or 'Standard')",
      "industry_pain_points": ["Specific pain point 1", "Specific pain point 2", "Specific pain point 3"],
      "core_solutions": ["Specific {core_name} feature solving point 1", "Feature for point 2", "Feature for point 3"],
      "custom_objects_mapping": ["Deals -> [Industry term for Deals]", "Contacts -> [Industry term for Contacts]", "Companies -> [Industry term]"],
      "ai_architect_verdict": "2 cynically honest paragraphs explaining the custom object architecture and potential API bottlenecks for this specific industry."
    }}
    """
    
    for crm in CORE_CRMS:
        for ind in INDUSTRIES:
            filename = f"{crm['id']}-for-{ind.lower().replace(' ', '-').replace('&', 'and')}.json"
            filepath = os.path.join(DIR_USECASES, filename)
            
            if os.path.exists(filepath):
                continue
                
            print(f"  -> Architektura pro: {crm['name']} v oboru {ind}")
            prompt = prompt_template.format(core_name=crm['name'], core_id=crm['id'], industry=ind)
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3, # Lehce kreativní, aby to trefilo oborový žargon
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                time.sleep(2.5)
            except Exception as e:
                print(f"     [CHYBA] {e}")

# 5. HLAVNÍ SPOUŠTĚČ
def main():
    print("="*50)
    print(" ENTERPRISE DATA BUILDER - G2/CAPTERRA KILLER ")
    print("="*50)
    
    build_core_crms()
    build_integrations()
    build_comparisons() # <-- Přidáno spuštění 3. fáze
    build_usecases() # <-- Tady to přidáš
    
    print("\n[HOTOVO] Továrna zapsala nová data přímo do Astro repozitáře!")

if __name__ == "__main__":
    main()