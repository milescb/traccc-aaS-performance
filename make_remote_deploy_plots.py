import os
import argparse
import pandas as pd

from performance.utils import clean_pandas_df, int_to_string
from performance.basic_plots import plot_var, plot_multiple_vars, plot_var_and_compare
from performance.nominal import plot_throughput_and_GPUutil_vs_var
from performance.multi_gpu import plot_gpu_utilization, plot_memory_usage, plot_gpu_power_usage

parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, 
                    help='Directory containing CSV files', required=True)
parser.add_argument('--infile', type=str, 
                    help='CSV file name', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
parser.add_argument('--device', type=str, help='Device name',
                    default='NVIDIA RTX 2080')
parser.add_argument('--title', type=str, help='Title for the plots',
                    default=r'ODD detector, $\mu = 200$, traccc e7a03e9')
parser.add_argument('--n-GPUs', type=int, help='Number of GPUs', default=2)
parser.add_argument('--n-instances', type=int, 
                    help='Number of Triton model instances per GPU', default=1)
args = parser.parse_args()

if not args.outdir:
    args.outdir = args.indir

data = pd.read_csv(os.path.join(args.indir, args.infile))
data = clean_pandas_df(data)

# avg GPU utilization over all GPUs
avg_gpu_util = data[[col for col in data.columns if 'gpu_util' in col]].mean(axis=1)

plot_throughput_and_GPUutil_vs_var(data['Concurrency'], 
                                   data['Inferences/Second'],
                                   avg_gpu_util, args.outdir,
                                   xlabel='Number of Concurrent Requests',
                                   device=args.device,
                                   title=args.title)

# plot latency breakdown
plot_multiple_vars(data['Concurrency'], 
                   [data['Server Compute Infer'] * 1e-6, 
                        data['Server Compute Input']*1e-6, 
                        data['Server Compute Output']*1e-6],
                   ['Inference Latency', 
                        'Input Processing Latency', 
                        'Output Processing Latency'],
                    'Latency [s]', 
                    'Number of Concurrent Requests',
                    filename=os.path.join(args.outdir, 'latency_breakdown.pdf'))

plot_var(data['Concurrency'], data['Server Compute Infer'] * 1e-6, 
         'Inference Latency [s]', 'Number of Concurrent Requests',
         filename=os.path.join(args.outdir, 'inference_latency_4gpu.pdf'))

# plot GPU utilization for each GPU
plot_gpu_utilization(data, args.outdir, args.n_instances, nGPUs=2,
                     device=args.device,
                     title=args.title)
plot_memory_usage(data, args.outdir, args.n_instances, nGPUs=2,
                     device=args.device,
                     title=args.title)
plot_gpu_power_usage(data, args.outdir, args.n_instances, nGPUs=2,
                    device=args.device,
                    title=args.title)
