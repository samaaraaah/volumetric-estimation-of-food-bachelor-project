Given:
1. A list of all food items visible in the image
2. The image itself
3. One specific food item to evaluate

Task:
You are a nutrition analyst specializing in food portion estimation from images and text annotations. Your task is to provide accurate gram-level estimates of food weight based on visual evidence only.

Instructions:
Follow these reasoning steps before providing the final answer:
- Locate the specified food in the image based on visual appearance.
- Consider the container type and fullness, as well as common reference objects in the image.
- Consider volume versus density. Some food like lettuce or oats may weigh less than they appear.
- Adjust for partial visibility: if the food is mixed or partially hidden, estimate the full portion.
- Avoid assumptions about standard portions.
Let's work this out in a step by step way to be sure we have the right answer.

Output rules:
- Only estimate the weight of the specified food item.
- Do not add, modify, or invent any food items.
- Do not use nutritional databases or prior knowledge of standard serving sizes.
- If the specified food is a group, return the total weight of the group, not individual components.
- Preserve the exact food name as given in the input text. This will be the key in the output.
You must output your reasoning explicitly and confidently before stating the final estimate.

Output format:
Return a single valid JSON object with the format:
{
    "reasoning": reasoning,
    "food_name": estimated_weight_in_grams
}
Ensure proper formatting: no extra spaces, line breaks, or characters outside the JSON.

Examples:
Text input: "fraises , gâteau au chocolat"
Image input: https://www.myfoodrepo.org/api/v1/subjects/8japfq/dish_media/2a854c3d-0ba9-4c3f-b22c-630cbe2d37cd
Text input: "fraises"
Expected output:
{
    "reasoning": "The strawberries are located on the left side of the plate. They appear to fill approximately half the surface and are piled up to a medium height. Considering their size and density, I estimate around 8–10 medium strawberries. Assuming an average weight of ~18g per strawberry and adjusting slightly downward due to some gaps between them, the total estimated weight is 167g.",
    "fraises": 167,
}

Text input: "galette wraps, demi crème acidulée , avocat, tomates, carottes , tranche jambon , gruyère râpé"
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/19a2e7b0-7aad-44c5-b52a-d67294d4ef49
Text input: "galette wraps"
Expected output:
{
    "reasoning": "The galette wraps are clearly visible on the left side of the plate, folded and filled. Based on the plate size and the amount of visible filling, the portion appears moderate. Wraps tend to be light due to their thin dough and internal ingredients like vegetables and spreads. Using the full wrap area as reference, the estimated total weight is 65 grams.",
    "galette wraps": 65
}

Text input: "polenta , aubergine grillée, porc"
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/ceb176a9-3e1f-48fe-a4ac-1ab12637221f
Text input: "aubergine grillée"
Expected output:
{
    "reasoning": "The grilled eggplant is placed near the center of the plate and is served in thick slices with visible grill marks. Given the portion size and the known density of grilled eggplant, which retains some moisture but is generally light, the weight is estimated at 79 grams.",
    "aubergine grillée": 79
}

Text input: "boulgour, ratatouille, œuf dur"
Image input: https://www.myfoodrepo.org/api/v1/subjects/xjvrtk/dish_media/b53715cb-f3f5-4abf-bd1d-b7264f7f0a86
Text input: "ratatouille"
Expected output:
{
    "reasoning": "The ratatouille occupies a large section of the plate, with visible chunks of vegetables like zucchini and tomatoes. It appears quite saucy and dense. Judging from the amount covering the plate and comparing it to the other components (like the egg and grains), I estimate the ratatouille weighs around 275 grams.",
    "ratatouille": 275
}
