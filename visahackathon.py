#!/usr/bin/env python3

import json
import os
import pandas as pd
import numpy as np

# Changing directory to current working
current_directory = os.getcwd()
working_directory = current_directory
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

average_spend = card_data_df["spend"].mean()

account_ids = [
    "94177e7a3daa4ef18746b355980ebd5f",
    "6r88582adf954cf6b3db6cc97bedccd9",
    "5a73582adf954cf6b3db6cc97yedood7",
    "5a73582adf954cf6b3db6cc97tedggd9",
    "5a73582adf954cf6b3db6cc97bedccd9",
]
segments = [
    "RESTAURANTS",
    "CHARITABLE/SOC SERVICE ORGS",
    "PARKING LOTS,METERS,GARAGES",
    "BARS/TAVERNS/LOUNGES/DISCOS",
    "LOCAL COMMUTER TRANSPORT",
]
mean_segment_spends = {
    account_id: {
        segment: open_banking_data_df[(open_banking_data_df["Value.accountId"] == account_id) & (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)]["amount"].mean()
        for segment in segments
    }
    for account_id in account_ids
}
sum_segment_spends = {
    account_id: {
        segment: open_banking_data_df[(open_banking_data_df["Value.accountId"] == account_id) & (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)]["amount"].sum()
        for segment in segments
    }
    for account_id in account_ids
}
count_segment_spends = {
    account_id: {
        segment: open_banking_data_df[(open_banking_data_df["Value.accountId"] == account_id) & (open_banking_data_df["mrch_catg_rlup_nm2"] == segment)]["amount"].shape[0]
        for segment in segments
    }
    for account_id in account_ids
}
average_segment_transaction = {
    segment: open_banking_data_df[(open_banking_data_df["mrch_catg_rlup_nm2"] == segment)]["amount"].mean()
    for segment in segments
} | { "RETAIL": 28.93756777 }

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
