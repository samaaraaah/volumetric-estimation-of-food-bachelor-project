import pandas as pd
import json
import argparse
import textwrap


def parse_arguments():
    parser = argparse.ArgumentParser(description="Benchmark food weight predictions.")
    parser.add_argument("--wholedata", action="store_true", default=False, help="Run comparison on the whole dataset.")
    parser.add_argument("--json", type=str, required=True, help="Path to the JSON predictions file.")
    parser.add_argument("--liquid", action="store_true", help="The data contains liquids.")
    parser.add_argument("--no-liquid", dest="liquid", action="store_false", help="The data does not contain liquids.")
    parser.add_argument("--errors", action="store_true", help="Display top 20 highest errors.")
    parser.add_argument("--best", action="store_true", help="Display top 20 lowest errors.")
    return parser.parse_args()

def load_data(args):
    # Load data from CSV and JSON files based on arguments
    if args.liquid:
        csv_file = "../data/cleaned/weight_data_cleaned.csv" if args.wholedata else "../data/cleaned/weight_data_cleaned_sample.csv"
    else:
        csv_file = "../data/cleaned/weight_data_cleaned_no_liquid.csv" if args.wholedata else "../data/cleaned/weight_data_cleaned_sample_20250520.csv"
    json_file = f"../data/result/{args.json}"

    with open(json_file, "r", encoding="utf-8") as f:
        predictions_data = json.load(f)["annotations"]

    return csv_file, json_file, predictions_data

def prepare_predictions(predictions_data):
    # Convert JSON predictions into a DataFrame
    predictions_list = []
    for key, value in predictions_data.items():
        food_dict = json.loads(value)
        reasoning = food_dict.get("reasoning", "")
        for food_name, predicted_weight in food_dict.items():
            if food_name != "reasoning":
                predictions_list.append({
                    "id": int(key),
                    "food_name": food_name.strip().lower(),
                    "predicted_weight": predicted_weight,
                    "reasoning": reasoning
                })
    return pd.DataFrame(predictions_list)

def compute_errors(df_comparison, args):
    df_comparison["absolute_error"] = abs(df_comparison["predicted_weight"] - df_comparison["weight"])
    df_comparison["normalized_ae"] = df_comparison["absolute_error"] / df_comparison["weight"]

    total_weight = df_comparison["weight"].sum()
    mae = df_comparison["absolute_error"].mean()
    mape = df_comparison["normalized_ae"].mean() * 100

    df_comparison["weighed_absolute_error"] = df_comparison["absolute_error"] * df_comparison["weight"] / total_weight

    if args.wholedata:
        # Compute weighted errors per dish
        df_dish_weights = df_comparison.groupby("image_id")["weight"].sum().reset_index()
        df_dish_weights = df_dish_weights.rename(columns={"weight": "total_dish_weight"})
        df_comparison = df_comparison.merge(df_dish_weights, on="image_id")
        df_comparison["dish_weighted_ae"] = df_comparison["absolute_error"] * df_comparison["weight"] / df_comparison["total_dish_weight"]

        dish_wmae_df = df_comparison.groupby("image_id")["dish_weighted_ae"].sum().reset_index()
        weighted_absolute_error = dish_wmae_df["dish_weighted_ae"].mean()
        dish_wmae_df = dish_wmae_df.rename(columns={"dish_weighted_ae": "total_dish_wmae"})
        df_comparison = df_comparison.merge(dish_wmae_df, on="image_id")
    else:
        weighted_absolute_error = (df_comparison["absolute_error"] * df_comparison["weight"]).sum() / total_weight

    return df_comparison, mae, weighted_absolute_error, mape

def append_to_csv(mae, weighted_mae, mape, result_file_name, output_file_name):
    # Store the result for the current file
    metrics = {
        "result_file": result_file_name,  # Name of the file processed
        "MAE": mae,
        "MAPE": mape,
        "Weighted_MAE": weighted_mae
    }
    # Create a DataFrame from the metrics
    df_metrics = pd.DataFrame([metrics], columns=["result_file", "MAE", "MAPE", "Weighted_MAE"])

    # If the file exists, append the data, otherwise create it with header
    try:
        # Append the results to the file
        df_metrics.to_csv(output_file_name, mode='a', header=False, index=False)
    except FileNotFoundError:
        # If the file does not exist, create it and add the header
        df_metrics.to_csv(output_file_name, mode='w', header=True, index=False)

    print(f"Metrics for {result_file_name} have been added to the results file {output_file_name}.")


