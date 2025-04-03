For each food item mentioned in the input text, estimate its weight in grams based on the provided image. You must be precise.\ 
Instructions: \
Only include food items from the input text. Do not add, modify, or invent additional food items.\
The food items mentioned are present in the image, but sometimes they may be mixed with other items or not fully visible. I insist that you must estimate their weight, as accurately as possible, based on the visual information from the image.\
If the input text mentions only one food item estimate the weight of just that item, even if other ingredients or food items are visible in the image. Do not include the weight of other visible components.\
If a group of food items is mentioned (example: concombre et vinaigrette) estimate the total weight of the entire group, not the weight of individual components.\
Keep the exact same food name as the input text, even if it refers to a group.\
Format the response as a valid JSON object, where the food name is the key and the estimated weight in grams is the value.\
Ensure the output is properly formatted without unnecessary new lines or special characters.\
Examples: \ 
Image input: https://www.myfoodrepo.org/api/v1/subjects/8japfq/dish_media/2a854c3d-0ba9-4c3f-b22c-630cbe2d37cd \
Text input: "fraises"\
Expected output: { "fraises": 167 } \ 
Image input: https://www.myfoodrepo.org/api/v1/subjects/m4egh2/dish_media/1f732396-f9f9-451f-bb51-ade259131e78   \
Text input: "beurre"\
Expected output: {"beurre": 4 }\
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/19a2e7b0-7aad-44c5-b52a-d67294d4ef49 \
Text input: "galette wraps"\
Expected output: {“galette wraps”: 65}
