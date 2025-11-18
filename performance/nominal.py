import numpy as np
import matplotlib.pyplot as plt

# ploting style
import mplhep as hep
plt.style.use(hep.style.ATLAS)
plt.rcParams['legend.loc'] = 'upper left'
figsize = (7, 7)
colors = plt.get_cmap('tab10')

def plot_memory_usage(instances, gpu_memory_util, savedir, 
                      title=r"ODD detector, $\mu = 200$, traccc e7a03e9",
                      device="NVIDIA A100 SXM4 40GB",
                      gpu_memory_util_std=None):
    """
    Plot the GPU memory utilization as a function of the number of 
    Triton model instances.
    """
    
    fig = plt.figure(figsize=figsize)
    plt.errorbar(instances, gpu_memory_util, yerr=gpu_memory_util_std,
                 label='GPU Memory Utilization', marker='o', color=colors(0),
                 capsize=5, capthick=2)
    plt.title(device+", "+title, loc='left', fontsize=12)
    plt.xlabel('Number of Triton model instances')
    plt.ylabel('GPU Memory Utilization (%)')
    plt.xlim(1, max(instances))
    
    fig.savefig(f"{savedir}/gpu_memory_util.pdf", bbox_inches='tight')
    
def plot_power_usage(instances, gpu_power_util, savedir, 
                      title=r"ODD detector, $\mu = 200$, traccc e7a03e9",
                      device="NVIDIA A100 SXM4 40GB",
                      gpu_power_util_std=None):
    """
    Plot the GPU power utilization as a function of the number of 
    Triton model instances.
    """
    
    fig = plt.figure(figsize=figsize)
    plt.errorbar(instances, gpu_power_util, yerr=gpu_power_util_std,
                 label='GPU Power Utilization', marker='o', color=colors(0),
                 capsize=5, capthick=2)
    plt.title(device+", "+title, loc='left', fontsize=12)
    plt.xlabel('Number of Triton model instances')
    plt.ylabel('GPU Power Utilization (%)')
    plt.xlim(1, max(instances))
    
    fig.savefig(f"{savedir}/gpu_power_util.pdf", bbox_inches='tight')
    
def plot_throughput_and_GPUutil_vs_var(variable, throughputs, gpu_util, savedir, 
                           xlabel='Number of Triton Model Instances',
                           device="NVIDIA A100 SXM4 40GB",
                           title=r'ODD detector, $\mu = 200$, traccc e7a03e9',
                           throughputs_std=None, gpu_util_std=None):
    fig, ax1 = plt.subplots(figsize=figsize)

    # Throughput axis with error bars
    ax1.errorbar(variable, throughputs, yerr=throughputs_std, 
                 label='Throughput', marker='o', color=colors(0),
                 capsize=5, capthick=2)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Throughput (Inferences/Second)')
    ax1.set_title(device+', '+title, loc='left', fontsize=12)
    ax1.yaxis.label.set_color(colors(0))
    ax1.tick_params(axis='y', colors=colors(0))
    ax1.set_xlim(1, max(variable))

    # share y-axis
    ax2 = ax1.twinx()

    # GPU Utilization axis with error bars
    ax2.errorbar(variable, gpu_util, yerr=gpu_util_std,
                 label='GPU Utilization', marker='P', color=colors(1),
                 capsize=5, capthick=2)
    ax2.set_ylabel('Average GPU Utilization (%)', rotation=270, y=0.67, labelpad=20)
    ax2.set_ylim(0, 100)
    ax2.yaxis.label.set_color(colors(1))
    ax2.tick_params(axis='y', colors=colors(1))
    
    fig.savefig(f"{savedir}/throughput_gpu_util.pdf", bbox_inches='tight')