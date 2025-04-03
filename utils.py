import pandas as pd

def append_to_csv(mae, weighted_mae, mape, result_file_name):
    # Store the result for the current file
    metrics = {
        "result_file": result_file_name,  # Name of the file processed
        "MAE": mae,
        "MAPE": mape,
        "Weighted_MAE": weighted_mae
    }
    # Create a DataFrame from the metrics
    df_metrics = pd.DataFrame([metrics], columns=["result_file", "MAE", "MAPE", "Weighted_MAE"])

    metrics_file = "metrics_results.csv"

    # If the file exists, append the data, otherwise create it with header
    try:
        # Append the results to the file if new result
        ##TODO: replace old result with new
        df_metrics.to_csv(metrics_file, mode='a', header=False, index=False)
    except FileNotFoundError:
        # If the file does not exist, create it and add the header
        df_metrics.to_csv(metrics_file, mode='w', header=True, index=False)

    print(f"Metrics for {result_file_name} have been added to the results file {metrics_file}.")
