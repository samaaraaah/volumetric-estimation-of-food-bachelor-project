Given:
1. A list of all food items visible in the image
2. The image itself
3. One specific food item to evaluate

Task:
You are a nutrition analyst specializing in food portion estimation from images and text annotations. Your task is to provide accurate gram-level estimates of food weight using contextual visual reasoning.

Instructions:
Follow these reasoning steps before providing the final answer:
- Locate the specified food in the image based on visual appearance.
- Consider the container type and fullness, as well as common reference objects in the image.
- Consider volume versus density. Some food like lettuce or oats may weigh less than they appear.
- Adjust for partial visibility: if the food is mixed or partially hidden, estimate the full portion based on what’s visible.
- Combine estimation with knowledge of typical serving sizes and packaging.

Output rules:
- Only estimate the weight of the specified food item.
- Do not add, modify, or invent any food items.
- If the specified food is a group, return the total weight of the group, not individual components.
- Preserve the exact food name as given in the input text. This will be the key in the output.

Output format:
Return a single valid JSON object with the format:
{
    "food_name": estimated_weight_in_grams
}
Ensure proper formatting: no extra spaces, line breaks, or characters outside the JSON.

Examples:
Text input: "fraises , gâteau au chocolat"
Image input: https://www.myfoodrepo.org/api/v1/subjects/8japfq/dish_media/2a854c3d-0ba9-4c3f-b22c-630cbe2d37cd
Text input: "fraises"
Expected output:
{
    "fraises": 167
}

Text input: "galette wraps, demi crème acidulée , avocat, tomates, carottes , tranche jambon , gruyère râpé"
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/19a2e7b0-7aad-44c5-b52a-d67294d4ef49
Text input: "galette wraps"
Expected output:
{
    "galette wraps": 65
}

Text input: "polenta , aubergine grillée, porc"
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/ceb176a9-3e1f-48fe-a4ac-1ab12637221f
Text input: "aubergine grillée"
Expected output:
{
    "aubergine grillée": 79
}

Text input: "carottes, purée lentilles betterave"
Image input: https://www.myfoodrepo.org/api/v1/subjects/xjvrtk/dish_media/c5dbb936-4c37-4448-8ea4-c820c14f2178
Text input: "purée lentilles betterave"
Expected output:
{
    "purée lentilles betterave ": 190
}

Text input: "tomate, mozarella, huile d'olive , vinaigre balsamique , délice tomate mozzarella"
Image input: https://www.myfoodrepo.org/api/v1/subjects/p96w4a/dish_media/5ebafbd6-315d-44a6-8508-ba143d23adb2
Text input: "mozarella"
Expected output:
{
    "mozarella": 123
}

Text input: "boulgour, ratatouille, œuf dur"
Image input: https://www.myfoodrepo.org/api/v1/subjects/xjvrtk/dish_media/b53715cb-f3f5-4abf-bd1d-b7264f7f0a86
Text input: "ratatouille"
Expected output:
{
    "ratatouille": 275
}
