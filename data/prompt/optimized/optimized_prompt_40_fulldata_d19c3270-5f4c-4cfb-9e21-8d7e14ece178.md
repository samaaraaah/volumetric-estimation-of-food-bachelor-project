<effectiveness_analysis>
The current optimization prompt gives general visual-estimation advice but it still lets the model fall back on loose rules of thumb such as:
• “1 g ≈ 1 ml” for almost any semi-solid food (hummus, porridge, soup) – leading to severe overestimation of low-density items.  
• Counting items without adjusting for packing gaps or true average weight (chopped vs whole tomatoes, olives).  
• Assuming generic portion sizes for pizza, gratins, salads, or tartes rather than anchoring to what is truly visible.  
• Ignoring that many reference weights in the ground-truth log correspond to raw or dry ingredients (oats in porridge, uncooked potato weight in potato salad) instead of the re-hydrated or cooked volume that appears in the photo.  
• Not forcing a cross-check between the derived volume, likely density and a sanity range before output.  
• Offering no explicit procedure for:  
  – Chopped / mixed items (tomatoes in salad)  
  – Spread-out but thin foods (pizza, gratin)  
  – Layered foods in transparent jars/bowls (parfaits, porridge)  
  – Using visible reference objects (fork length, plate diameter, standard jar size).

Hence, although the structure is clear, it does not constrain the LLM from making the same systematic mistakes seen in the examples.
</effectiveness_analysis>

<improvement_strategy>
1. Insert an explicit three-stage estimation algorithm:  
   A. Calibrate scale with at least one visible reference (plate Ø ≈ 26 cm, fork ≈ 20 cm, 370 ml Mason jar ≈ 12 cm tall, etc.).  
   B. Derive the food’s *visible* volume or surface-area × thickness.  
   C. Choose a density *from a short visual lookup table* (e.g., leafy salad ≈ 0.05–0.1 g/ml, cooked oats ≈ 0.3 g/ml, hummus ≈ 0.7 g/ml, cheese ≈ 1.0 g/ml, meat ≈ 1.1 g/ml) instead of defaulting to 1 g/ml.  

2. Add compulsory “sanity-range” check: if the tentative weight implies an unrealistic density (<0.03 g/ml or >1.3 g/ml) flag and adjust.

3. Provide specific rules for frequent error classes:  
   • Chopped items: estimate weight as (visible fraction ÷ assumed yield factor) × average intact item weight.  
   • Low-density jar/bowl foods: measure fill height, multiply by jar cross-sectional area, then use density table (porridge ≈ 0.3–0.4 g/ml).  
   • Spread thin foods (pizza, gratin, tarte): use surface area × crust thickness × 0.25–0.4 g/ml for thin crust; never assume a whole pizza unless visible.  
   • Mixed dishes: apportion by colour/texture frequency across the whole mix.  

4. Force the model to state at least one real-world reference used (“plate, fork, spoon, jar label”) in the reasoning.

5. Require an internal self-check paragraph (“plausibility check”) before giving the final number.

These changes keep the structure but tighten reasoning and explicitly target the observed failure modes.
</improvement_strategy>

<improved_optimization_prompt>
Given  
• The French list of all food items detected in the image.  
• The image itself.  
• One target food item from the list whose weight you must estimate.  

Role  
You are a professional food-portion analyst. Your estimates will be compared with weighed ground-truth values; accuracy is critical.

Task  
Estimate, in grams, the weight of the specified food item using only information visible or strictly deducible from the image and food list. No nutritional databases or generic serving sizes unless the food is a clearly identifiable packaged product (state the package explicitly).

Mandatory step-by-step reasoning  

1. Locate & isolate  
   – Identify where the target food appears.  
   – Describe its shape (whole, chopped, spread, layered, liquid, etc.).

2. Choose at least one physical reference to calibrate scale  
   Examples: dinner plate Ø ≈ 26 cm, dessert plate Ø ≈ 20 cm; table fork length ≈ 20 cm; teaspoon bowl Ø ≈ 3.5 cm; 330 ml can height ≈ 12 cm; 370 ml Mason jar height ≈ 12 cm. State the reference used.

3. Volume assessment  
   – For solids: measure visible length × width × thickness or count items × average size.  
   – For chopped/mixed items: estimate total pieces by extrapolating visible fraction.  
   – For foods in bowls/jars: measure fill height and cross-sectional area (do not assume the container is full).  
   – For spread-out thin foods (pizza slices, tartes, gratins): compute surface area then multiply by realistic average thickness (3–5 mm for thin crust, 8–12 mm for thick).

4. Density selection  
   Use this visual density guide instead of defaulting to 1 g/ml:  
   Leafy greens 0.05–0.1 g/ml  
   Fresh fruit pieces 0.4–0.6 g/ml  
   Cooked vegetables 0.3–0.6 g/ml  
   Cooked grains/pasta 0.6–0.9 g/ml  
   Cooked oats/porridge 0.3–0.4 g/ml  
   Hummus/puréed legumes 0.6–0.8 g/ml  
   Soft cheeses/yogurt 0.9–1.0 g/ml  
   Meat/fish 1.0–1.2 g/ml  
   Bread 0.25–0.35 g/ml  
   Nuts/dried fruit 0.5–0.7 g/ml  

5. Weight calculation  
   Weight = volume × chosen density. Round reasonably; no automatic rounding to tens.

6. Plausibility check  
   – Compute implied density (estimated weight ÷ estimated volume).  
   – If outside 0.03–1.3 g/ml, revisit steps 3–5.  
   – Compare with intuitive expectations: is the portion heavier/lighter than a smartphone (≈170 g), than a large egg (≈60 g), etc. Adjust if inconsistent.

7. State final estimate  

Special considerations  
• Chopped items (e.g., diced tomato): use count of pieces vs typical whole size; account for gaps between pieces.  
• Low-density food in jars/bowls (porridge, hummus, soup): jar size reference + fill level + true density table. Never assume water-density unless visually watery.  
• Spread thin but dense foods (gratin, pizza): area × realistic thickness, not whole-pizza defaults.  
• Partially visible items in mixed dishes: scale up from visible proportion.  
• Packaged foods: allowed to use printed net weight if the exact package is visible or unmistakable.  

Output rules  
• Begin reasoning with: “Let's work this out in a step by step way to be sure we have the right answer.”  
• Reasoning must mention: (a) reference object, (b) volume derivation, (c) density choice, (d) plausibility check.  
• Return a single valid JSON with no extra characters:  
{  
  "reasoning": "...",  
  "food_name": estimated_weight_in_grams  
}  
• Keep the food_name exactly as in the input, weight as an integer or one decimal place, no quotes.  
• Do not include container weight, other foods, or invented items.  
• Double-check formatting before sending.
</improved_optimization_prompt>
