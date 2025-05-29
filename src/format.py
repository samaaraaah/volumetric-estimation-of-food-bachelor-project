import pandas as pd
import argparse
import time
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Formatting files for benchmarking tool.")
    parser.add_argument("--sample", action="store_true", help="Sample the data again")
    parser.add_argument("--no-sample", dest="sample", action="store_false", help="Only clean the data")
    parser.add_argument("--liquid", action="store_true", help="Keep liquids in the dataset")
    parser.add_argument("--no-liquid", dest="liquid", action="store_false", help="Remove liquids from the dataset")
    parser.add_argument("--size", type=int, default=100, help="Sample size (default: 100)")
    return parser.parse_args()


def remove_liquids(df):
    # List of liquid-related food terms to filter out
    liquids = [
        "eau", "thé", "café", "lait", "bière", "vin", "sirop", "jus", "rosé",
        "espresso", "biere", "cacao", "capuccino", "spritz", "hugo",
        "huile de colza", "huile", "cappuccino", "vinaigrette"
    ] # Liquids to add for next formatting: "cidre", "tonic au gingembre"

    # Build a regex pattern that matches any of the liquid terms
    pattern = r'\b(?:' + '|'.join(map(re.escape, liquids)) + r')\b'

    # Remove rows where the description contains any of the listed liquids
    return df[~df["description"].str.contains(pattern, case=False, na=False, regex=True)]


def group_descriptions(df):
    # Group descriptions by image_id and concatenate them into a single string
    grouped = df.groupby("image_id")["description"].apply(lambda x: ", ".join(x)).reset_index()
    grouped.rename(columns={"description": "all_food_items"}, inplace=True)
    
    # Merge back the grouped descriptions with the original dataframe
    return pd.merge(df, grouped, on="image_id", how="left")


def create_output_df(df):
    # Format the dataframe for the benchmarking tool 
    return pd.DataFrame({
        'id': range(len(df)),
        '00_MSG_00_TEXT': df['all_food_items'].str.lower(),
        '00_MSG_01_IMAGE': df.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),
        '00_MSG_02_TEXT': df['description'].str.lower()
    })


def main():
    args = parse_args()

    input_file = "../data/cleaned/weight_data_cleaned.csv"
    grouped_file = "../data/cleaned/weight_data_cleaned_grouped.csv"
    output_file = "../data/ready/weight_data_cleaned_ready.csv"

    df = pd.read_csv(input_file)

    if not args.liquid:
        df = remove_liquids(df)
        df.to_csv("../data/cleaned/weight_data_cleaned_no_liquid.csv", index=False)
        grouped_file = "../data/cleaned/weight_data_cleaned_grouped_no_liquid.csv"
        output_file = "../data/ready/weight_data_cleaned_ready_no_liquid.csv"

    df_grouped = group_descriptions(df)
    df_grouped.to_csv(grouped_file, index=False)

    if args.sample:
        timestamp = time.strftime("%Y%m%d")
        sample_file = f"../data/cleaned/weight_data_cleaned_sample_{timestamp}.csv"
        sample_output_file = f"../data/ready/weight_data_cleaned_sample_ready_{timestamp}.csv"
        sample_df = df_grouped.sample(n=args.size, random_state=30)
        sample_df["description"] = sample_df["description"].str.lower()
        sample_df.to_csv(sample_file, index=False)
        sample_output_df = create_output_df(sample_df)
        sample_output_df.to_csv(sample_output_file, index=False)

    output_df = create_output_df(df_grouped)
    output_df.to_csv(output_file, index=False)

    print(f"Output saved to {output_file}")
    if args.sample:
        print(f"Sample output saved to {sample_output_file}")


if __name__ == "__main__":
    main()
