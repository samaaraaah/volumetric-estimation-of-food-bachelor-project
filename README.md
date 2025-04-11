# volumetric-estimation-of-food-bachelor-project

## Version 1 (v1-2025-04-03):  
give the llm one food class per image  
weight data not cleaned  

### Files:  
data/v1/comparison_data/comparison_{result_file_name}: contains the key, image_id, url, description, weight, predicted_weight, absolute_error of each food class that was annotated  
data/v1/comparison_data/sorted_{result_file_name}: contains the same lines as comparison file but with the absolute error sorted in decreasing order  
data/v1/prompt_data/prompt_{result_file_id}: contains the prompt used to generate the corresponding result file, using ChatGPT 4o (2024-11-20)  
data/v1/result/result_file_name: contains the resulting file from the LLM prediction  
data/weight_data.csv: original data  
data/v1/weight_data_ready.csv: original data formatted for the benchmarking tool  
data/v1/weight_data_sample.csv: sample (100) from original data  
data/v1/weight_data_sample_ready.csv: sample (100) from original data formatted for the benchmarking tool  
src/v1/comparison.py: script that creates the files in the folder comparison_data from a result file and writes the results of the metrics in metrics_results.csv  
src/v1/format.py: script that creates the formatted files for the benchmarking tool  
src/v1/metrics_results.csv: file containing the metrics results for each result file  

## Version 2 :  
give the llm all the food items on the image, ask it to evaluate the weight of only one food item  
data cleaned (in process)


data/cleaned/weight_data_cleaned.csv: original data, cleaned  
data/cleaned/weight_data_cleaned_grouped.csv: cleaned data with an additional column containing all the food items on the picture  
data/cleaned/weight_data_cleaned_sample.csv: sample (100) from cleaned data  
data/ready/weight_data_cleaned_ready.csv: cleaned data formatted for the benchmarking tool  
data/ready/weight_data_cleaned_sample_ready.csv: sample (100) from cleaned data formatted for the benchmarking tool  
data/comparison/sorted_{result_file_name}: contains the same lines as comparison file but with the absolute error sorted in decreasing order  
data/prompt/prompt_{result_file_id}: contains the prompt used to generate the corresponding result file, using ChatGPT 4o (2024-11-20)  
data/result/result_file_name: contains the resulting file from the LLM prediction  
data/weight_data.csv: original data  
data/removed_logs.csv: contains the removed rows and the reason why it was removed  
src/format.py: script that creates the formatted files for the benchmarking tool  
src/comparison.py: script that creates the files in the folder comparison from a result file and writes the results of the metrics in metrics_results.csv  
src/metrics_results.csv: file containing the metrics results for each result file  
