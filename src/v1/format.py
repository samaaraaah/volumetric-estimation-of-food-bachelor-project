import pandas as pd

input_file = "../../data/weight_data.csv" 
output_file = "../../data/v1/weight_data_ready.csv" # Formatted for the benchmarking tool
sample_file = "../../data/v1/weight_data_sample.csv"
sample_output_file = "../../data/v1/weight_data_sample_ready.csv"  # Formatted for the benchmarking tool

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)
random_seed = 30
sample_df = df.sample(n=100, random_state=random_seed) #fixed random sample
sample_df["description"] = sample_df["description"].str.lower() 
sample_df.to_csv(sample_file, index=False)

# Create the new CSV with 'id' and '00_MSG_00_IMAGE' and '00_MSG_01_TEXT'
output_data = {
    'id': range(len(df)),  
    '00_MSG_00_IMAGE': df.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),  # Generate the URL
    '00_MSG_01_TEXT': df['description'].str.lower() # Retrieve the description given by the user
}
sample_output_data = {
    'id': range(len(sample_df)),  
    '00_MSG_00_IMAGE': sample_df.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),  # Generate the URL
    '00_MSG_01_TEXT': sample_df['description'] # Retrieve the description given by the user
}

# Create a new DataFrame for the output
output_df = pd.DataFrame(output_data)
sample_output_df = pd.DataFrame(sample_output_data)

# Save the output DataFrame to a new CSV
output_df.to_csv(output_file, index=False)
sample_output_df.to_csv(sample_output_file, index=False)

print(f"Output saved to {output_file} and {sample_output_file}")