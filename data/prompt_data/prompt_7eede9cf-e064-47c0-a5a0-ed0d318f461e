For each food item mentioned in the input text, estimate its weight in grams based on the provided image. You must be precise.\ 
Instructions: \
Only include food items from the input text. Do not add, modify, or invent additional food items.\
The food items mentioned are present in the image, but sometimes they may be mixed with other items or not fully visible. Estimate their weight as accurately as possible using the visual information available.\
Use surrounding objects as references for approximating portion sizes.\
If the input text specifies a single food item, estimate the weight of that item alone, even if other ingredients or components are visible in the image. Do not include their weight.\
If a group of food items is mentioned (example: concombre et vinaigrette) estimate the total weight of the entire group, not the weight of individual components.\
Keep the exact same food name as the input text, even if it refers to a group.\
Format the response as a valid JSON object, where the food name is the key and the estimated weight in grams is the value.\
Ensure the output is properly formatted without unnecessary new lines or special characters.\
Examples: \ 
Image input: https://www.myfoodrepo.org/api/v1/subjects/8japfq/dish_media/2a854c3d-0ba9-4c3f-b22c-630cbe2d37cd \
Text input: "fraises"\
Expected output: { "fraises": 167 } \ 
Image input: https://www.myfoodrepo.org/api/v1/subjects/wrah5h/dish_media/19a2e7b0-7aad-44c5-b52a-d67294d4ef49 \
Text input: "galette wraps"\
Expected output: {“galette wraps”: 65}
