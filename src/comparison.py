import pandas as pd
import json
import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) ##TODO: find a better way to do it
import utils

# Command line argument parsing
parser = argparse.ArgumentParser(description="Benchmark food weight predictions.")
parser.add_argument("--wholedata", action="store_true", required=False, default=False, help="Use it to run the comparison on the whole dataset.")
parser.add_argument("--json", type=str, required=True, help="Path to the JSON predictions file.")
parser.add_argument("--liquid", action="store_true", required=False, help="The data contains liquids.")
parser.add_argument("--no-liquid", dest="liquid", action="store_false", help="Use it to indicate that the data doesn't contain liquids.")
parser.add_argument("--errors", action="store_true", required=False, help="Use it to show top 20 highest errors in terminal.")
parser.add_argument("--liquidsonly", action="store_true", required=False, help="The data contains only liquids.")
args = parser.parse_args()

# Load the dataset with ground truth labels 
if args.liquid:
    if args.wholedata:
        csv_file = "../data/cleaned/weight_data_cleaned.csv"
    else:
        csv_file = "../data/cleaned/weight_data_cleaned_sample.csv"
else:
    if args.wholedata:
        csv_file = "../data/cleaned/weight_data_cleaned_no_liquid.csv" 
    else:
        csv_file = "../data/cleaned/weight_data_cleaned_sample_20250422.csv"
json_file = f"../data/result/{args.json}"  

if args.liquidsonly:
    csv_file = "../data/liquids.csv"
    json_file =  f"../data/result/liquids/{args.json}" 


# Load the predictions JSON file
with open(json_file, "r", encoding="utf-8") as f:
    predictions_data = json.load(f)["annotations"]

# Convert the predictions into a DataFrame
predictions_list = []
for key, value in predictions_data.items():
    food_dict = json.loads(value)  # Convert stringified dictionary to actual dictionary
    reasoning = food_dict.get("reasoning", "")
    
    # Extract the food name and weight (excluding "reasoning")
    for food_name, predicted_weight in food_dict.items():
        if food_name != "reasoning":
            predictions_list.append({
                "id": int(key),
                "food_name": food_name.strip().lower(),
                "predicted_weight": predicted_weight,
                "reasoning": reasoning
            })

df_predictions = pd.DataFrame(predictions_list)

# Load the ground truth CSV 
df_ground_truth = pd.read_csv(csv_file)

# Filter out rows where the description is 'eau'
df_ground_truth = df_ground_truth[df_ground_truth["description"].str.strip().str.lower() != "eau"]

# Keep only relevant columns
df_ground_truth = df_ground_truth[["key", "image_id", "description", "weight"]]
df_ground_truth["description"] = df_ground_truth["description"].str.strip().str.lower() # Ensure consistency in names

# Merge predictions with ground truth
df_comparison = df_ground_truth.join(df_predictions)

# Check that the description and food_name are the same for each row
df_comparison["description_match"] = df_comparison["description"] == df_comparison["food_name"]

# Print out any mismatched rows or count them
mismatches = df_comparison[~df_comparison["description_match"]]
if not mismatches.empty:
    print(f"Warning: {len(mismatches)} rows have mismatched description and food_name.")
    print(mismatches[["key", "description", "food_name"]])
else:
    print("Rows have no mismatch !")

# Remove rows where the descriptions do not match and then remove the column 'description_mismatch'
df_comparison = df_comparison[df_comparison["description_match"]]
df_comparison.drop(columns=["description_match"], inplace=True)

# Compute absolute error
df_comparison["absolute_error"] = abs(df_comparison["predicted_weight"] - df_comparison["weight"])
df_comparison["normalized_ae"] = df_comparison["absolute_error"] / df_comparison["weight"]

# Compute the errors
total_weight = df_comparison["weight"].sum()
mae = df_comparison["absolute_error"].mean()
mape = df_comparison["normalized_ae"].mean() *100 
df_comparison["weighed_absolute_error"] = df_comparison["absolute_error"] * df_comparison["weight"] / total_weight

if args.wholedata:
    df_dish_weights = df_comparison.groupby("image_id")["weight"].sum().reset_index()
    df_dish_weights = df_dish_weights.rename(columns={"weight": "total_dish_weight"})
    df_comparison = df_comparison.merge(df_dish_weights, on="image_id")

    # Per item contibution to dish-level WMAE
    df_comparison["dish_weighted_ae"] = df_comparison["absolute_error"] * df_comparison["weight"] / df_comparison["total_dish_weight"]
    
    # Sum per dish and then average across dishes
    dish_wmae_df = df_comparison.groupby("image_id")["dish_weighted_ae"].sum().reset_index()
    weighted_absolute_error = dish_wmae_df["dish_weighted_ae"].mean()
    dish_wmae_df = dish_wmae_df.rename(columns={"dish_weighted_ae": "total_dish_wmae"})
    df_comparison = df_comparison.merge(dish_wmae_df, on="image_id")
else:
    weighted_absolute_error = (df_comparison["absolute_error"] * df_comparison["weight"]).sum() / total_weight
    
    
print(f"MAE (Mean Absolute Error): {mae:.4f} grams")
print(f"Weighted MAE: {weighted_absolute_error:.4f} grams") ##probably the best
print(f"MAPE (Mean Absolute Percentage Error): {mape:.4f}%\n")

utils.append_to_csv(mae, weighted_absolute_error, mape, json_file) ##TODO: choose filename

# Save results to CSV
# Create a unique filename using the LLM result filename
#output_filename = f"../data/comparison/comparison_{args.json.split('.')[0]}.csv"
df_comparison["url"] = df_comparison.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1)
#df_comparison.to_csv(output_filename, index=False, columns=["key", "image_id", "url", "description", "weight", "predicted_weight", "absolute_error"]) ##add weighed_absolute_error if want to visualize it
sorted_filename = f"../data/comparison/sorted_{args.json.split('.')[0]}.csv"
if args.liquidsonly:
    sorted_filename = f"../data/comparison/liquids/sorted_{args.json.split('.')[0]}.csv"


if args.wholedata:
    sorted_df = df_comparison.sort_values(by="total_dish_wmae", ascending=False)
    sorted_df.to_csv(sorted_filename, index=False, columns=["key", "description", "weight", "predicted_weight", "absolute_error", "total_dish_wmae", "weighed_absolute_error", "url", "reasoning"])
else:
    sorted_df = df_comparison.sort_values(by="absolute_error", ascending=False)
    sorted_df.to_csv(sorted_filename, index=False, columns=["key", "description", "weight", "predicted_weight", "absolute_error", "weighed_absolute_error", "url", "reasoning"])
    
print(f"\nSorted results saved to {sorted_filename}.")

if args.errors:
    # Display the 10 highest absolute errors with wrapped reasoning
    import textwrap

    print("\nTop 20 highest absolute errors with reasoning:\n" + "-"*60)
    top_errors = df_comparison.sort_values(by="absolute_error", ascending=False).head(20)

    for i, row in top_errors.iterrows():
        print(f"\n#{i+1} - Key: {row['key']}")
        print(f"Description: {row['description']}")
        print(f"True weight: {row['weight']} g")
        print(f"Predicted weight: {row['predicted_weight']} g")
        print(f"Absolute error: {row['absolute_error']} g")
        print(f"URL: {row['url']}")
        print("Reasoning:")
        wrapped_reasoning = textwrap.fill(str(row['reasoning']), width=100)
        print(wrapped_reasoning)
        print("-" * 60)