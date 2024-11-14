import pandas as pd
import os

# Function to ensure unique column names
def make_unique_columns(columns):
    seen = {}
    new_columns = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_columns.append(col)
    return new_columns

def consolidate_data():
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Load the mapping file from the mapping output folder
    mapping_folder = os.path.join(project_root, 'mapping', 'mapping_output')
    mapping_files = [f for f in os.listdir(mapping_folder) 
                    if f.startswith('field_mapping') and f.endswith('.csv')]

    # Add error handling and debugging
    if not mapping_files:
        print(f"Error: No 'field_mapping' files found in {mapping_folder}")
        print(f"Available items in directory: {os.listdir(mapping_folder)}")
        raise ValueError("No field mapping files found. Please ensure there are files starting with 'field_mapping' in the mapping_output directory")

    latest_mapping_file = max(mapping_files)
    mapping_file_path = os.path.join(mapping_folder, latest_mapping_file)

    mapping_df = pd.read_csv(mapping_file_path)

    # Create a dictionary to map source field names to standard field names
    mapping_dict = pd.Series(mapping_df['Standard Field'].values, index=mapping_df['Source Field']).to_dict()

    # Get paths to cleaned CSV files
    cleaned_folder = os.path.join(project_root, 'data', 'raw', 'cleaned')
    cleaned_files_paths = [
        os.path.join(cleaned_folder, f) 
        for f in os.listdir(cleaned_folder) 
        if f.endswith('.csv')
    ]

    # Initialise a DataFrame for the standardised and consolidated data
    standardised_consolidated_data = pd.DataFrame()

    # Process each cleaned file
    for file_path in cleaned_files_paths:
        print(f"Processing: {os.path.basename(file_path)}")
        # Load the cleaned data
        temp_df = pd.read_csv(file_path)
        
        # Standardise column names using the mapping file
        standardised_columns = {col: mapping_dict.get(col, col) for col in temp_df.columns}
        temp_df.rename(columns=standardised_columns, inplace=True)
        
        # Add missing columns from the mapping file if not present in the cleaned file
        for required_field in mapping_df['Standard Field'].unique():
            if required_field not in temp_df.columns:
                temp_df[required_field] = pd.NA  # Fill missing fields with NaN
        
        # Ensure unique column names
        temp_df.columns = make_unique_columns(temp_df.columns)
        
        # Append to the consolidated DataFrame
        standardised_consolidated_data = pd.concat([standardised_consolidated_data, temp_df], ignore_index=True)

    # Create processed folder if it doesn't exist
    processed_folder = os.path.join(project_root, 'data', 'processed')
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # Save the consolidated master file
    output_file_path = os.path.join(processed_folder, 'standardised_master_consolidated_data.csv')
    standardised_consolidated_data.to_csv(output_file_path, index=False)

    print(f"\nProcessed {len(cleaned_files_paths)} files")
    print(f"Total records in consolidated file: {len(standardised_consolidated_data)}")
    print(f"Master consolidated file saved to: {output_file_path}")

    return standardised_consolidated_data, output_file_path

# Add this to make the script runnable both as a module and directly
if __name__ == "__main__":
    consolidated_data, output_path = consolidate_data()