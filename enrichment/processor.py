import json
import os
import time
import itertools
from dotenv import load_dotenv
from groq import Groq

# IMPORT NAŠEHO NOVÉHO ŘÍDÍCÍHO CENTRA
import config

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("CRITICAL ERROR: GROQ_API_KEY nenalezen v .env souboru.")
    exit()

client = Groq(api_key=GROQ_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "../data/crms.json")
OUTPUT_AUDITS = os.path.join(BASE_DIR, "../data/enriched_crms.json")
OUTPUT_COMPARE = os.path.join(BASE_DIR, "../data/enriched_comparisons.json")
OUTPUT_USECASES = os.path.join(BASE_DIR, "../data/enriched_usecases.json")

def run_ai_prompt(prompt_text):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You strictly output valid JSON."},
                {"role": "user", "content": prompt_text}
            ],
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"  [ERROR] Groq selhal: {e}")
        return None

def generate_base_audits(crms):
    print("\n=== FÁZE 1: ZÁKLADNÍ AUDITY ===")
    results = []
    for crm in crms:
        print(f"Auditing: {crm['name']}...")
        prompt = config.PROMPT_CORE_AUDIT.format(
            crm_name=crm['name'],
            crm_category=crm['base_category'],
            crm_id=crm['id'],
            affiliate_url=crm['affiliate_url'],
            crm_id_upper=crm['id'][:3].upper()
        )
        data = run_ai_prompt(prompt)
        if data: results.append(data)
        time.sleep(config.API_DELAY)
    return results

def generate_comparisons(crms):
    print("\n=== FÁZE 2: SROVNÁVACÍ MATICE (A vs B) ===")
    results = []
    pairs = list(itertools.combinations(crms, 2))
    for crm_a, crm_b in pairs:
        print(f"Comparing: {crm_a['name']} vs {crm_b['name']}...")
        prompt = config.PROMPT_COMPARISON.format(
            crm_a_name=crm_a['name'], crm_b_name=crm_b['name'],
            crm_a_id=crm_a['id'], crm_b_id=crm_b['id']
        )
        data = run_ai_prompt(prompt)
        if data: results.append(data)
        time.sleep(config.API_DELAY)
    return results

def generate_usecases(crms):
    print("\n=== FÁZE 3: OBOROVÉ USE-CASES ===")
    results = []
    for crm in crms:
        for ind in config.INDUSTRIES:
            print(f"Analyzing: {crm['name']} for {ind}...")
            ind_slug = ind.lower().replace(' ', '-')
            prompt = config.PROMPT_USECASE.format(
                crm_name=crm['name'], crm_id=crm['id'],
                industry=ind, industry_slug=ind_slug
            )
            data = run_ai_prompt(prompt)
            if data: results.append(data)
            time.sleep(config.API_DELAY)
    return results

def main():
    print("Spouštím GROQ Data Engine z nového Control Centra...")
    
    # KROK 1: Načteme tvou zlatou desítku přímo z configu (už žádný externí soubor)
    crms = config.CORE_CRMS

    audits = generate_base_audits(crms)
    with open(OUTPUT_AUDITS, "w", encoding="utf-8") as f: 
        json.dump(audits, f, indent=2, ensure_ascii=False)
    
    comparisons = generate_comparisons(crms)
    with open(OUTPUT_COMPARE, "w", encoding="utf-8") as f: 
        json.dump(comparisons, f, indent=2, ensure_ascii=False)

    usecases = generate_usecases(crms)
    with open(OUTPUT_USECASES, "w", encoding="utf-8") as f: 
        json.dump(usecases, f, indent=2, ensure_ascii=False)

    print("\n[ÚSPĚCH] Systém úspěšně vygeneroval data z nového configu!")

if __name__ == "__main__":
    main()