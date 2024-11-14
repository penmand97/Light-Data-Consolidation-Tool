import os
from mapping.refresh_mapping_matrix import refresh_mapping_matrix
from utils.data_consolidation import consolidate_data
from cleaning.deduplicate_and_consolidate import deduplicate_and_consolidate
from cleaning.clean_vendor_data import clean_vendor_data

def run_post_mapping_process():
    """
    Runs all processes needed after manual mapping check:
    1. Refresh mapping matrix
    2. Consolidate data
    3. Deduplicate and consolidate
    4. Clean vendor data
    """
    try:
        print("=== Starting Post-Mapping Process ===")
        
        # Get project paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        processed_dir = os.path.join(current_dir, "data", "processed")
        
        # Step 1: Refresh mapping matrix
        print("\n1. Refreshing mapping matrix...")
        refresh_mapping_matrix()
        
        # Step 2: Consolidate data
        print("\n2. Consolidating data...")
        consolidate_data()
        
        # Step 3: Deduplicate and consolidate
        print("\n3. Deduplicating consolidated data...")
        deduplicate_and_consolidate()
        
        # Step 4: Final vendor data cleaning
        print("\n4. Performing final vendor data cleaning...")
        input_file = os.path.join(processed_dir, "deduplicated_consolidated_vendor_data.csv")
        output_file = os.path.join(processed_dir, "cleaned_vendor_data.csv")
        clean_vendor_data(input_file, output_file)
        
        print("\n=== Post-Mapping Process Complete ===")
        print(f"Final output file: {output_file}")
        
    except Exception as e:
        print(f"\nError in post-mapping process: {str(e)}")
        raise

if __name__ == "__main__":
    run_post_mapping_process()
