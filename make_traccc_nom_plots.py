import re
import argparse
import matplotlib.pyplot as plt
import os

from performance.utils import process_log_dir

import mplhep as hep
plt.style.use(hep.style.ATLAS)
plt.rcParams['legend.loc'] = 'upper right'

# Parse command line arguments
parser = argparse.ArgumentParser(description='Plot performance metrics')
parser.add_argument('--indir', type=str, help='Directory containing log files', required=True)
parser.add_argument('--outdir', type=str, help='Directory to save plots')
parser.add_argument('--device', type=str, help='Device name',
                    default='NVIDIA A100 SXM4 80GB')
parser.add_argument('--title', type=str, help='Title for the plots',
                    default='ODD detector, traccc v0.23.0')
args = parser.parse_args()

if not args.outdir:
    args.outdir = args.indir

# Create output directory if it doesn't exist
os.makedirs(args.outdir, exist_ok=True)

# Process data
data = process_log_dir(args.indir)

plt.figure(figsize=(7, 7))

cpu_mu = sorted(data['cpu'].keys())
cpu_time = [data['cpu'][mu] for mu in cpu_mu]
plt.plot(cpu_mu, cpu_time, label='AMD EPYC 7763 (48 CPU cores)', marker='o')

gpu_mu = sorted(data['gpu'].keys())
gpu_time = [data['gpu'][mu] for mu in gpu_mu]

TITLE = f"1 {args.device} on Perlmutter, {args.title}"
plt.plot(gpu_mu, gpu_time, label=f'{args.device} (1 CPU core)', marker='s')
plt.xlabel('Average interactions per bunch crossing', loc='right')
plt.ylabel('Throughput for full-chain (events / sec)', loc='top')
plt.title(TITLE, loc='left', fontsize=12)
plt.legend()
plt.yscale('log')

# Save plot
plt.savefig(os.path.join(args.outdir, 'performance.png'), bbox_inches='tight')
plt.close()