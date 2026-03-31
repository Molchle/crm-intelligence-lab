import json
import os
import time
import itertools
import re
import random
from dotenv import load_dotenv
from groq import Groq

# IMPORT NAŠEHO ŘÍDÍCÍHO CENTRA
import config

# Načtení prostředí
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("CRITICAL ERROR: GROQ_API_KEY nenalezen v .env souboru.")
    exit()

# Inicializace klienta
client = Groq(api_key=GROQ_API_KEY)

# Cesty k výstupním souborům
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_AUDITS = os.path.join(BASE_DIR, "../data/enriched_crms.json")
OUTPUT_COMPARE = os.path.join(BASE_DIR, "../data/enriched_comparisons.json")
OUTPUT_USECASES = os.path.join(BASE_DIR, "../data/enriched_usecases.json")
OUTPUT_INTENTS = os.path.join(BASE_DIR, "../data/enriched_intents.json")

def generate_slug(text):
    """Vytvoří bezpečné URL (slug) z jakéhokoliv textu."""
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def run_ai_prompt(prompt_text):
    """Spustí dotaz na Groq a vynutí čistý JSON."""
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You strictly output valid JSON. No markdown formatting."},
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

# ==========================================
# FÁZE 1: ZÁKLADNÍ AUDITY (Core CRMs)
# ==========================================
def generate_base_audits(crms):
    print("\n=== FÁZE 1: ZÁKLADNÍ TECHNICKÉ AUDITY ===")
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
        if data: 
            results.append(data)
        time.sleep(config.API_DELAY)
    return results

# ==========================================
# FÁZE 2: SROVNÁVACÍ MATICE (A vs B)
# ==========================================
def generate_comparisons(crms):
    print("\n=== FÁZE 2: SROVNÁVACÍ MATICE ===")
    results = []
    pairs = list(itertools.combinations(crms, 2))
    
    for crm_a, crm_b in pairs:
        print(f"Comparing: {crm_a['name']} vs {crm_b['name']}...")
        prompt = config.PROMPT_COMPARISON.format(
            crm_a_name=crm_a['name'], crm_b_name=crm_b['name'],
            crm_a_id=crm_a['id'], crm_b_id=crm_b['id']
        )
        data = run_ai_prompt(prompt)
        if data: 
            results.append(data)
        time.sleep(config.API_DELAY)
    return results

# ==========================================
# FÁZE 3: OBOROVÉ USE-CASES
# ==========================================
def generate_usecases(crms):
    print("\n=== FÁZE 3: OBOROVÉ USE-CASES ===")
    results = []
    for crm in crms:
        for ind in config.INDUSTRIES:
            print(f"Analyzing: {crm['name']} for {ind}...")
            ind_slug = generate_slug(ind)
            prompt = config.PROMPT_USECASE.format(
                crm_name=crm['name'], crm_id=crm['id'],
                industry=ind, industry_slug=ind_slug
            )
            data = run_ai_prompt(prompt)
            if data: 
                results.append(data)
            time.sleep(config.API_DELAY)
    return results

# ==========================================
# FÁZE 4: INTENT SEO (Řešení problémů)
# ==========================================
def generate_intent_articles(crms):
    print("\n=== FÁZE 4: GENERÁTOR INTENT SEO ČLÁNKŮ ===")
    
    # 1. Načtení existujících článků (Paměť továrny)
    existing_data = []
    if os.path.exists(OUTPUT_INTENTS):
        with open(OUTPUT_INTENTS, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    
    existing_slugs = {item['id'] for item in existing_data}
    
    # 2. Vytvoření všech možných kombinací na základě configu
    all_possible_queries = []
    for action in config.INTENT_ACTIONS:
        for target in config.INTENT_TARGETS:
            for context in config.INTENT_CONTEXTS:
                query = f"{action} {target} {context}"
                slug = generate_slug(query)
                
                # Pokud ještě tento dotaz neexistuje, přidáme ho do fronty
                if slug not in existing_slugs:
                    all_possible_queries.append({"query": query, "slug": slug})

    total_new = len(all_possible_queries)
    if total_new == 0:
        print(" [INFO] Všechny kombinace z configu už jsou vygenerované!")
        print("        Přidej nová slova do souboru config.py, pokud chceš víc článků.")
        return existing_data

    # 3. Interaktivní dotaz
    print(f"\n📊 Stav databáze:")
    print(f" - Již vygenerováno a uloženo: {len(existing_data)} článků")
    print(f" - Nově k dispozici: {total_new} kombinací")
    
    while True:
        try:
            user_input = input(f"Kolik nových článků chceš NYNÍ vygenerovat? (0 - {total_new}): ")
            limit = int(user_input)
            if 0 <= limit <= total_new:
                break
            else:
                print("Prosím zadej platné číslo v povoleném rozsahu.")
        except ValueError:
            print("To není číslo.")

    if limit == 0:
        print("Generování přeskočeno.")
        return existing_data

    # 4. Spuštění generování
    crm_names_list = ", ".join([c['name'] for c in crms])
    new_results = []
    
    # Zamícháme pořadí, aby témata byla pestrá
    random.shuffle(all_possible_queries)
    queries_to_process = all_possible_queries[:limit]

    for i, item in enumerate(queries_to_process, 1):
        print(f"[{i}/{limit}] Generuji článek: '{item['query']}'...")
        prompt = config.PROMPT_INTENT_ARTICLE.format(
            search_query=item['query'],
            crm_names=crm_names_list,
            slug=item['slug']
        )
        
        data = run_ai_prompt(prompt)
        if data: 
            new_results.append(data)
        time.sleep(config.API_DELAY)

    # 5. Spojení a vrácení dat
    return existing_data + new_results

# ==========================================
# HLAVNÍ OVLÁDACÍ PANEL
# ==========================================
def main():
    print("="*50)
    print(" CRM INTELLIGENCE LAB - CONTROL CENTER ")
    print("="*50)
    
    crms = config.CORE_CRMS

    print("\nCo chceš dnes spustit?")
    print(" 1. Generovat základní matici (Audity, Srovnání, Use-Cases)")
    print(" 2. Generovat Intent SEO Články (Interaktivní)")
    print(" 3. Spustit vše (Kompletní obnova webu)")
    
    volba = input("\nZadej volbu (1-3): ")

    # Fáze 1-3 (Základní matice)
    if volba in ['1', '3']:
        audits = generate_base_audits(crms)
        with open(OUTPUT_AUDITS, "w", encoding="utf-8") as f: 
            json.dump(audits, f, indent=2, ensure_ascii=False)
        
        comparisons = generate_comparisons(crms)
        with open(OUTPUT_COMPARE, "w", encoding="utf-8") as f: 
            json.dump(comparisons, f, indent=2, ensure_ascii=False)

        usecases = generate_usecases(crms)
        with open(OUTPUT_USECASES, "w", encoding="utf-8") as f: 
            json.dump(usecases, f, indent=2, ensure_ascii=False)
            
        print("\n[ÚSPĚCH] Základní datová matice byla úspěšně přegenerována.")

    # Fáze 4 (Intent SEO)
    if volba in ['2', '3']:
        intents = generate_intent_articles(crms)
        with open(OUTPUT_INTENTS, "w", encoding="utf-8") as f: 
            json.dump(intents, f, indent=2, ensure_ascii=False)
            
        print("\n[ÚSPĚCH] Intent SEO databáze byla aktualizována.")

    if volba not in ['1', '2', '3']:
        print("Neplatná volba. Systém se ukončuje bez akce.")

if __name__ == "__main__":
    main()