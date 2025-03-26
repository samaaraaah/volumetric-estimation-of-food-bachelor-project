import pandas as pd
import json
import argparse

# Load the dataset with ground truth labels ###TODO MAKE SOMETHING WITH ARGUMENT SO THAT I CAN PICK SAMPLE DATA OR FULL DATA
csv_file = "./data/weight_data_sample.csv" 

# Command line argument parsing
parser = argparse.ArgumentParser(description="Benchmark food weight predictions.")
parser.add_argument("--json", type=str, required=True, help="Path to the JSON predictions file.")
args = parser.parse_args()

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
#print(df_predictions.head(20))

# Load the ground truth CSV 
df_ground_truth = pd.read_csv(csv_file)

# Keep only relevant columns
df_ground_truth = df_ground_truth[["key", "image_id", "description", "weight"]]
df_ground_truth["description"] = df_ground_truth["description"].str.strip() # Ensure consistency in names
#print(df_ground_truth.head(10))

# Merge predictions with ground truth
#df_comparison = df_ground_truth.merge(df_predictions, how="inner", left_on="description", right_on="food_name")
df_comparison = df_ground_truth.join(df_predictions)
##TODO something to ensure that the columns really are about the same food item !!!! (manually checking it is right but try to do it better)
#df_comparison.drop(columns=["id", "food_name"], inplace=True)
#print(df_comparison.head(10))

# Check that the description and food_name are the same for each row
df_comparison["description_match"] = df_comparison["description"] == df_comparison["food_name"]

# Print out any mismatched rows or count them
mismatches = df_comparison[~df_comparison["description_match"]]
if not mismatches.empty:
    print(f"Warning: {len(mismatches)} rows have mismatched description and food_name.")
    print(mismatches[["key", "description", "food_name"]])

# Remove rows where the descriptions do not match and then remove the column 'description_mismatch'
df_comparison = df_comparison[df_comparison["description_match"]]
df_comparison.drop(columns=["description_match"], inplace=True)

# Compute absolute error
df_comparison["absolute_error"] = abs(df_comparison["predicted_weight"] - df_comparison["weight"])
#df_comparison["normalized_ae"] = df_comparison["absolute_error"] / df_comparison["weight"]

# Compute the normalized average misestimation error
#total_weight = df_comparison["weight"].sum()
avg_error = df_comparison["absolute_error"].sum() / len(df_comparison)

print(f"On average, the predictions are off by {avg_error:.4f} grams")

# Save results to CSV
# Create a unique filename using the current timestamp or LLM result filename
output_filename = f"./data/comparison_data/comparison_{args.json.split('.')[0]}.csv"
df_comparison["url"] = df_comparison.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1)
df_comparison.to_csv(output_filename, index=False, columns=["key", "image_id", "url", "description", "weight", "predicted_weight", "absolute_error"])


print(df_comparison.sort_values(by="absolute_error", ascending=False).head(10))
print(f"Comparison results saved to {output_filename}.")