"""
This module contains functions to clean the data for performance tests
in comparison of concurrency vs model instances. 

The function process_csv_dir reads csv files of the form cpu_Xinstance.csv or 
gpu_Xinstance.csv and returns a dictionary of pandas DataFrames for each instance,
where X is the number of instances. This is the main function to retrieve the data
in the `plot_model_instance_studies.py` script.

Author: Miles Cochran-Branson
Date: 2024-08-05
"""

import re 
import os
import pandas as pd

def clean_pandas_df(df):
    df = df.sort_values(by='Concurrency', ascending=True)
    
    new_columns = {}
        
    for index, row in df.iterrows():
        # Split the cell content by ';' to get individual GPU utilizations
        gpus = row['Avg GPU Utilization'].rstrip(';').split(';')
        gpu_memory = row['Max GPU Memory Usage'].rstrip(';').split(';')
        gpu_total_memory = row['Total GPU Memory'].rstrip(';').split(';')
        
        for i, gpu in enumerate(gpus):
            _, utilization = gpu.split(':')
            new_col_name = f'gpu_util_{i}'
            
            # Add the utilization value to the new_columns dictionary
            if new_col_name not in new_columns:
                new_columns[new_col_name] = [None] * len(df) 
            new_columns[new_col_name][index] = pd.to_numeric(utilization, errors='coerce') * 100
            
        for i, mem in enumerate(gpu_memory):
            _, memory = mem.split(':')
            new_col_name = f'gpu_memory_{i}_GB'
            
            # Add the memory value to the new_columns dictionary
            if new_col_name not in new_columns:
                new_columns[new_col_name] = [None] * len(df) 
            new_columns[new_col_name][index] = pd.to_numeric(memory, errors='coerce') * 1e-9
            
        for i, mem in enumerate(gpu_total_memory):
            _, memory = mem.split(':')
            new_col_name = f'gpu_total_memory_{i}_GB'
            
            # Add the memory value to the new_columns dictionary
            if new_col_name not in new_columns:
                new_columns[new_col_name] = [None] * len(df) 
            new_columns[new_col_name][index] = pd.to_numeric(memory, errors='coerce') * 1e-9
    
    # Add the new columns to the DataFrame
    for new_col_name, values in new_columns.items():
        df[new_col_name] = values
        
    gpu_util_columns = [col for col in df.columns if 'gpu_util_' in col]
    df['total_gpu_usage'] = df[gpu_util_columns].sum(axis=1)
    
    gpu_highest_memory_columns = [col for col in df.columns if 'gpu_memory_' in col]
    df['max_gpu_memory'] = df[gpu_highest_memory_columns].max(axis=1)
    
    df['percent_gpu_memory'] = (df['max_gpu_memory'] / df['gpu_total_memory_0_GB']) * 100
        
    df.drop('Avg GPU Utilization', axis=1, inplace=True)
    df.drop('Max GPU Memory Usage', axis=1, inplace=True)
    df.drop('Total GPU Memory', axis=1, inplace=True)
    
    return df

def instance_number(filename):
    match = re.search(r'(cpu|gpu)_(\d+)instance_sync\.csv', filename)
    if match:
        return int(match.group(2))
    else:
        return None

def process_csv_dir(directory):
    gpu_data_instances = {}
    cpu_data_instances = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                if 'gpu' in filename:
                    gpu_data = pd.read_csv(file_path)
                    gpu_data = clean_pandas_df(gpu_data)
                    gpu_data_instances[instance_number(filename)] = gpu_data
                elif 'cpu' in filename:
                    cpu_data = pd.read_csv(file_path)
                    cpu_data = clean_pandas_df(cpu_data)
                    cpu_data_instances[instance_number(filename)] = cpu_data
    return cpu_data_instances, gpu_data_instances
    