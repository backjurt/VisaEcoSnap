import os
import pandas as pd
import numpy as np

# Changing directory to current working
#current_directory = os.getcwd()
working_directory = '/Users/jackburt/OneDrive/Documents/AI/Visa Hackathon/MVP'
os.chdir(working_directory)

file_name = 'Visa Climate Tech Data.xlsx'
file_path = os.path.join(working_directory, file_name)

# Reading the file
excel_data = pd.ExcelFile(file_name)
sheet_names = excel_data.sheet_names
#print(sheet_names)

# Reading the sheets into DataFrames
card_data_df = pd.read_excel(excel_data, sheet_name='2_Card data')
open_banking_data_df = pd.read_excel(excel_data, sheet_name='3_Open banking data')

#print(card_data_df.head(10))
#print(open_banking_data_df.head(10))

# Select the column to analyze
column_name_card = 'mrch_catg_rlup_nm'
column_name_open = 'mrch_catg_rlup_nm2'

# Count the number of unique values in the column
unique_count_card = card_data_df[column_name_card].nunique()
print(f"Number of unique values in '{column_name_card}': {unique_count_card}")

unique_count_open = open_banking_data_df[column_name_open].nunique()
print(f"Number of unique values in '{column_name_open}': {unique_count_open}")

# List the unique values in the column

unique_values_card = card_data_df[column_name_card].unique()
#print(f"Unique values in '{column_name_card}': {unique_values_card}")

unique_values_open = open_banking_data_df[column_name_open].unique()
#print(f"Unique values in '{column_name_open}': {unique_values_open}")

# Filter out elements that are not strings
#unique_values_card_not_str = [x for x in unique_values_card if not isinstance(x, str)]
#unique_values_open_not_str = [x for x in unique_values_open if not isinstance(x, str)]
#--------------------------------------------------------------------------------------------------------------------------------------
'''# Convert all elements to strings for comparison
unique_values_card = [str(x) for x in unique_values_card]
unique_values_open = [str(x) for x in unique_values_open]

def compare_arrays(arr1, arr2):
    return sorted(arr1) == sorted(arr2)

print(compare_arrays(unique_values_card, unique_values_open)) # Result is False'''