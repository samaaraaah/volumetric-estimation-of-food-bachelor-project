import os
from dotenv import load_dotenv
import openai
import argparse 
import csv

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
    errors = [row for row in reader]

# Keep only the first 20 error cases
errors = errors[:20]

# Step 3: Create optimization instruction
instruction = f"""
You are an expert in prompt optimization systems. Your task is to improve the effectiveness of prompt optimization prompts - the prompts used to guide the improvement of task-specific prompts.

Below is the current prompt used for food weight estimation. Then, you will find several real-world error examples from a system using this prompt.

Your goal: Optimize the prompt to reduce the types of errors shown. Keep the structure similar, but improve reasoning guidance, especially for:
- Chopped food (e.g., tomatoes misestimated when chopped)
- Overestimation of low-density food in jars or bowls (e.g., porridge, hummus)
- Misjudgment of spread-out but dense foods (e.g., gratins, salads)
- Partial foods mixed with others
- Misuse of volume assumptions
- Use of reference items

## Current Prompt:
{current_prompt}

## Output Format:
<effectiveness_analysis>
Analysis of how well this optimization prompt guides improvements
</effectiveness_analysis>

<improvement_strategy>
Specific changes to enhance optimization capabilities
</improvement_strategy>

<improved_optimization_prompt>
The enhanced prompt for optimizing task-specific prompts
</improved_optimization_prompt>


## Examples of high-error outputs:
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
"""

instruction += "\n## Please provide a refined prompt that addresses these common failures while keeping the structure clear and robust."

# Step 4: Send request to GPT-o3
response = client.chat.completions.create(
    model="o3",
    messages=[
        {"role": "system", "content": "You are an expert in prompt optimization for machine learning and computer vision tasks."},
        {"role": "user", "content": instruction}
    ],
    temperature=1
)

# Step 5: Save the optimized prompt
optimized_prompt = response.choices[0].message.content
print(optimized_prompt)

# Step 6: Save output to file
output_path = f"../data/prompt/optimized/optimized_{args.prompt.replace('.md', '')}.md"
with open(output_path, "w", encoding="utf-8") as out_file:
    out_file.write(optimized_prompt)

print(f"Optimized prompt saved to: {output_path}")

