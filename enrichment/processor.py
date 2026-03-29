import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Konfigurace profesionálního logování
# Výstup v terminálu bude vypadat jako z opravdového serveru
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("CRM_Intelligence_Engine")

# 2. Bezpečné načtení API klíče
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    logger.critical("GEMINI_API_KEY not found in .env file. Halting execution.")
    exit(1)

genai.configure(api_key=API_KEY)

# Použijeme rychlý a přesný model ideální pro zpracování textu a JSONu
MODEL_NAME = 'gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# 3. MASTER PROMPT - Srdce celého projektu
# Psáno v angličtině pro maximální pochopení nuancí modelu.
MASTER_PROMPT = """
You are a highly compensated, deeply cynical Enterprise B2B Solutions Architect. 
Your job is to audit CRM systems for technical buyers, CTOs, and pragmatic CFOs.
You absolutely despise marketing fluff, buzzwords, and overly optimistic sales pitches. 
Your writing style is highly technical, dry, objective, and brutally honest.

CRITICAL RULE: DO NOT use any of the following words under any circumstances: 
revolutionary, empower, seamless, game-changer, unlock, synergies, next-level, robust, intuitive.

Analyze the following CRM system: 
Target Name: "{crm_name}"
Primary Category: "{crm_category}"

Generate a STRICTLY VALID JSON object with the following keys. ALL content MUST be written in English.
Do NOT wrap the output in markdown code blocks. Just output raw JSON.

Structure requirements:
- "executive_summary": (String) A brutally honest, one-sentence summary of what this CRM actually is.
- "core_utility": (String) 2-3 sentences explaining its actual technical capability and primary use-case without any sugar-coating.
- "operational_friction": (String) The "Trust Key". Identify a specific, highly realistic technical debt, limitation, or implementation pain-point (e.g., "GraphQL API rate limits on lower tiers", "Overly complex custom object schema mapping"). Be highly specific.
- "resource_requirement": (String) A pragmatic estimate of the personnel needed to run it (e.g., "0.5 FTE Admin", "Requires dedicated Dev/Ops").
- "efficiency_coefficient": (Float) A number between 9.0 and 9.8 representing the technical ROI. (e.g., 9.4)
- "implementation_window": (String) A realistic, non-marketing timeline for deployment (e.g., "4-6 Weeks", "Minimum 3 Months").
- "direct_access_rationale": (String) The cold, hard reason why an engineering or ops team should deploy this system *despite* its friction.
"""

def process_crm_database(input_path: str, output_path: str):
    logger.info("Initializing Data Enrichment Sequence...")
    
    # Kontrola, zda existuje vstupní soubor
    if not os.path.exists(input_path):
        logger.error(f"Input artifact missing at: {input_path}")
        return

    # Načtení surových (seed) dat
    with open(input_path, 'r', encoding='utf-8') as f:
        try:
            crms = json.load(f)
        except json.JSONDecodeError:
            logger.error("Input file is not a valid JSON. Check syntax.")
            return

    enriched_database = []

    # Iterace přes každý CRM záznam
    for crm in crms:
        logger.info(f"Target locked: Auditing {crm['name']}...")
        
        # Dosazení dat do promptu
        prompt = MASTER_PROMPT.format(
            crm_name=crm['name'], 
            crm_category=crm['base_category']
        )
        
        try:
            # Volání Gemini API
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", # Vynucení JSON formátu
                    temperature=0.15 # Téměř nulová teplota zaručí analytický, ne-kreativní tón
                )
            )
            
            # Převedení textové odpovědi do Python slovníku (dictionary)
            ai_data = json.loads(response.text)
            
            # Sloučení (merge) surových dat s obohacenými AI daty
            enriched_crm = {**crm, **ai_data}
            
            # Vygenerování estetického technického ID pro frontend (např. CRM-2026-PIP)
            prefix = str(crm['id'])[:3].upper()
            enriched_crm['tech_id'] = f"CRM-2026-{prefix}"
            
            enriched_database.append(enriched_crm)
            logger.info(f"[SUCCESS] {crm['name']} audited. Coeff: {ai_data.get('efficiency_coefficient')}")
            
        except json.JSONDecodeError as e:
            logger.error(f"[FAIL] {crm['name']} - API did not return valid JSON. Error: {e}")
        except Exception as e:
            logger.error(f"[FAIL] {crm['name']} - Unexpected Error: {str(e)}")

    # Uložení kompletně obohacených dat
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_database, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Sequence complete. Artifact saved to: {output_path}")

if __name__ == "__main__":
    # Nastavení relativních cest (počítá s tím, že skript spouštíš ze složky 'enrichment')
    INPUT_FILE = os.path.join("..", "data", "crms.json")
    OUTPUT_FILE = os.path.join("..", "data", "enriched_crms.json")
    
    process_crm_database(INPUT_FILE, OUTPUT_FILE)