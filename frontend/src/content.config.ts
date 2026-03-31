import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

// 1. Schéma pro tvou Zlatou desítku (Tvrdá data)
const crmsCollection = defineCollection({
  // TÍMTO ASTRU ŘÍKÁME: Načti všechny JSON soubory z této složky
  loader: glob({ pattern: "**/*.json", base: "./src/content/crms" }),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    affiliate_url: z.string().url(),
    starting_price: z.number(),
    has_free_tier: z.boolean(),
    primary_category: z.string(),
    features: z.array(z.string()),
  }),
});

// 2. Schéma pro Integrace (Ecosystem Model)
const integrationsCollection = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/integrations" }),
  schema: z.object({
    core_crm_id: z.string(),
    app_name: z.string(),
    seo_title: z.string().max(65),
    sync_direction: z.enum(['One-way', 'Two-way', 'Native', 'Zapier-only']),
    ai_technical_analysis: z.string(),
    friction_rating: z.number().min(1).max(10),
    // --- NOVÁ BOHATÁ DATA ---
    setup_time: z.string(),
    pros: z.array(z.string()),
    cons: z.array(z.string()),
    technical_warning: z.string(),
    integration_steps: z.array(z.string()),
  }),
});

// 3. Schéma pro Versus (Porovnání)
const comparisonsCollection = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/comparisons" }),
  schema: z.object({
    core_crm_id: z.string(),
    competitor_name: z.string(),
    seo_title: z.string().max(65),
    winner: z.enum(['Core', 'Competitor', 'Tie']),
    ai_verdict: z.string(), // 2 odstavce drsného zhodnocení
    migration_difficulty: z.enum(['Easy', 'Moderate', 'Nightmare']),
    core_pros: z.array(z.string()), // Výhody tvého affiliate systému
    competitor_pros: z.array(z.string()), // Výhody cizího systému (musíme být objektivní)
    technical_warning: z.string(), // Co je na cizím systému špatně
    ideal_for_core: z.string(), // Např. "B2B SaaS se 100+ zaměstnanci"
  }),
});

// 4. Schéma pro Industry Use-Cases (Oborová řešení)
const usecasesCollection = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/usecases" }),
  schema: z.object({
    core_crm_id: z.string(),
    industry: z.string(),
    seo_title: z.string().max(65),
    setup_time: z.string(), // e.g., "2-3 Weeks"
    compliance_standard: z.string(), // e.g., "HIPAA", "SOC2", "Standard"
    industry_pain_points: z.array(z.string()), // 3 specifické problémy oboru
    core_solutions: z.array(z.string()), // 3 specifická řešení přes tvůj CRM
    custom_objects_mapping: z.array(z.string()), // e.g., ["Deals -> Property Listings", "Contacts -> Buyers/Sellers"]
    ai_architect_verdict: z.string(), // 2 odstavce drsné analýzy nasazení
  }),
});

// NEZAPOMEŇ AKTUALIZOVAT EXPORT ÚPLNĚ DOLE:
export const collections = {
  'crms': crmsCollection,
  'integrations': integrationsCollection,
  'comparisons': comparisonsCollection,
  'usecases': usecasesCollection, // <-- Přidán Model 3
};


