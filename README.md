# volumetric-estimation-of-food-bachelor-project

## Version 1 (v1-2025-04-03):  
give the llm one food class per image  
weight data not cleaned  

### Files in v1-2025-04-03:  
data/comparison_data/comparison_{result_file_name}: contains the key, image_id, url, description, weight, predicted_weight, absolute_error of each food class that was annotated  
data/comparison_data/sorted_{result_file_name}: contains the same lines as comparison file but with the absolute error sorted in decreasing order  
data/prompt_data/prompt_{result_file_id}: contains the prompt used to generate the corresponding result file, using ChatGPT 4o (2024-11-20)  
data/result/result_file_name: contains the resulting file from the LLM prediction  
data/weight_data.csv: original data  
data/weight_data_ready.csv: original data formatted for the benchmarking tool  
data/weight_data_sample.csv: sample (100) from original data  
data/weight_data_sample_ready.csv: sample (100) from original data formatted for the benchmarking tool  
comparison.py: script that creates the files in the folder comparison_data from a result file and writes the results of the metrics in metrics_results.csv  
format.py: script that creates the formatted files for the benchmarking tool  
metrics_results.csv: file containing the metrics results for each result file  

## Version 2 :  
give the llm all the food items on the image, ask it to evaluate the weight of only one food item
data cleaned (in process)


data/weight_data_cleaned.csv: original data, cleaned  
data/weight_data_cleaned_grouped.csv: cleaned data with an additional column containing all the food items on the picture  
data/weight_data_v2_ready.csv: cleaned data formatted for the benchmarking tool  
data/weight_data_v2_sample.csv: sample (100) from cleaned data  
data/weight_data_v2_sample_ready.csv: sample (100) from cleaned data formatted for the benchmarking tool  
format.py: script that creates the formatted files for the benchmarking tool  