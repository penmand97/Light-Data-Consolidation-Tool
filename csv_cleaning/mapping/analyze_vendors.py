import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

def process_cleaned_folder(cleaned_folder_path):
    """
    Process all CSV files in the cleaned folder
    """
    print(f"Processing files from: {cleaned_folder_path}")
    
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(cleaned_folder_path) if f.endswith('.csv')]
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Store DataFrames
    dfs = {}
    
    # Read each file
    for file in csv_files:
        file_path = os.path.join(cleaned_folder_path, file)
        print(f"\nProcessing: {file}")
        df = pd.read_csv(file_path)
        dfs[file] = df
        print(f"Loaded {len(df)} rows from {file}")
    
    return dfs

def analyse_columns(dfs):
    """
    analyse columns across all files
    """
    column_analysis = {}
    all_columns = set()
    
    # Collect all unique columns
    for file_name, df in dfs.items():
        all_columns.update(df.columns)
        column_analysis[file_name] = {
            'columns': list(df.columns),
            'sample_data': df.head(1).to_dict('records')[0]
        }
    
    # Create comparison matrix
    comparison = pd.DataFrame(index=dfs.keys(), columns=sorted(all_columns))
    for file_name, df in dfs.items():
        for col in all_columns:
            comparison.loc[file_name, col] = '✓' if col in df.columns else '-'
    
    return column_analysis, comparison

def generate_report(dfs, column_analysis, comparison, output_folder):
    """
    Generate a detailed analysis report
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save comparison matrix to CSV
    comparison_file = os.path.join(output_folder, f'column_comparison_{timestamp}.csv')
    comparison.to_csv(comparison_file)
    
    # Generate report
    report = {
        'analysis_timestamp': timestamp,
        'files_analysed': list(dfs.keys()),
        'row_counts': {file: len(df) for file, df in dfs.items()},
        'column_counts': {file: len(df.columns) for file, df in dfs.items()},
        'common_fields': list(set.intersection(*[set(df.columns) for df in dfs.values()])),
        'unique_fields': list(set.union(*[set(df.columns) for df in dfs.values()])),
        'column_details': column_analysis
    }
    
    # Save report to JSON
    report_file = os.path.join(output_folder, f'analysis_report_{timestamp}.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report, comparison_file, report_file

def main():
    """
    Main execution function
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Gets mapping/ directory
    project_root = os.path.dirname(current_dir)  # Goes up one level to csv_cleaning/
    
    # Define paths
    cleaned_folder = os.path.join(project_root, 'data', 'raw', 'cleaned')  # Point to csv_cleaning/data/raw/cleaned
    output_folder = os.path.join(project_root, 'mapping', 'analysis_output')  # Store analysis in mapping/analysis_output
    
    print("Starting vendor data analysis...")
    print(f"Reading cleaned files from: {cleaned_folder}")
    print(f"Saving analysis to: {output_folder}")
    
    # Process files
    try:
        # Load all CSV files
        dfs = process_cleaned_folder(cleaned_folder)
        
        # analyse columns
        column_analysis, comparison = analyse_columns(dfs)
        
        # Generate report
        report, comparison_file, report_file = generate_report(
            dfs, column_analysis, comparison, output_folder
        )
        
        # Print summary
        print("\nAnalysis Complete!")
        print(f"Files processed: {len(dfs)}")
        print(f"Output folder: {output_folder}")
        print(f"Generated files:")
        print(f"- Column comparison: {os.path.basename(comparison_file)}")
        print(f"- Analysis report: {os.path.basename(report_file)}")
        
        # Print comparison matrix
        print("\nColumn Comparison Matrix:")
        print(comparison)
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()