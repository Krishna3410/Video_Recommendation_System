import pandas as pd
import os

# Define input and output directories
INPUT_DIR = "fetched_data"
OUTPUT_DIR = "processed_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_file(input_file, output_file):
    print(f"Processing {input_file}...")
    
    # Load the data
    df = pd.read_csv(input_file)
    
    # Handle missing values
    df.fillna("unknown", inplace=True)  # Fill missing values with "unknown" 
    
    # Normalize numerical fields 
    if 'rating_percent' in df.columns:
        df['rating_normalized'] = df['rating_percent'] / 100.0
    
    # Extract features from timestamps
    if 'viewed_at' in df.columns:
        df['viewed_date'] = pd.to_datetime(df['viewed_at'])
        df['viewed_hour'] = df['viewed_date'].dt.hour
        df['viewed_day'] = df['viewed_date'].dt.day_name()

    # Drop unnecessary columns
    if 'viewed_date' in df.columns:
        df.drop(columns=['viewed_date'], inplace=True)

    # Save the processed file
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

def preprocess_all_files():
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".csv"):
            input_file = os.path.join(INPUT_DIR, file_name)
            output_file = os.path.join(OUTPUT_DIR, file_name)
            preprocess_file(input_file, output_file)

if __name__ == "__main__":
    preprocess_all_files()
