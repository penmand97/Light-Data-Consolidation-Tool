import pandas as pd

def clean_vendor_data(file_path, output_path=None):
    """
    Cleans vendor data from the given file.
    
    Args:
        file_path (str): Path to the raw vendor data CSV file.
        output_path (str, optional): Path to save the cleaned file. If not provided, data is not saved.

    Returns:
        pd.DataFrame: Cleaned vendor data.
    """
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Deduplicate based on 'vendor_id' and 'vendor_name'
    data_cleaned = data.drop_duplicates(subset=['vendor_id', 'vendor_name'], keep='first')

    # Standardise capitalisation in text fields
    text_columns = ['vendor_name', 'owner', 'address', 'city', 'country', 'email']
    for col in text_columns:
        if col in data_cleaned.columns:
            data_cleaned[col] = data_cleaned[col].str.title()

    # Handle missing values - replacing blanks with 'Non Applicable'
    data_cleaned.fillna('Non Applicable', inplace=True)

    # Remove special characters and spaces from 'vendor_id'
    if 'vendor_id' in data_cleaned.columns:
        data_cleaned['vendor_id'] = data_cleaned['vendor_id'].astype(str).str.replace(r'[-.\s]', '', regex=True)
        # Flag non-alphanumeric IDs as 'Unknown'
        invalid_vendor_ids = ~data_cleaned['vendor_id'].str.isalnum()
        data_cleaned.loc[invalid_vendor_ids, 'vendor_id'] = 'Unknown'

    # Remove '.0' from 'number_belgian' and ensure it's string formatted
    if 'number_belgian' in data_cleaned.columns:
        data_cleaned['number_belgian'] = pd.to_numeric(data_cleaned['number_belgian'], errors='coerce')
        data_cleaned['number_belgian'] = data_cleaned['number_belgian'].fillna('Non Applicable').astype(str)
        data_cleaned['number_belgian'] = data_cleaned['number_belgian'].str.replace(r'\.0$', '', regex=True)

    # Remove special characters and spaces from 'vat_number'
    if 'vat_number' in data_cleaned.columns:
        data_cleaned['vat_number'] = data_cleaned['vat_number'].str.replace(r'[^\w]', '', regex=True)

    # Standardise IBAN formatting (remove spaces, ensure uppercase)
    if 'iban' in data_cleaned.columns:
        data_cleaned['iban'] = data_cleaned['iban'].str.replace(' ', '', regex=False).str.upper()

    # Save the cleaned data if output_path is provided
    if output_path:
        data_cleaned.to_csv(output_path, index=False)
        print(f"Cleaned data saved to: {output_path}")

    return data_cleaned

# Example usage
if __name__ == "__main__":
    # Update these paths to point to your actual files
    file_path = 'csv_cleaning/data/processed/deduplicated_consolidated_vendor_data.csv'  # Update this to your input file path
    output_path = 'csv_cleaning/data/processed/cleaned_vendor_data.csv'  # Update this to your desired output path
    
    # Clean the vendor data
    cleaned_data = clean_vendor_data(file_path, output_path)