import pandas as pd
import matplotlib.pyplot as plt

import mplhep as hep
hep.style.use(hep.style.ATLAS)

TITLE = r'NVIDIA A100 SXM4 40GB GPUs, ODD detector, $\mu = 200$, traccc e7a03e9'

def plot_memory_usage(data, OUT_DIR, N_INSTANCES, PLOT_INST_LABEL):
    """
    
    """
    plt.figure(figsize=(7, 7))
    for i in range(4):
        plt.plot(data['Concurrency'].values, 
                 data[f'gpu_memory_{i}_GB'].values/data[f'gpu_total_memory_1_GB']*100, 
                'o-', label=f'Device ID {i}')
    plt.xlabel('Number of concurrent requests', loc='right')
    plt.ylabel('GPU Memory Utilization (%)', loc='top')
    plt.title(TITLE, fontsize=10, loc='left')
    plt.legend(title=f'{PLOT_INST_LABEL} triton model instance per GPU')
    plt.ylim(0, 60)

    plt.savefig(f'{OUT_DIR}/concurrency_vs_gpu_memory_util_{N_INSTANCES}inst.pdf', 
                    bbox_inches='tight')
    
def plot_throughput(data, data_1gpu, OUT_DIR, N_INSTANCES, PLOT_INST_LABEL):
    """
    
    """
    plt.figure(figsize=(7, 7))
    plt.plot(data_1gpu['Concurrency'].values, data_1gpu['Inferences/Second'].values, 
             'o-', label='1 NVIDIA A100 SXM4 40GB')
    plt.plot(data['Concurrency'].values, data['Inferences/Second'].values, 
             'o-', label='4 NVIDIA A100 SXM4 40GB')
    plt.xlabel('Number of concurrent requests', loc='right')
    plt.ylabel('Throughput (infer/sec)', loc='top')
    plt.title(r'ODD detector, $\mu = 200$, traccc e7a03e9', fontsize=10, loc='left')
    plt.legend(title=f'{PLOT_INST_LABEL} triton model instance per GPU')

    plt.savefig(f'{OUT_DIR}/concurrency_vs_throughput_{N_INSTANCES}inst.pdf', 
                    bbox_inches='tight')
    
def plot_gpu_utilization(data, OUT_DIR, N_INSTANCES, PLOT_INST_LABEL):
    """
    
    """
    plt.figure(figsize=(7, 7))
    for i in range(4):
        plt.plot(data['Concurrency'].values, data[f'gpu_util_{i}'].values, 
                'o-', label=f'Device ID {i}')
    plt.xlabel('Number of concurrent requests', loc='right')
    plt.ylabel('GPU Utilization (%)', loc='top')
    plt.title(TITLE, fontsize=10, loc='left')
    plt.legend(title=f'{PLOT_INST_LABEL} triton model instance per GPU')

    plt.savefig(f'{OUT_DIR}/concurrency_vs_gpu_util_{N_INSTANCES}inst.pdf', 
                    bbox_inches='tight')