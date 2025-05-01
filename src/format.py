import pandas as pd
import argparse
import time
import re

# Command line argument parsing
parser = argparse.ArgumentParser(description="Formatting files for bechmarking tool.")
parser.add_argument("--sample", action="store_true", help="Use it to indicate that the data needs to be sampled again")
parser.add_argument("--no-sample", dest="sample", action="store_false", help="Use it to indicate that the data only needs to be cleaned")
parser.add_argument("--liquid", action="store_true", help="The data will contain liquids")
parser.add_argument("--no-liquid", dest="liquid", action="store_false", help="Use it to create a file with the whole data without liquids")
parser.add_argument("--testing", action="store_true")
args = parser.parse_args()

input_file = "../data/cleaned/weight_data_cleaned.csv" 
grouped_file = "../data/cleaned/weight_data_cleaned_grouped.csv"
output_file = "../data/ready/weight_data_cleaned_ready.csv" # Formatted for the benchmarking tool
sample_output_file = "no sample output file modified"
if args.sample:
    timestamp = time.strftime("%Y%m%d")
    sample_file = f"../data/cleaned/weight_data_cleaned_sample_{timestamp}.csv"
    sample_output_file = f"../data/ready/weight_data_cleaned_sample_ready_{timestamp}.csv"  # Formatted for the benchmarking tool
if not args.liquid:
    grouped_file = "../data/cleaned/weight_data_cleaned_grouped_no_liquid.csv"
    output_file = "../data/ready/weight_data_cleaned_ready_no_liquid.csv"
    no_liquid_file = "../data/cleaned/weight_data_cleaned_no_liquid.csv" # Whole data without liquids
if args.testing:
    testing = "testing"
    input_file = f"../data/sample_for_testing.csv" 
    grouped_file = f"../data/cleaned/{testing}_cleaned_grouped.csv"
    output_file = f"../data/ready/{testing}_cleaned_ready.csv" # Formatted for the benchmarking tool
    sample_output_file = "no sample output file modified"

# Group all descriptions by image_id
df = pd.read_csv(input_file)
if not args.liquid:
    liquids = ["eau", "thé", "café", "lait", "bière", "vin", "sirop", "jus", "rosé", "espresso", "biere", "cacao", "capuccino", "spritz", "hugo", "jus", "huile de colza"] #to add: "huile", "cappuccino"
    pattern = r'\b(?:' + '|'.join(map(re.escape, liquids)) + r')\b'

    df = df[~df["description"].str.contains(pattern, case=False, na=False, regex=True)]
    df.to_csv(no_liquid_file, index=False)

grouped_descriptions = df.groupby("image_id")["description"].apply(lambda x: ", ".join(x)).reset_index()
grouped_descriptions.rename(columns={"description": "all_food_items"}, inplace=True)

# Merge back to the original DataFrame
df_grouped = pd.merge(df, grouped_descriptions, on="image_id", how="left")

# Save to a new file
df_grouped.to_csv(grouped_file, index=False)

if args.sample:
    # Create the sample file
    random_seed = 30
    sample_df = df_grouped.sample(n=100, random_state=random_seed) # Fixed random sample
    sample_df["description"] = sample_df["description"].str.lower() 
    sample_df.to_csv(sample_file, index=False)

# Create the new CSV with 'id', '00_MSG_00_TEXT', '00_MSG_01_IMAGE' and '00_MSG_02_TEXT'
output_data = {
    'id': range(len(df_grouped)),  
    '00_MSG_00_TEXT': df_grouped['all_food_items'].str.lower(), # Retrieve all the food items present on the picture
    '00_MSG_01_IMAGE': df_grouped.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),  # Generate the URL
    '00_MSG_02_TEXT': df_grouped['description'].str.lower() # Retrieve the description given by the user
}

if args.sample:
    sample_output_data = {
        'id': range(len(sample_df)),  
        '00_MSG_00_TEXT': sample_df['all_food_items'].str.lower(), # Retrieve all the food items present on the picture
        '00_MSG_01_IMAGE': sample_df.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),  # Generate the URL
        '00_MSG_02_TEXT': sample_df['description'].str.lower() # Retrieve the description given by the user
    }

# Create a new DataFrame for the output
output_df = pd.DataFrame(output_data)
if args.sample:
    sample_output_df = pd.DataFrame(sample_output_data)

# Save the output DataFrame to a new CSV
output_df.to_csv(output_file, index=False)
if args.sample:
    sample_output_df.to_csv(sample_output_file, index=False)

print(f"Output saved to {output_file} and {sample_output_file}")