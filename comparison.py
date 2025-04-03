import pandas as pd
import json
import argparse
import utils

# Command line argument parsing
parser = argparse.ArgumentParser(description="Benchmark food weight predictions.")
parser.add_argument("--sample", type=bool, required=False, default=True, help="Set to False to run the comparison on the whole dataset.")
parser.add_argument("--json", type=str, required=True, help="Path to the JSON predictions file.")
args = parser.parse_args()

# Load the dataset with ground truth labels 
if args.sample:
    csv_file = "./data/weight_data_sample.csv"
else:
    csv_file = "./data/weight_data.csv"

json_file = f"./data/result_data/{args.json}"  

# Load the predictions JSON file
with open(json_file, "r", encoding="utf-8") as f:
    predictions_data = json.load(f)["annotations"]

# Convert the predictions into a DataFrame
predictions_list = []
for key, value in predictions_data.items():
    food_dict = json.loads(value)  # Convert stringified dictionary to actual dictionary
    for food_name, predicted_weight in food_dict.items():
        predictions_list.append({"id": int(key),"food_name": food_name.strip().lower(), "predicted_weight": predicted_weight})

df_predictions = pd.DataFrame(predictions_list)

# Load the ground truth CSV 
df_ground_truth = pd.read_csv(csv_file)

# Keep only relevant columns
df_ground_truth = df_ground_truth[["key", "image_id", "description", "weight"]]
df_ground_truth["description"] = df_ground_truth["description"].str.strip() # Ensure consistency in names

# Merge predictions with ground truth
df_comparison = df_ground_truth.join(df_predictions)
##TODO something to ensure that the columns really are about the same food item !!!! (manually checking it is right but try to do it better)

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
mape = df_comparison["normalized_ae"].sum() / len(df_comparison) *100 ##want this metric but in grams?
df_comparison["weighed_absolute_error"] = df_comparison["absolute_error"] * df_comparison["weight"] / total_weight
weighted_absolute_error = (df_comparison["absolute_error"] * df_comparison["weight"]).sum() / total_weight

print(f"MAE (Mean Absolute Error): {mae:.4f} grams")
print(f"Weighted MAE: {weighted_absolute_error:.4f} grams") ##probably the best
print(f"MAPE (Mean Absolute Percentage Error): {mape:.4f}%\n")

utils.append_to_csv(mae, weighted_absolute_error, mape, json_file) ##TODO: choose filename

# Save results to CSV
# Create a unique filename using the LLM result filename
output_filename = f"./data/comparison_data/comparison_{args.json.split('.')[0]}.csv"
df_comparison["url"] = df_comparison.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1)
df_comparison.to_csv(output_filename, index=False, columns=["key", "image_id", "url", "description", "weight", "predicted_weight", "absolute_error"]) ##add weighed_absolute_error if want to visualize it

sorted_df = df_comparison.sort_values(by="absolute_error", ascending=False)
sorted_df.to_csv(f"./data/comparison_data/sorted_{args.json.split('.')[0]}.csv", index=False, columns=["key", "description", "weight", "predicted_weight", "absolute_error", "weighed_absolute_error", "url"])
print(f"\nComparison results saved to {output_filename}.")