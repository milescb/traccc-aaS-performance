import os
import argparse

from performance.utils import process_csv_dir
from performance.nominal import plot_memory_usage, plot_power_usage, plot_throughput_and_GPUutil_vs_var
from performance.basic_plots import plot_multiple_vars, plot_var

# get command-line arguments
parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, help='Directory containing CSV files', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
parser.add_argument('--device', type=str, help='Device name',
                    default='NVIDIA A100 SXM4 80GB')
parser.add_argument('--title', type=str, help='Title for the plots',
                    default=r'ODD detector, $\mu = 200$, traccc v0.20.0')
args = parser.parse_args()

if not args.outdir:
    args.outdir = args.indir

# process data
cpu_data_instances, gpu_data_instances = process_csv_dir(args.indir)
data = gpu_data_instances
instances = sorted(data.keys())

throughputs = []
gpu_util = []
gpu_memory_util = []
gpu_power_util = []
server_infer = []
server_input = []
server_output = []

for inst in instances:
    tmp_data = data[inst][data[inst]['Concurrency'] == inst]
    throughputs.append(tmp_data['Inferences/Second'].values[0])
    gpu_util.append(tmp_data['total_gpu_usage'].values[0])
    gpu_memory_util.append(tmp_data['percent_gpu_memory'].values[0])
    gpu_power_util.append(tmp_data['largest_gpu_power_percent'].values[0])
    server_infer.append(tmp_data['Server Compute Infer'].values[0] * 1e-6)
    server_input.append(tmp_data['Server Compute Input'].values[0] * 1e-6)
    server_output.append(tmp_data['Server Compute Output'].values[0] * 1e-6)

# make plots   
plot_memory_usage(instances, gpu_memory_util, args.outdir, 
                  title=args.title, device=args.device)
plot_power_usage(instances, gpu_power_util, args.outdir, 
                 title=args.title, device=args.device)
plot_throughput_and_GPUutil_vs_var(instances, throughputs, gpu_util, args.outdir, 
                                   title=args.title, device=args.device)

plot_multiple_vars(instances, [server_infer, server_input, server_output],
                   ['Inference Latency', 'Input Processing Latency', 'Output Processing Latency'],
                   'Latency [s]', 'Number of Triton model instances',
                   filename=os.path.join(args.outdir, 'latency_breakdown.pdf'),
                   title=args.title, device=args.device)
plot_var(instances, server_infer, 'Inference Latency [s]', 
         'Number of Triton model instances', filename=os.path.join(args.outdir, 
         'inference_latency.pdf'), title=args.title, device=args.device)
