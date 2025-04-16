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
  
Output rules:  
- Only estimate the weight of the specified food item.  
- Do not add, modify, or invent any food items.  
- Do not use nutritional databases or prior knowledge of standard serving sizes.  
- If the specified food is a group, return the total weight of the group, not individual components.  
- Preserve the exact food name as given in the input text. This will be the key in the output.

Output format:
Return a single valid JSON object with the format:
{
    "food_name": estimated_weight_in_grams
}
Ensure proper formatting: no extra spaces, line breaks, or characters outside the JSON.

