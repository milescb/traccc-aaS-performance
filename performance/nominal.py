import matplotlib.pyplot as plt

# ploting style
import mplhep as hep
plt.style.use(hep.style.ATLAS)
plt.rcParams['legend.loc'] = 'upper left'
figsize = (7, 7)
colors = plt.get_cmap('tab10')

TITLE = r"1 NVIDIA A100 SXM4 40GB, ODD detector, $\mu = 200$, traccc e7a03e9"

def plot_memory_usage(instances, gpu_memory_util, savedir):
    """
    Plot the GPU memory utilization as a function of the number of 
    Triton model instances.
    
    Parameters:
    - instances: list of integers, the number of Triton model instances
    - gpu_memory_util: list of floats, the GPU memory utilization
    - savedir: str, the directory to save the plot
    
    Returns:
    - None
    """
    
    fig = plt.figure(figsize=figsize)
    plt.plot(instances, gpu_memory_util, label='Throughput', 
             marker='o', color=colors(0))
    plt.title(TITLE, loc='left', fontsize=12)
    plt.xlabel('Number of Triton model instances')
    plt.ylabel('GPU Memory Utilization (%)')
    
    fig.savefig(f"{savedir}/gpu_memory_util.pdf", bbox_inches='tight')
    
def plot_throughput(instances, throughputs, gpu_util, savedir):
    """
    Plot throughput and GPU utilization as a function of the number of 
    Triton model instances.
    
    Parameters:
    - instances: list of integers, the number of Triton model instances
    - throughputs: list of floats, the throughput
    - gpu_util: list of floats, the GPU utilization
    - savedir: str, the directory to save the plot
    
    Returns:
    - None
    """
    fig, ax1 = plt.subplots(figsize=figsize)

    # Throughput axis
    ax1.plot(instances, throughputs, label='Throughput', 
             marker='o', color=colors(0))
    ax1.set_xlabel('Number of Triton Model Instances')
    ax1.set_ylabel('Throughput (Inferences/Second)')
    ax1.set_title(TITLE, loc='left', fontsize=12)
    ax1.yaxis.label.set_color(colors(0))
    ax1.tick_params(axis='y', colors=colors(0))

    # share y-axis
    ax2 = ax1.twinx()

    # GPU Utilization axis
    ax2.plot(instances, gpu_util, label='GPU Utilization', 
             marker='P', color=colors(1))
    ax2.set_ylabel('GPU Utilization (%)')
    ax2.set_ylim(0, 100)
    ax2.yaxis.label.set_color(colors(1))
    ax2.tick_params(axis='y', colors=colors(1))
    
    fig.savefig(f"{savedir}/throughput_gpu_util.pdf", bbox_inches='tight')