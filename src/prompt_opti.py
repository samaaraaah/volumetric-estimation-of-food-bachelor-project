import os
from datetime import datetime
from dotenv import load_dotenv
import openai
import argparse 
import csv
import re

# Argument parsing
parser = argparse.ArgumentParser(description="Prompt optimizer.")
parser.add_argument("--prompt", type=str, required=True, help="Name of the prompt file.")
parser.add_argument("--errors", type=str, required=True, help="Name of the error file.")
args = parser.parse_args()
#prompt_40_fulldata_d19c3270-5f4c-4cfb-9e21-8d7e14ece178.md

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Read the current prompt
with open(f"../data/prompt/{args.prompt}", "r", encoding="utf-8") as f:
    current_prompt = f.read()

# Step 2: Read error cases from CSV
with open(f"../data/comparison/{args.errors}", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    results = [row for row in reader]

# Keep only the first 20 error cases
errors = results[:20]

# Keep 20 best estimations
best = results[-20:]

# Step 3: Create optimization instruction
instruction = f"""
You are an expert in improving prompts for AI systems. Your task is to help optimize the following prompt used for food weight estimation.

Below is the current prompt followed by several examples where the model made significant errors and other where it performed well.

Your goal: Refine the prompt to reduce recurring failure modes, using both good and bad examples as guidance. The current prompt already performs well—make small, targeted improvements only where needed, and preserve the structure, logic, and reasoning flow as much as possible. 

Use the error cases to identify failure modes, and the good examples to understand what works well.

Important: The <revised_prompt> must be presented as a clean, final version—do not highlight or annotate changes inside it (e.g., using bold, comments, or explanations). All change explanations should go in the <recommendations> section only.

## Requirements to keep in the revised prompt:
- Assume all images were taken in Switzerland; leverage common Swiss portion sizes where relevant.
- Emphasize visual grounding: prioritise cues like texture, shape, shadow, and relative size over rigid calculations (e.g., plate diameter × height).
- Preserve the final instruction to return a JSON with:
  {{
    "reasoning": "Let’s work this out in a step by step way to be sure we have the right answer…",
    "food_name": estimated_weight_in_grams
  }}
– Replace food_name with exactly the specified food name from the input (no translation).  
– Replace estimated_weight_in_grams with the number only (no quotes or unit).
- Do not output any text outside of the JSON block.
- Preserve the existing structure of steps and instructions in the current prompt. Do not add new sections unless they directly address recurring failure modes.

## Current Prompt:
{current_prompt}

## Your Response Format:
<error_analysis>
1. Identify the most common types of mistakes
2. Explain why the current prompt fails to prevent them
</error_analysis>

<recommendations>
Clear suggestions to improve the prompt
</recommendations>

<revised_prompt>
Your improved version of the original prompt
</revised_prompt>

## High-error examples:
"""

for e in errors:
    instruction += f"""
----
Key: {e["key"]}
Description: {e["description"]}
True weight: {e["weight"]}g
Predicted weight: {e["predicted_weight"]}g
Error: {e["absolute_error"]}g
Reasoning: {e["reasoning"]}
Image: {e["url"]}

## Good performance examples:
"""
    
for b in best:
    instruction += f"""
----
Key: {b["key"]}
Description: {b["description"]}
True weight: {b["weight"]}g
Predicted weight: {b["predicted_weight"]}g
Error: {b["absolute_error"]}g
Reasoning: {b["reasoning"]}
Image: {b["url"]}
"""

instruction += """\n## Please suggest a stronger prompt that addresses the patterns of failure shown above. 
Important: The <revised_prompt> must be presented as a clean, final version—do not highlight or annotate changes inside it (e.g., using bold, comments, or explanations). 
All change explanations should go in the <recommendations> section only. """



# Step 4: Send request to GPT-o3
response = client.chat.completions.create(
    model="o3",
    messages=[
        {"role": "system", "content": "You are an expert in prompt optimization, with a focus on visual reasoning and volume/weight estimation tasks."},
        {"role": "user", "content": instruction}
    ],
    temperature=1
)

# Step 5: Save the optimized prompt
optimized_prompt = response.choices[0].message.content
print(optimized_prompt)

# Step 6: Save output to file
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
base = args.prompt.replace(".md", "")        # Remove extension
parts = base.split("_")                   # Split by underscore

# parts[1] is the number, parts[2] is the ID (we want only parts[1])
prompt_number = parts[0] + "_" + parts[1]
output_path = f"../data/prompt/optimized/optimized_{prompt_number}_{timestamp}.md"
with open(output_path, "w", encoding="utf-8") as out_file:
    out_file.write(optimized_prompt)

print(f"Optimized prompt saved to: {output_path}")

# Step 7: Extract and save only the revised prompt
match = re.search(r"<revised_prompt>\s*(.*?)\s*</revised_prompt>", optimized_prompt, re.DOTALL)
if match:
    revised_prompt = match.group(1).strip()
    # Compute the incremented prompt number (e.g., from "prompt_40" to "prompt_41")
    prefix, num = prompt_number.split("_")
    incremented_num = int(num) + 1
    new_prompt_filename = f"../data/prompt/prompt_{incremented_num}_.md"
    with open(new_prompt_filename, "w", encoding="utf-8") as out_file:
        out_file.write(revised_prompt)
    print(f"Revised prompt saved to: {new_prompt_filename}")
else:
    print("Failed to extract <revised_prompt> block.")
