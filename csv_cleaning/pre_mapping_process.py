import os
from cleaning.csv_cleaner_hdr import process_directory
from mapping.analyse_vendors import main as analyse_vendors
from mapping.create_mapping import main as create_mapping

def run_pre_mapping_process():
    """
    Runs all processes needed before manual mapping check:
    1. Clean CSVs
    2. analyse vendors
    3. Create initial mapping
    """
    try:
        print("=== Starting Pre-Mapping Process ===")
        
        # Get project paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_directory = os.path.join(current_dir, "data", "raw")
        output_directory = os.path.join(current_dir, "data", "cleaned")
        
        # Step 1: Clean CSVs
        print("\n1. Cleaning CSV files...")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        process_directory(input_directory)
        
        # Step 2: analyse vendors
        print("\n2. Analyzing vendor data...")
        analyse_vendors()
        
        # Step 3: Create initial mapping
        print("\n3. Creating initial mapping...")
        create_mapping()
        
        print("\n=== Pre-Mapping Process Complete ===")
        print("Please review and edit the mapping file in mapping/mapping_output/")
        print("Once complete, run the post_mapping_process.py script")
        
    except Exception as e:
        print(f"\nError in pre-mapping process: {str(e)}")
        raise

if __name__ == "__main__":
    run_pre_mapping_process()
