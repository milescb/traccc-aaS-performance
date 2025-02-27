import argparse

from performance.utils import process_csv_dir
from performance.nominal import plot_memory_usage, plot_throughput

# get command-line arguments
parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, help='Directory containing CSV files', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
args = parser.parse_args()

# process data
cpu_data_instances, gpu_data_instances = process_csv_dir(args.indir)
data = gpu_data_instances
instances = sorted(data.keys())

throughputs = []
gpu_util = []
gpu_memory_util = []

for inst in instances:
    tmp_data = data[inst][data[inst]['Concurrency'] == inst]
    throughputs.append(tmp_data['Inferences/Second'].values[0])
    gpu_util.append(tmp_data['total_gpu_usage'].values[0])
    gpu_memory_util.append(tmp_data['percent_gpu_memory'].values[0])

# make plots   
plot_memory_usage(instances, gpu_memory_util, args.outdir)
plot_throughput_and_GPUutil_vs_var(instances, throughputs, gpu_util, args.outdir)
