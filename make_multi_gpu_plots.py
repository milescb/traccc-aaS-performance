import argparse
import pandas as pd

from performance.utils import clean_pandas_df, int_to_string
from performance.multi_gpu import plot_memory_usage, plot_throughput, plot_gpu_utilization

# get command-line arguments
parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, help='Directory containing CSV files', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
parser.add_argument('--n-instances', type=int, help='Number of Triton model instances per GPU', required=True)
args = parser.parse_args()

# process data
N_INSTANCES = args.n_instances
PLOT_INST_LABEL = int_to_string(N_INSTANCES)

IN_FILE = f"/{N_INSTANCES}insts_4gpus/gpu_{N_INSTANCES}instance_sync.csv"
IN_FILE_1GPU = f"/{N_INSTANCES}insts_1gpus/gpu_{N_INSTANCES}instance_sync.csv"

data = pd.read_csv(args.indir + IN_FILE)
data = clean_pandas_df(data)

data_1gpu = pd.read_csv(args.indir + IN_FILE_1GPU)
data_1gpu = clean_pandas_df(data_1gpu)

# plot the data
plot_memory_usage(data, args.outdir, N_INSTANCES, PLOT_INST_LABEL)
plot_throughput(data, data_1gpu, args.outdir, N_INSTANCES, PLOT_INST_LABEL)
plot_gpu_utilization(data, args.outdir, N_INSTANCES, PLOT_INST_LABEL)