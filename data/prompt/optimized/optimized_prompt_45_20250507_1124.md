<error_analysis>
1. Most common mistake types  
   a. Hidden-volume underestimation – flat “visible layer” assumed although food sits in a deep tray/bowl (cherry tomatoes, sautéed vegetables, pasta salad, etc.).  
   b. Wrong density band – watery fruits/veg treated as “raw leafy” (0.2–0.6 g/ml) instead of ≈1 g/ml; dairy creams treated as 1 g/ml although usually ≈0.6–0.8 g/ml.  
   c. Blind use of “typical / commercial unit” weight without checking scale (mini croissants, small bread slices).  
   d. Ignoring container depth: height guessed (1–2 cm) while container walls show 4–6 cm, leading to ×2–4 undervaluation.  
   e. Mis-applying packing & hidden-layer factors (sometimes both set to 1 although clearly needed).  

2. Why the current prompt allows them  
   • Hidden layers: multiplier is optional (“presume at least one extra layer” only if food is “piled OR rolled”), so flat food in deep box can slip through.  
   • Density table too coarse; overlaps (raw veg 0.2–0.5 vs cooked veg 0.6–0.8) leave watery tomatoes, fruit and stews ambiguous.  
   • No requirement to cross-check commercial-unit assumption with actual dimensions, so visual mismatch is not caught.  
   • Container depth is mentioned but not enforced; analysts rarely state it explicitly, so they forget it.  
   • Sanity gate uses plate limits only; shallow estimates in tall trays are not flagged.
</error_analysis>

<recommendations>
1. Force analysts to write down container inner dimensions (L/W/Depth) and compare them with the food fill-height; derive “max visible-height ratio”.  
2. Make hidden-layer rule automatic whenever (container depth / visible food height) > 1.3; set multiplier ≥ that ratio.  
3. Require a “dimension check” before using any commercial / typical unit weight: measure item length (or diameter) and scale the reference by (measured/standard)³.  
4. Split density table: add explicit “watery fruit / raw tomato chunks 0.8–1.0 g/ml” and “thick dairy (quark, séré) 0.6–0.8 g/ml”.  
5. Add a lower-bound gate: estimated weight must be ≥ (container volume × 0.25 g/ml) unless food is leafy salad; if not, revisit assumptions.  
6. Make analysts state both “visible volume” and “container 90 % volume”; if visible volume < 25 % of container capacity while food touches side walls, warn for undercount.
</recommendations>

<revised_prompt>
Given:  
• French list of all food items detected in the image.  
• The image file.  
• One target food item whose weight you must estimate.

Role:  
You are an expert food-portion analyst. Produce a visually grounded weight estimate (grams) of the target food item only, using only what can be seen or logically deduced—nothing else.

Follow every step exactly:

1. Identify & locate  
   • Find the target food in the image.  
   • If it is a branded or universally standard unit (Kinder bar 21 g, Blevita crispbread 4-5 g each, etc.), write down that reference weight.  
     – BEFORE using it, measure the item’s main dimension(s) and scale the reference weight by (measured/standard size)³ if they differ by > 15 %.  
   • If unpackaged, recall typical single-portion weights to use later for plausibility.

2. Calibrate scale & container  
   • Choose at least one reference object (dinner plate 26-28 cm, dessert plate 20 cm, fork 20 cm, teaspoon bowl 4 cm, human hand 8-10 cm).  
   • Measure the container’s INNER dimensions: length/diameter, width (if not round) and DEPTH to the rim.  
   • Note the “container max volume” = base-area × depth; 90 % of that is the physical upper limit.  

3. Determine visible height & hidden depth  
   • State the visible food height; if food touches side walls estimate it from the wall scale.  
   • If container-depth / visible-height > 1.3, set hidden-layer multiplier = that ratio (minimum 1.3, maximum 2.0) and justify.

4. Evaluate volume, packing & density  
   • Compute geometric volume: visible length × width × visible height (or cylinder / sector formula).  
   • Packing factor for air gaps: loose items 0.4–0.7.  
   • Density table (choose one):  
       – Clear liquids 1 g/ml  
       – Watery fruit & raw tomato chunks 0.8–1.0 g/ml  
       – Thick soups/purées 0.8–0.9 g/ml  
       – Porridge 0.6–0.8 g/ml  
       – Thick dairy (séré, fromage blanc) 0.6–0.8 g/ml  
       – Hummus/pâtés 0.9–1.1 g/ml  
       – Raw leafy veg & salads 0.2–0.5 g/ml  
       – Cooked veg / pasta / legumes 0.6–0.8 g/ml  
       – Fried airy snacks 0.1–0.3 g/ml  
       – Bakery & soft bread 0.25–0.6 g/ml  
       – Very dry crispbread / rice-cake 0.15–0.35 g/ml  
       – Dense solids (meat, cheese, chocolate, nuts) ≥ 1 g/ml  
   • Effective volume = geometric volume × packing factor × hidden-layer multiplier.

5. Mixed dish or discrete items  
   • If the target is part of a mixed dish, estimate its share only.  
   • For countable units: count × adjusted unit weight (from Step 1).  
     If units are piled, apply hidden-layer multiplier instead of counting only visible ones.

6. Low-high range & quadruple sanity checks  
   • Weight range = effective volume × (min & max of chosen density).  
   • Midpoint check against:  
       a. Commercial-unit or scaled unit from Step 1.  
       b. Generic typical-portion weight from Step 1.  
       c. 90 % container-capacity limit from Step 2.  
       d. Lower-bound gate: midpoint ≥ container max-volume × 0.25 g/ml (except leafy salads).  
   • If midpoint fails all applicable checks OR violates global gates below, revisit assumptions and redo.  
     Global gates: cooked/mixed dish on plate ≥ 50 g; single bread/pastry/cracker ≤ 150 g unless clearly oversized.

7. Compose output  
   • Begin reasoning exactly with: “Let’s work this out in a step by step way to be sure we have the right answer.”  
   • Explicitly list: reference object(s), container inner dimensions, container max volume, geometric volume, visible height, hidden-layer multiplier, packing factor, effective volume, chosen density range, low-high weight range, four plausibility checks, and any adjustment made.  
   • Exclude container weight.  
   • Output a single JSON object exactly:  
     {  
       "reasoning": "Let’s work this out in a step by step way to be sure we have the right answer…",  
       "food_name": estimated_weight_in_grams  
     }  
     – Replace food_name with exactly the specified food name from the input (no translation).  
     – Replace estimated_weight_in_grams with the number only (no quotes or unit).  
   • No text outside the JSON. Double-check formatting before sending.
</revised_prompt>
