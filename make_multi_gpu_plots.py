import argparse
import pandas as pd

from performance.utils import clean_pandas_df, int_to_string
from performance.multi_gpu import plot_memory_usage, plot_throughput, plot_gpu_utilization

# get command-line arguments
parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, help='Directory containing CSV files', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
parser.add_argument('--inFile-1gpu', type=str, 
                    help='CSV file for 1 GPU', required=True)
parser.add_argument('--inFile-multiGpu', type=str, 
                    help='CSV file for multiple GPUs', required=True)
parser.add_argument('--device', type=str, help='Device name', 
                    default='NVIDIA A100 SXM4 40GB')
parser.add_argument('--title', type=str, help='Title for the plots',
                    default='ODD detector, $\mu = 200$, traccc e7a03e9')
parser.add_argument('--n-GPUs', type=int, help='Number of GPUs', default=4)
parser.add_argument('--n-instances', type=int, help='Number of Triton model instances per GPU', default=1)
args = parser.parse_args()

# process data
N_INSTANCES = args.n_instances
PLOT_INST_LABEL = int_to_string(N_INSTANCES)

data = pd.read_csv(args.indir + args.inFile_multiGpu)
data = clean_pandas_df(data)

data_1gpu = pd.read_csv(args.indir + args.inFile_1gpu)
data_1gpu = clean_pandas_df(data_1gpu)

# plot the data
plot_memory_usage(data, args.outdir, N_INSTANCES, PLOT_INST_LABEL,
                  device=args.device, title=args.title)
plot_throughput(data, data_1gpu, args.outdir, N_INSTANCES, PLOT_INST_LABEL,
                nGPUs=args.n_GPUs, device=args.device, title=args.title)
plot_gpu_utilization(data, args.outdir, N_INSTANCES, PLOT_INST_LABEL,
                     device=args.device, title=args.title)