def main():
    args = parse_arguments()
    csv_file, json_file, predictions_data = load_data(args)
    df_predictions = prepare_predictions(predictions_data)

    df_ground_truth = pd.read_csv(csv_file)

    # Keep only relevant columns
    df_ground_truth = df_ground_truth[["key", "image_id", "description", "weight"]]
    df_ground_truth["description"] = df_ground_truth["description"].str.strip().str.lower()

    # Merge predictions with ground truth
    df_comparison = df_ground_truth.join(df_predictions)
    df_comparison["description_match"] = df_comparison["description"] == df_comparison["food_name"]

    # Display any mismatches
    mismatches = df_comparison[~df_comparison["description_match"]]
    if not mismatches.empty:
        print(f"Warning: {len(mismatches)} rows have mismatched description and food_name.")
        print(mismatches[["key", "description", "food_name"]])
    else:
        print("Rows have no mismatch!")

    # Filter only matching descriptions
    df_comparison = df_comparison[df_comparison["description_match"]].drop(columns=["description_match"])
    
    # Compute the errors
    df_comparison, mae, weighted_absolute_error, mape = compute_errors(df_comparison, args)

    # Display error metrics and append it to tracking file
    print(f"MAE (Mean Absolute Error): {mae:.4f} grams")
    print(f"Weighted MAE: {weighted_absolute_error:.4f} grams")
    print(f"MAPE (Mean Absolute Percentage Error): {mape:.4f}%\n")
    append_to_csv(mae, weighted_absolute_error, mape, json_file, "metrics_results.csv")

    df_comparison["url"] = df_comparison.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1)

    # Save sorted comparison results to file
    sorted_filename = f"../data/comparison/sorted_{args.json.split('.')[0]}.csv"
    if args.wholedata:
        sorted_df = df_comparison.sort_values(by="total_dish_wmae", ascending=False)
        sorted_df.to_csv(sorted_filename, index=False, columns=["key", "description", "weight", "predicted_weight", "absolute_error", "total_dish_wmae", "weighed_absolute_error", "url", "reasoning"])
    else:
        sorted_df = df_comparison.sort_values(by="absolute_error", ascending=False)
        sorted_df.to_csv(sorted_filename, index=False, columns=["key", "description", "weight", "predicted_weight", "absolute_error", "weighed_absolute_error", "url", "reasoning"])

    print(f"\nSorted results saved to {sorted_filename}.")

    if args.errors:
        print("\nTop 20 highest absolute errors with reasoning:\n" + "-" * 60)
        top_errors = df_comparison.sort_values(by="absolute_error", ascending=False).head(20)
        for i, row in top_errors.iterrows():
            print(f"\n#{i+1} - Key: {row['key']}")
            print(f"Description: {row['description']}")
            print(f"True weight: {row['weight']} g")
            print(f"Predicted weight: {row['predicted_weight']} g")
            print(f"Absolute error: {row['absolute_error']} g")
            print(f"URL: {row['url']}")
            print("Reasoning:")
            print(textwrap.fill(str(row['reasoning']), width=100))
            print("-" * 60)

    if args.best:
        print("\nTop 20 lowest absolute errors with reasoning:\n" + "-" * 60)
        top_errors = df_comparison.sort_values(by="absolute_error", ascending=False).tail(20)
        for i, row in top_errors.iterrows():
            print(f"\n#{i+1} - Key: {row['key']}")
            print(f"Description: {row['description']}")
            print(f"True weight: {row['weight']} g")
            print(f"Predicted weight: {row['predicted_weight']} g")
            print(f"Absolute error: {row['absolute_error']} g")
            print(f"URL: {row['url']}")
            print("Reasoning:")
            print(textwrap.fill(str(row['reasoning']), width=100))
            print("-" * 60)

if __name__ == "__main__":
    main()
