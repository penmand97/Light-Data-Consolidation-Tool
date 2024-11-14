import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

def create_mapping_table(analysis_folder):
    """
    Create a mapping table from analysis results
    """
    # Find the most recent analysis report
    reports = [f for f in os.listdir(analysis_folder) if f.startswith('analysis_report_')]
    latest_report = max(reports)
    report_path = os.path.join(analysis_folder, latest_report)
    
    # Load the analysis report
    with open(report_path, 'r') as f:
        analysis = json.load(f)
    
    # Create mapping table structure
    mapping_data = []
    
    # Standard field names we want to map to
    standard_fields = {
        'vendor_id': ['Vendor ID', 'Vendor Number', 'Vendor identifier', 'Vendor ID Number'],
        'vendor_name': ['Vendor name', 'Name', 'Vendor Name', 'Description'],
        'address': ['Address', 'Comapny Address'],
        'postal_code': ['ZIP/postcode', 'ZIP', 'Postcode'],
        'city': ['City'],
        'country': ['Country'],
        'email': ['Email', 'Email for Contact'],
        'vat_number': ['VAT Code', 'VAT-No'],
        'currency': ['Currency', 'Currency code'],
        'iban': ['IBAN'],
        'bic': ['BIC'],
        'bank_name': ['Bank Name', 'Bank name'],
        'bank_country': ['Bank country', 'Bank Country'],
        'company_entity': ['Company entities'],
        'group': ['Vendor Group', 'Groups', 'Group']
    }
    
    # Process each file's columns
    for file_name, details in analysis['column_details'].items():
        source = file_name.replace('cleaned_', '').replace('.csv', '')
        
        # Map each column
        for column in details['columns']:
            # Find standard field match
            standard_field = None
            for std_field, variations in standard_fields.items():
                if column in variations or any(var.lower() == column.lower() for var in variations):
                    standard_field = std_field
                    break
            
            # Get sample data
            sample_value = details['sample_data'].get(column, '')
            
            mapping_data.append({
                'Source': source,
                'Source Field': column,
                'Standard Field': standard_field or 'UNMAPPED',
                'Sample Data': str(sample_value),
                'Data Type': str(type(sample_value).__name__),
                'Required': 'Yes' if standard_field in ['vendor_id', 'vendor_name', 'country'] else 'No',
                'Notes': ''
            })
    
    # Create mapping DataFrame
    mapping_df = pd.DataFrame(mapping_data)
    
    # Sort by Standard Field and Source
    mapping_df = mapping_df.sort_values(['Standard Field', 'Source'])
    
    return mapping_df

def generate_mapping_files(mapping_df, output_folder):
    """
    Generate CSV files with mapping table and mapping matrix
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate field mapping CSV
    mapping_output = os.path.join(output_folder, f'field_mapping_{timestamp}.csv')
    mapping_df.to_csv(mapping_output, index=False)
    
    # Create and save mapping matrix CSV
    matrix_output = os.path.join(output_folder, f'mapping_matrix_{timestamp}.csv')
    pivot_df = pd.pivot_table(
        mapping_df,
        values='Source Field',
        index='Standard Field',
        columns='Source',
        aggfunc=lambda x: ' | '.join(str(v) for v in x if pd.notnull(v))
    )
    pivot_df.to_csv(matrix_output)
    
    return mapping_output, matrix_output

def main():
    """
    Main execution function
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    analysis_folder = os.path.join(current_dir, 'analysis_output')
    output_folder = os.path.join(current_dir, 'mapping_output')
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print("Creating vendor mapping table...")
    
    try:
        # Create mapping table
        mapping_df = create_mapping_table(analysis_folder)
        
        # Generate CSV files
        mapping_file, matrix_file = generate_mapping_files(mapping_df, output_folder)
        
        print("\nMapping files created successfully!")
        print(f"Field mapping file: {mapping_file}")
        print(f"Mapping matrix file: {matrix_file}")
        
        # Print summary
        print("\nMapping Summary:")
        print(f"Total fields mapped: {len(mapping_df[mapping_df['Standard Field'] != 'UNMAPPED'])}")
        print(f"Unmapped fields: {len(mapping_df[mapping_df['Standard Field'] == 'UNMAPPED'])}")
        print(f"Sources analysed: {len(mapping_df['Source'].unique())}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()