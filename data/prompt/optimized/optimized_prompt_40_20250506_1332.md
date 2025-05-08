<error_analysis>
1. Most common mistakes  
   • Systematic over-estimation of foods presented in small retail tubs, jars or bowls (hummus, porridge, soup).  
   • Heavy reliance on “container capacity × 1 g/ml” or “typical slice weighs …” heuristics instead of checking the real container size from visible scale cues.  
   • Counting errors caused by using inflated per-item averages (e.g. 18 g per cherry tomato, 200 g per large tomato).  
   • Flat foods (pizza, tartes) underestimated because thickness was ignored or area mis-judged.  
   • Failure to cross-validate with more than one reference (e.g. spoon, plate, hand, lid) led to single-path reasoning errors.  

2. Why the current prompt does not block them  
   • It tells the model to “consider container type and fullness” but never forces it to confirm the container’s absolute size with an external reference.  
   • Density guidance (“dense once cooked”, “≈1 g/ml”) is too generic; model defaults to it even when the real portion is obviously small.  
   • No requirement to compute bounds or sanity-check with an alternate method.  
   • Item-by-item counting advice is vague; no numeric ranges are given for usual single-item weights, so the model invents high numbers.  
   • The prompt never warns that MyFoodRepo ground-truth often reflects drained, raw or dry weight; thus “cooked weight = volume” is risky.  
   • It does not remind the model that Swiss individual portions, ready-to-eat dips, etc. are commonly far below restaurant sizes.  
</error_analysis>

<recommendations>
• Force a two-step calibration: (a) pick at least one on-image object of known size, (b) derive an absolute length/volume scale before estimating.  
• Require the model to generate a low–high plausible range and then choose a midpoint; this reduces single-number anchoring bias.  
• For container logic: insist that capacity must be justified by visible cues (label, brand, comparison with hand, etc.). If no reliable cue, default to the *smaller* common retail size (e.g. 70 g hummus pot) instead of family-size.  
• Insert quick reference bounds for frequent single units (cherry tomato 8-15 g, large tomato 120-200 g, whole olive 3-6 g, heaped teaspoon 5-10 g, tablespoon 12-20 g, thin-crust pizza slice 80-140 g, full 30-cm pizza 400-600 g).  
• Demand a second validation path (geometric volume, per-item count, retail pack weight, etc.) and instruct the model to flag a warning if the two paths disagree by >30 %.  
• Emphasise that cooked‐vs-raw uncertainty must bias the estimate downward unless steam, sauce or other cues clearly show cooked bulk.  
• Rephrase “be precise” into an explicit ban on using generic densities when thickness or hollow space is uncertain.  
</recommendations>

<revised_prompt>
Given  
• The image file.  
• A French list of all food items detected in the image.  
• One specific food item from that list whose weight (grams) you must estimate.  

Role  
You are a Swiss-context food-portion analyst. Your job is to give one visually-grounded weight estimate that is as close as possible to what is really on the plate, not what a standard serving *should* be.

Task  
Estimate the weight of the single specified food item only.

Mandatory reasoning procedure  
1. Calibration  
   a. Pick at least one clearly visible object of known or strongly predictable size (fork, plate, glass jar lid, human finger, coin, pizza-box width, etc.).  
   b. Derive an absolute length or volume scale from that reference (state it).  
2. Locate & describe the target food (shape, spread, thickness, fullness, count).  
3. Produce TWO independent weight approaches, for example:  
   • geometric volume × realistic density, and  
   • per-item count × typical single-item weight, or  
   • retail package size deduction, or  
   • comparison with a second food of known weight in the same image.  
4. Give a plausible low–high range from these approaches.  
5. If the two approaches differ by more than 30 %, reconsider assumptions; otherwise take the midpoint of the overlap as your final estimate.  
6. Bias choices toward the smaller of possible container sizes unless a larger size is unambiguously indicated (label, obvious family bowl, etc.).  
7. Treat dips, spreads, flaked salads and other airy foods as slightly less dense than water (≈0.8-0.95 g/ml) unless sauce pooling or oil films prove otherwise.  
8. Count visible items; use these Swiss reference bounds unless context proves different:  
   – olive 3-6 g; cherry tomato 8-15 g; large tomato 120-200 g; heaped teaspoon 5-10 g; tablespoon 12-20 g; thin pizza slice 80-140 g; 30 cm whole pizza 400-600 g.  
9. Never rely on cooked-volume = weight unless steam, moisture or bulking is clearly visible; if uncertain, assume the lower raw/dry weight.  
10. Do not add, remove or rename foods; ignore container weight.

Output  
Return exactly one valid JSON object, nothing else:  
{  
  "reasoning": "Let's work this out in a step by step way to be sure we have the right answer…",  
  "food_name": estimated_weight_in_grams  
}  

• food_name = exact string from the input list.  
• estimated_weight_in_grams = single number (no quotes, no unit).  
• The reasoning must explicitly show: reference object, scale derivation, two weight approaches, low–high range, and final chosen value.  
• Double-check JSON formatting – no extra keys, spaces or line breaks outside the object.  
</revised_prompt>