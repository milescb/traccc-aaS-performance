import os
import argparse
import numpy as np

from performance.utils import process_csv_dir
from performance.nominal import plot_memory_usage, plot_power_usage, plot_throughput_and_GPUutil_vs_var
from performance.basic_plots import plot_multiple_vars, plot_var

def process_data(indirs):
    
    # Collect data from all runs
    all_runs_data = []
    all_instances = []

    for indir in indirs:
        cpu_data_instances, gpu_data_instances = process_csv_dir(indir)
        data = gpu_data_instances
        instances = sorted(data.keys())
        all_instances.append(set(instances))
        
        run_data = {
            'instances': instances,
            'throughputs': {},
            'gpu_util': {},
            'gpu_memory_util': {},
            'gpu_power_util': {},
            'server_infer': {},
            'server_input': {},
            'server_output': {}
        }
        
        for inst in instances:
            tmp_data = data[inst][data[inst]['Concurrency'] - 3 == inst]
            run_data['throughputs'][inst] = tmp_data['Inferences/Second'].values[0]
            run_data['gpu_util'][inst] = tmp_data['total_gpu_usage'].values[0]
            run_data['gpu_memory_util'][inst] = tmp_data['percent_gpu_memory'].values[0]
            run_data['gpu_power_util'][inst] = tmp_data['largest_gpu_power_percent'].values[0]
            run_data['server_infer'][inst] = tmp_data['Server Compute Infer'].values[0] * 1e-6
            run_data['server_input'][inst] = tmp_data['Server Compute Input'].values[0] * 1e-6
            run_data['server_output'][inst] = tmp_data['Server Compute Output'].values[0] * 1e-6
        
        all_runs_data.append(run_data)
        
    return all_runs_data, all_instances
    

def main():
    
    all_runs_data, all_instances = process_data(indirs)

    # Find common instances across all runs
    common_instances = sorted(set.intersection(*all_instances))
    print(f"Common instances across all runs: {common_instances}")

    # Calculate means and standard deviations for common instances
    metrics = ['throughputs', 'gpu_util', 'gpu_memory_util', 'gpu_power_util', 
            'server_infer', 'server_input', 'server_output']

    results = {}
    for metric in metrics:
        values = []
        for inst in common_instances:
            inst_values = [run[metric][inst] for run in all_runs_data]
            values.append(inst_values)
        
        results[metric] = np.mean(values, axis=1)
        results[metric + '_std'] = np.std(values, axis=1)

    instances = common_instances
    throughputs = results['throughputs']
    throughputs_std = results['throughputs_std']
    gpu_util = results['gpu_util']
    gpu_util_std = results['gpu_util_std']
    gpu_memory_util = results['gpu_memory_util']
    gpu_memory_util_std = results['gpu_memory_util_std']
    gpu_power_util = results['gpu_power_util']
    gpu_power_util_std = results['gpu_power_util_std']
    # server_infer = results['server_infer']
    # server_infer_std = results['server_infer_std']
    # server_input = results['server_input']
    # server_input_std = results['server_input_std']
    # server_output = results['server_output']
    # server_output_std = results['server_output_std']

    # make plots   
    plot_memory_usage(instances, gpu_memory_util, args.outdir, 
                    title=args.title, device=args.device,
                    gpu_memory_util_std=gpu_memory_util_std)
    plot_power_usage(instances, gpu_power_util, args.outdir, 
                    title=args.title, device=args.device,
                    gpu_power_util_std=gpu_power_util_std)
    plot_throughput_and_GPUutil_vs_var(instances, throughputs, gpu_util, args.outdir, 
                                    title=args.title, device=args.device,
                                    throughputs_std=throughputs_std,
                                    gpu_util_std=gpu_util_std)

    # plot_multiple_vars(instances, [server_infer, server_input, server_output],
    #                    ['Inference Latency', 'Input Processing Latency', 'Output Processing Latency'],
    #                    'Latency [s]', 'Number of Triton model instances',
    #                    filename=os.path.join(args.outdir, 'latency_breakdown.pdf'),
    #                    title=args.title, device=args.device,
    #                    yerr=[server_infer_std, server_input_std, server_output_std])
    # plot_var(instances, server_infer, 'Inference Latency [s]', 
    #          'Number of Triton model instances', filename=os.path.join(args.outdir, 
    #          'inference_latency.pdf'), title=args.title, device=args.device,
    #          yerr=server_infer_std)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Plot performance metrics')
    parser.add_argument('--indir', type=str, nargs='+', help='Directory(ies) containing CSV files', required=True)
    parser.add_argument('--outdir', type=str, help='Directory to save plots')
    parser.add_argument('--device', type=str, help='Device name',
                        default='NVIDIA A100 SXM4 40GB')
    parser.add_argument('--title', type=str, help='Title for the plots',
                        default=r'ITk detector, $\mu = 200$, traccc 0.26.0')
    args = parser.parse_args()

    if not args.outdir:
        args.outdir = args.indir[0] if isinstance(args.indir, list) else args.indir

    # Support both single directory and multiple directories
    indirs = args.indir if isinstance(args.indir, list) else [args.indir]
    
    main()