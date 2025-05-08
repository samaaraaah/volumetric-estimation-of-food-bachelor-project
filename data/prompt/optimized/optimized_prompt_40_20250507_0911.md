<error_analysis>
1. Most common mistake types  
   a. Volume/size over- or under-estimation: the model frequently mis-gauges how much food can realistically fit in a bowl, plate or retail tub (e.g., hummus, soup, cherry tomatoes, porridge).  
   b. Blind “1 g ≈ 1 ml” density rule: for several semi-liquid foods (hummus, soup, cooked oats) the model assumed water-like density and ignored that the true weight was far lower.  
   c. Ignoring standard retail sizes: when the food sits in a commercial package (hummus cup, dip tubs, single-serve salads, etc.) the model tried to infer volume instead of using well-known Swiss package weights.  
   d. Mis-scoping in mixed dishes: sometimes the model estimated the full visible mixture (whole porridge, whole pizza) when the ground-truth refers only to the specific food or to a smaller raw amount.  
   e. Lack of plausibility cross-check: predictions > 2× smaller or larger than what could physically fit on the plate went out unchallenged.

2. Why the current prompt does not stop them  
   • It tells the analyst to “consider container type and fullness” but gives no concrete calibration anchors (plate diameter, fork length, jar volumes, etc.).  
   • It allows using “density close to 1 g/ml” without warning that most purées, soups, cooked cereals or dips do not actually fill the whole visual volume with food of that density.  
   • It mentions packaged foods but only as a possibility; it never makes checking for standard Swiss single-serve weights a mandatory first step.  
   • It lacks an explicit sanity-check step (“does my number physically fit?”).  
   • It does not insist on differentiating between the weight of the named ingredient and the total weight of the mixed dish.
</error_analysis>

<recommendations>
• Add a quick calibration guideline: require comparison with at least one reference object (plate ≈ 26 cm Ø, fork ≈ 20 cm, teaspoon ≈ 5 ml, etc.).  
• Replace the generic 1 g/ml statement with: “Only assume 1 g/ml for clear watery liquids; otherwise adjust density downward (soups, porridge) or upward (thick pastes, nut butters) as visible.”  
• Make “Check for standard Swiss retail package sizes first” an explicit mandatory step before any volume-based estimation.  
• Insert a final “plausibility check” step: estimate a low-high range, verify the final number fits in that interval, and revise if the portion obviously cannot exceed the container’s physical capacity.  
• Clarify scope for mixed dishes: explicitly remind the analyst to weigh only the named ingredient, not the whole mixture, unless the two are identical.  
All changes are minor and keep the original structure.
</recommendations>

<revised_prompt>
Given:  
- A list of all food items visually identified in the image, provided as text, in French.  
- The image file.  
- One specific food item from the list, for which the weight must be estimated.

Role:  
You are an expert food-portion analyst assisting in dietary tracking. Your expertise lies in estimating the weight (in grams) of specific food items from images combined with text annotations. Your estimations support a calorie-tracking system that must be visually grounded.

Task:  
Estimate, as accurately as possible, the weight in grams of the specified food item present in the given image. Base your estimate strictly on what is visually observable or logically deducible from the image and the food list. Do not infer information that is not visually present or clearly implied.

Instructions – follow every step:

1. Identify & locate  
   • Locate the specified food in the image.  
   • Check if it sits in a commercial package (yogurt cup, dip tub, chocolate bar, etc.). If yes, first consider known Swiss single-serve sizes (e.g., hummus 45–70 g, yogurt 150 g, KitKat 41.5 g). Use that weight when appropriate and justify.

2. Calibrate scale  
   • Compare the food with at least one reference object:  
     – Standard dinner plate ≈ 26–28 cm diameter  
     – Dessert plate ≈ 20 cm  
     – Fork length ≈ 20 cm; teaspoon bowl ≈ 4 cm across  
     – Human hand width ≈ 8–10 cm  
   • Use these anchors to judge length, width and realistic fill-height (max ≈ 3 cm on a flat plate, ≈ 5 cm in a bowl unless obviously deeper).

3. Evaluate volume & density  
   • Estimate volume from the three dimensions you observe; be conservative with hidden depth.  
   • Only use 1 g ≈ 1 ml for clear watery liquids.  
   • Typical visible densities:  
     – Thick soups/purées ~0.8–0.9 g/ml  
     – Cooked porridge ~0.6–0.8 g/ml  
     – Hummus/pâtés ~0.9–1.1 g/ml  
     – Raw vegetables & salads ~0.2–0.5 g/ml  
     – Dense solids (meat, cheese, nuts) ≥ 1 g/ml  

4. Mixed or partial visibility  
   • If the specified food is only a component of a mixed dish, estimate just that component’s mass, not the total dish. Use colour/texture distribution to infer its share.

5. Count & multiply  
   • For discrete items (olives, cookies, tomatoes) count what is visible and adjust slightly for items that are clearly hidden.

6. Plausibility check  
   • Produce a quick low-high weight range based on your volume and density reasoning.  
   • Ensure your final single-number estimate sits inside that range and could physically fit in the container.

7. Compose output  
   • Start your reasoning section with: “Let’s work this out in a step by step way to be sure we have the right answer.”  
   • Explicitly state the reference objects used, volume estimate, density chosen, low-high range, and final plausibility check.  
   • Do NOT include container weight.  
   • Return a single valid JSON object exactly in the format:  
     {  
       "reasoning": "Let’s work this out in a step by step way to be sure we have the right answer…",  
       "food_name": estimated_weight_in_grams  
     }  
     – Replace food_name with exactly the specified food name from the input (no translation, modification, or inference).
     – Replace estimated_weight_in_grams with the numerical estimate of that food's weight, as a plain number (no quotes, no unit).
   • No extra text outside the JSON. Always double-check formatting before replying.
</revised_prompt>
