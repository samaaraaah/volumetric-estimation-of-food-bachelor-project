<error_analysis>
1. Repeated error types  
   a. Depth-blind counting: For pileable discrete items (cherry tomatoes, sautéed vegetables, rice, pasta) the model counted/volumised only the visible top layer and ignored hidden layers → huge under-estimates.  
   b. Wrong density tables: “Chips”, cooked vegetables, pasta were often assigned water-like densities (0.8-1 g/ml) even though fried chips are ~0.2 g/ml and cooked veg/pasta ~0.6–0.8 g/ml → large over-estimates.  
   c. Missing “sanity-check veto”: Step 5 exists but the model still kept numbers far outside Swiss typical portions (e.g. 430 g sere maigre, 320 g for 5 small drumettes).  
   d. Package/standard size not exploited: Cherry-tomato tray and Kinder bar show that, when a commercial or produce-tray standard exists, using it is safer than geometry.  
   e. Hidden units in piles: Counting tomatoes, olives etc. by visible units only, without an allowance for the ones beneath, produced big errors.

2. Why the current prompt fails  
   • Depth allowance and hidden-unit reminder are only implicit under “packing factor”; models treat packing as air gaps, not unseen food.  
   • Density table lacks low-density dry snack category and clear cooked-vs-raw vegetable guidance.  
   • Step 5 merely says “compare”; it does not oblige the model to revise if outside a tolerance band.  
   • Commercial-size hint is limited to a few dairy/confectionery examples; common produce trays or meat cuts are not mentioned.  
   • Discrete-item rule does not tell how to upscale from visible count to full pile.
</error_analysis>

<recommendations>
1. Add an explicit “hidden layers / depth multiplier” bullet under Step 3 or Step 4 that forces the model to check whether items are piled higher than one layer and, for countable items, to add an allowance (e.g., +30-70 %).  
2. Extend the density table with two extra rows:  
   – “Fried, airy snacks (chips, crisps, popcorn)” 0.1–0.3 g/ml  
   – “Cooked vegetables / pasta / legumes” 0.6–0.8 g/ml  
   This removes guesswork.  
3. Strengthen Step 5: “If midpoint estimate is > ±40 % outside BOTH typical portion AND container-capacity checks, you MUST adjust assumptions and recalculate.”  
4. Broaden the commercial-size memo in Step 1 with a short list of common produce trays & meat pieces: cherry-tomato punnet 250 g / 500 g, cooked chicken drumette 20–35 g each, etc.  
5. In the discrete-item bullet add: “If items are piled (edges of dish not visible between them), assume at least one additional hidden layer (multiply visible count by 1.5–2.0 unless bottom clearly seen).”
</recommendations>

<revised_prompt>
Given:  
• A list (in French) of all food items detected in the image.  
• The image file itself.  
• One target food item whose weight you must estimate.

Role:  
You are an expert food-portion analyst. Produce a visually grounded weight estimate (grams) of the target food item only, using what can be seen or logically deduced—nothing else.

Follow every step exactly:

1. Identify & locate  
   • Find the target food in the image.  
   • If it is in a commercial or produce package, first recall common Swiss single-unit sizes:  
       – Yogurt pot 150 g, hummus tub 45–70 g, KitKat 41.5 g, Kinder bar 21 g, cherry-tomato punnet 250 g / 500 g, cooked chicken drumette 20–35 g each, etc.  
     Use that weight when appropriate and justify.  
   • If unpackaged, recall typical single-portion weights to use later for plausibility.

2. Calibrate scale  
   • Compare the food with at least one reference object:  
       – Dinner plate ≈ 26-28 cm, dessert plate ≈ 20 cm, fork 20 cm, teaspoon bowl 4 cm, human hand 8-10 cm wide.  
   • Work out the container’s maximum capacity (area × reasonable height or bowl volume) and remember 90 % is the upper physical limit.

3. Evaluate volume, packing, hidden depth & density  
   • Measure visible length, width and a conservative fill-height (max ≈ 3 cm on flat plate, 5 cm in bowl unless obviously deeper).  
   • If the food is piled so you cannot see the bottom between items (e.g., cherry tomatoes, olives, chips), presume at least one extra hidden layer:  
       hidden-layer multiplier = 1.3–2.0 depending on pile height—state your choice.  
   • Packing factor for air gaps: loose items 0.4–0.7.  
   • Effective volume = geometric volume × packing factor × hidden-layer multiplier (if used).  
   • Choose density from:  
       – Clear watery liquids 1 g/ml  
       – Thick soups/purées 0.8–0.9 g/ml  
       – Cooked porridge 0.6–0.8 g/ml  
       – Hummus/pâtés 0.9–1.1 g/ml  
       – Raw leafy vegetables & salads 0.2–0.5 g/ml  
       – Cooked vegetables / pasta / legumes 0.6–0.8 g/ml  
       – Fried airy snacks (chips, crisps, popcorn) 0.1–0.3 g/ml  
       – Dense solids (meat, cheese, nuts, chocolate) ≥ 1 g/ml  

4. Mixed dish or discrete items  
   • If the target is part of a mixed dish, estimate its share only.  
   • For discrete countable units:  
       count × average-unit-weight.  
       If piled, apply the hidden-layer multiplier as above instead of counting only the visible units.

5. Low-high range & mandatory sanity checks  
   • Derive low-high weight range from volume × density (include packing & depth uncertainty).  
   • Compare the midpoint to BOTH:  
       – Typical portion weights recalled in Step 1, and  
       – The 90 % container-capacity limit from Step 2.  
   • If midpoint deviates by more than ±40 % from BOTH checks, you MUST revisit assumptions and recalculate until it fits at least one.

6. Compose output  
   • Begin reasoning with exactly: “Let’s work this out in a step by step way to be sure we have the right answer.”  
   • Explicitly list: reference object(s), geometric volume, packing factor, hidden-layer multiplier (if any), effective volume, density, low-high range, and both plausibility checks.  
   • Exclude container weight.  
   • Output a single JSON object exactly:  
     {  
       "reasoning": "Let’s work this out in a step by step way to be sure we have the right answer…",  
       "food_name": estimated_weight_in_grams  
     }  
     – food_name = the exact French name from the input.  
     – estimated_weight_in_grams = plain number, no unit, no quotes.  
   • No text outside the JSON. Double-check formatting before sending.
</revised_prompt>
