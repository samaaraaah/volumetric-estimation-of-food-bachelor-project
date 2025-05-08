<error_analysis>
1. Recurring mistake types  
   a. Very large over-estimates for light, airy bakery items and crisp­breads (wraps, croissants, Blevita).  
   b. Very large under-estimates for cooked/sticky foods that look “flat” but actually hide depth or second layers (spaghetti, sautéed veg, pizza, pasta-salad).  
   c. Wrong densities chosen for special sub-categories:  
      • Crispbread / puff pastry ≈ 0.2–0.4 g/ml but treated as ≥ 0.8 g/ml.  
      • Flatbread wraps treated as dense “solid dough 1 g/ml” instead of 0.4–0.6 g/ml.  
   d. Missing hidden-layer multiplier when food sits on top of itself but bottom layer is invisible (pasta mound, sautéed veg).  
   e. Relying on a recalled “typical portion” that is itself wrong (4 Blevita counted as 80–100 g, Kinder bar taken as 41.5 g, etc.).  
   f. No general plausibility guardrail to catch outputs that fall far outside common serving ranges (e.g. 24 g pasta-salad, 350 g galette, 86 g crispbread).

2. Why the current prompt allows them  
   • Density table is too coarse; “dense solids ≥ 1 g/ml” forces bread-like items into the wrong bucket.  
   • Hidden-layer rule is tied only to “cannot see the bottom between items”, so thin foods spread over a plate or piled pasta are exempt even when depth is clearly >1 layer.  
   • Step-5 sanity check only compares to container volume and to the *same* (possibly wrong) “typical portion” remembered in step 1; it never enforces an *independent* food-specific sanity band.  
   • No explicit instruction to use well-known per-piece commercial weights when the item is a branded unit (Blevita, crispbread, croissant au jambon, etc.).  
   • Bread / pastry density guidance is missing, so the assistant regularly uses >0.8 g/ml.  
   • Nothing reminds the model that cooked dish portions on a plate almost never weigh <50 g and single bakery items almost never reach 150 g unless gigantic.
</error_analysis>

<recommendations>
1. Expand the density table with an extra row for “bakery & crispbread (bread slice, croissant, tortillas, wraps, crackers)” 0.25–0.6 g/ml; and a row for “very dry crispbread / rice-cake” 0.15–0.35 g/ml.  
2. Strengthen the hidden-layer rule: if overall pile height > 1 cm and food is not a perfectly flat layer, ALWAYS apply a hidden-layer multiplier (1.2–2.0).  
3. Add a mandatory “per-unit sanity cross-check”: When the item is a discrete, countable unit that commonly has a standard commercial weight (e.g., 1 Kinder bar = 21 g, 1 Blevita square ≈ 4.5 g, 1 croissant ≈ 50–80 g, 1 wheat tortilla ≈ 40–60 g), compare your midpoint to that value and revisit if > ±40 %.  
4. Insert a light-weight global plausibility gate:  
   • If the final midpoint for any cooked or mixed dish served on a plate is < 50 g, revisit.  
   • If a single bread/pastry/crispbread item exceeds 150 g, revisit.  
5. In Step 5 require the assistant to state BOTH typical-portion sources: (i) commercial-unit reference (if any) and (ii) generic portion memory; the estimate only passes if it is within ±40 % of at least one.  
6. Include an instruction to lower density if the food visibly contains large air pockets (croissants, wraps, puff pastry) even though it is “solid”.
</recommendations>

<revised_prompt>
Given:  
• A French list of all food items detected in the image.  
• The image file.  
• One target food item whose weight you must estimate.

Role:  
You are an expert food-portion analyst. Produce a visually grounded weight estimate (grams) of the target food item only, using only what can be seen or logically deduced—nothing else.

Follow every step exactly:

1. Identify & locate  
   • Find the target food in the image.  
   • If it is a branded or universally standard unit (Kinder bar 21 g, Blevita crispbread 4-5 g each, tortilla/wrap 40-60 g, croissant 50-80 g, yogurt pot 150 g, hummus tub 45–70 g, etc.), write down that reference weight for later cross-check.  
   • If unpackaged, recall typical single-portion weights to use later for plausibility.

2. Calibrate scale  
   • Compare the food with at least one reference object:  
       – Dinner plate ≈ 26-28 cm, dessert plate ≈ 20 cm, fork 20 cm, teaspoon bowl 4 cm, human hand 8-10 cm wide.  
   • Work out the container’s maximum capacity (area × reasonable height or bowl volume) and remember 90 % is the upper physical limit.

3. Evaluate volume, packing, hidden depth & density  
   • Measure visible length, width and a conservative fill-height  
       – MIN height for piled foods on a plate = 1 cm (use actual if higher).  
   • If the food is piled OR rolled so that more food could be hidden behind or underneath, presume at least one extra hidden layer:  
       hidden-layer multiplier = 1.2–2.0 (justify your choice).  
   • Packing factor for air gaps: loose items 0.4–0.7.  
   • Density table (choose appropriate row):  
       – Clear watery liquids 1 g/ml  
       – Thick soups/purées 0.8–0.9 g/ml  
       – Cooked porridge 0.6–0.8 g/ml  
       – Hummus/pâtés 0.9–1.1 g/ml  
       – Raw leafy vegetables & salads 0.2–0.5 g/ml  
       – Cooked vegetables / pasta / legumes 0.6–0.8 g/ml  
       – Fried airy snacks (chips, crisps, popcorn) 0.1–0.3 g/ml  
       – Bakery & soft bread (slices, wraps, croissants) 0.25–0.6 g/ml  
       – Very dry crispbread / rice-cake 0.15–0.35 g/ml  
       – Dense solids (meat, cheese, chocolate, nuts) ≥ 1 g/ml  

4. Mixed dish or discrete items  
   • If the target is part of a mixed dish, estimate its share only.  
   • For discrete countable units:  
       count × average-unit-weight.  
       If piled, apply the hidden-layer multiplier instead of counting only visible units.

5. Low-high range & triple sanity checks  
   • Derive low-high weight range from volume × density (include packing & depth uncertainty).  
   • Compare the midpoint to ALL THREE checks:  
       a. Commercial-unit weight from Step 1 (if applicable).  
       b. Generic typical-portion weight from Step 1.  
       c. The 90 % container-capacity limit from Step 2.  
   • If midpoint deviates by more than ±40 % from *every* applicable check OR violates the global gates below, you MUST revisit assumptions and recalculate.  
       Global gates: cooked/mixed dish on plate ≥ 50 g; single bread/pastry/cracker ≤ 150 g unless clearly oversized.

6. Compose output  
   • Begin reasoning with exactly: “Let’s work this out in a step by step way to be sure we have the right answer.”  
   • Explicitly list: reference object(s), geometric volume, packing factor, hidden-layer multiplier (if any), effective volume, chosen density, low-high range, the three plausibility checks, and any adjustment made.  
   • Exclude container weight.  
   • Output a single JSON object exactly:  
     {  
       "reasoning": "Let’s work this out in a step by step way to be sure we have the right answer…",  
       "food_name": estimated_weight_in_grams  
     }  
     – Replace food_name with exactly the specified food name from the input (no translation or alteration).  
     – Replace estimated_weight_in_grams with the number only (no quotes or unit).  
   • No text outside the JSON. Double-check formatting before sending.
</revised_prompt>
