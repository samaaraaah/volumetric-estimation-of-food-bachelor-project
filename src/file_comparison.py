import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Comparison script between 2 files.")
parser.add_argument("--file1", type=str, required=False, default=False, help="File name 1.")
parser.add_argument("--file2", type=str, required=True, help="File name 2.")
args = parser.parse_args()
file1 = pd.read_csv(f"../data/comparison/sorted_{args.file1}.csv")
file2 = pd.read_csv(f"../data/comparison/sorted_{args.file2}.csv")
output_path = f"./comparisonfile.csv"

# Merge on both 'description' and 'weight' to handle duplicates properly
merged = pd.merge(
    file1,
    file2,
    on=["description", "weight"],
    suffixes=("_file1", "_file2"),
    how="inner"  # 'inner' ensures only matching rows are kept
)

# Determine which file had the smaller absolute error
def best_file(row):
    if row["absolute_error_file1"] < row["absolute_error_file2"]:
        return "file1"
    elif row["absolute_error_file2"] < row["absolute_error_file1"]:
        return "file2"
    else:
        return "tie"

# Apply the logic to get the best result
merged["best"] = merged.apply(best_file, axis=1)

# Select only the needed columns
output = merged[[
    "description",
    "weight",
    "predicted_weight_file1",
    "predicted_weight_file2",
    "best",
    "url_file1"
]]

output = output.sort_values(by="best", ascending=True)

# Save to new CSV
output.to_csv(output_path, index=False)

print(f"Output saved to {output_path}")