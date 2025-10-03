#!/usr/bin/env python3
"""Extract CSV files from the downloaded Excel file."""

import pandas as pd
import os

def extract_csvs():
    """Extract sheets from Excel file to individual CSV files."""
    
    # Read the Excel file
    excel_file = 'financial_data.xlsx'
    
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found. Please download it first.")
        return
    
    # Create fixtures directory if it doesn't exist
    os.makedirs('fixtures', exist_ok=True)
    
    try:
        # Read all sheets
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        # Expected sheet names and their corresponding CSV names
        sheet_mappings = {
            'actuals': 'actuals.csv',
            'budget': 'budget.csv', 
            'fx': 'fx.csv',
            'cash': 'cash.csv'
        }
        
        print("Available sheets:", list(excel_data.keys()))
        
        # Extract each sheet to CSV
        for sheet_name, csv_name in sheet_mappings.items():
            if sheet_name in excel_data:
                df = excel_data[sheet_name]
                csv_path = f'fixtures/{csv_name}'
                df.to_csv(csv_path, index=False)
                print(f"Extracted {sheet_name} -> {csv_path}")
                print(f"  Shape: {df.shape}")
                print(f"  Columns: {list(df.columns)}")
                print()
            else:
                print(f"Warning: Sheet '{sheet_name}' not found in Excel file")
        
        # If the expected sheet names don't exist, save all sheets
        if not any(sheet in excel_data for sheet in sheet_mappings.keys()):
            print("Expected sheets not found. Saving all sheets:")
            for sheet_name, df in excel_data.items():
                csv_path = f'fixtures/{sheet_name.lower()}.csv'
                df.to_csv(csv_path, index=False)
                print(f"Saved {sheet_name} -> {csv_path}")
                
    except Exception as e:
        print(f"Error processing Excel file: {e}")

if __name__ == "__main__":
    extract_csvs()
