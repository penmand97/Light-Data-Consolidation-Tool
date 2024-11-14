import pandas as pd
import numpy as np
import os

def find_first_nonempty_row(file_path):
    """
    Find the index of the first non-empty row in the CSV
    """
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            if line.strip() and not all(cell.strip() == '' for cell in line.split(',')):
                return index
    return 0

def clean_csv(df):
    """
    Clean a CSV DataFrame by:
    1. Removing empty rows
    2. Handling merged cells
    3. Removing duplicate rows
    """
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Forward fill merged cells
    df = df.fillna(method='ffill')
    
    # Remove duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate rows")
    
    return df

def process_csv_file(file_path, output_path=None):
    """
    Process a single CSV file and save the cleaned version
    """
    try:
        # Find the first non-empty row to use as header
        header_row = find_first_nonempty_row(file_path)
        
        # Read the CSV file using the first non-empty row as header
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path, header=header_row, dtype=str)
        
        # Clean the data
        cleaned_df = clean_csv(df)
        
        # If no output path specified, create one
        if output_path is None:
            output_path = file_path.rsplit('.', 1)[0] + '_cleaned.csv'
        
        # Save cleaned data
        cleaned_df.to_csv(output_path, index=False)
        print(f"Cleaned file saved to: {output_path}")
        
        # Print some statistics
        print(f"Original rows: {len(df)}")
        print(f"Cleaned rows: {len(cleaned_df)}")
        print(f"Total rows removed: {len(df) - len(cleaned_df)}")
        
        return cleaned_df
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def process_directory(directory_path):
    """
    Process all CSV files in a directory
    """
    # Create 'cleaned' subdirectory if it doesn't exist
    cleaned_dir = os.path.join(directory_path, 'cleaned')
    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)
    
    # Process each CSV file
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(cleaned_dir, f'cleaned_{filename}')
            process_csv_file(input_path, output_path)

if __name__ == "__main__":
    # Get the project root directory
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Gets cleaning/ directory
    project_root = os.path.dirname(current_directory)  # Goes up one level to csv_cleaning/
    
    # Specify the input and output directories
    input_directory = os.path.join(project_root, "data", "raw")
    output_directory = os.path.join(project_root, "data", "cleaned")  # Will create cleaned/ next to raw/
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Process all CSV files
    process_directory(input_directory)