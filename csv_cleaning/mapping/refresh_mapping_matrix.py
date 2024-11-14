import pandas as pd
import os
from datetime import datetime

def refresh_mapping_matrix():
    """
    Read the latest edited mapping file and generate a fresh matrix
    """
    try:
        # Get the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets mapping/ directory
        project_root = os.path.dirname(current_dir)  # Goes up one level to csv_cleaning/

        # Set up mapping folder path
        mapping_folder = os.path.join(project_root, 'mapping', 'mapping_output')

        # Create directory if it doesn't exist
        os.makedirs(mapping_folder, exist_ok=True)

        # Find the most recent field_mapping CSV file
        csv_files = [f for f in os.listdir(mapping_folder) if f.startswith('field_mapping_') and f.endswith('.csv')]
        if not csv_files:
            print(f"No field mapping CSV files found in: {mapping_folder}")
            return
        
        latest_csv = max(csv_files)
        mapping_path = os.path.join(mapping_folder, latest_csv)
        
        print(f"\nProcessing mapping file: {latest_csv}")
        
        # Read the CSV file
        mapping_df = pd.read_csv(mapping_path)
        
        # Create new filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        matrix_file = os.path.join(mapping_folder, f'mapping_matrix_{timestamp}.csv')
        
        # Create and save the matrix
        print("Generating mapping matrix...")
        pivot_df = pd.pivot_table(
            mapping_df,
            values='Source Field',
            index='Standard Field',
            columns='Source',
            aggfunc=lambda x: ' | '.join(str(v) for v in x if pd.notnull(v))
        )
        pivot_df.to_csv(matrix_file)
        
        print(f"\nCreated matrix file: {os.path.basename(matrix_file)}")
        
        # Print summary
        print("\nMapping Summary:")
        print(f"Total fields: {len(mapping_df)}")
        print(f"Mapped fields: {len(mapping_df[mapping_df['Standard Field'] != 'UNMAPPED'])}")
        print(f"Unmapped fields: {len(mapping_df[mapping_df['Standard Field'] == 'UNMAPPED'])}")
        print(f"Sources: {', '.join(sorted(mapping_df['Source'].unique()))}")
        
        # Show unmapped fields
        unmapped = mapping_df[mapping_df['Standard Field'] == 'UNMAPPED']
        if len(unmapped) > 0:
            print("\nUnmapped fields that still need review:")
            for _, row in unmapped.iterrows():
                print(f"- {row['Source']}: {row['Source Field']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check that there are field_mapping_*.csv files in the mapping_output folder")
        print("2. Make sure the file is not open in another program")
        raise

if __name__ == "__main__":
    refresh_mapping_matrix()