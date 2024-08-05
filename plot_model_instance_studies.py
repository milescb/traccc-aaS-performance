
import matplotlib.pyplot as plt
import argparse

from performance.utils import process_csv_dir

def plot_instance_cpu_gpu(cpu_data, gpu_data, concurrency=1, 
                          variable='Inferences/Second',
                          ylabel='Throughput (infer/sec)',
                          save_name='instances_vs_throughput_compare_con3.pdf'):
    
    plt.figure(figsize=(6, 6))
    
    in_cpu = sorted(cpu_data.keys())
    in_gpu = sorted(gpu_data.keys())
    
    vals_cpu = []
    vals_gpu = []
    for i in in_cpu:
        val = cpu_data[i][cpu_data[i]['Concurrency'] == concurrency][variable].values
        vals_cpu.append(val[0])
    for i in in_gpu:
        val = gpu_data[i][gpu_data[i]['Concurrency'] == concurrency][variable].values
        vals_gpu.append(val[0])
        
    plt.plot(in_cpu, vals_cpu, label='CPU', marker='o')
    plt.plot(in_gpu, vals_gpu, label='GPU', marker='s')
    plt.xlabel('Number of Instances', loc='right')
    plt.ylabel(f'{ylabel} for {concurrency} concurrent requests', loc='top')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'{args.output_directory}/{save_name}', bbox_inches='tight')

    
def plot_var_vs_instance(data_dict, 
                         variable='Inferences/Second', 
                         ylabel='GPU Throughput (infer/sec)',
                         save_name='instances_vs_throughput_gpu.pdf',
                         ratio=True):
    
    instances = sorted(data_dict.keys())
    concurrencies = data_dict[1]['Concurrency'].values
    
    con_vals = []
    for con in concurrencies:
        vals = []
        for i in instances:
            val = data_dict[i][data_dict[i]['Concurrency'] == con][variable].values
            vals.append(val[0])
        con_vals.append(vals)
    
    if ratio:
        
        ratio_vals = []
        for i in range(1, len(concurrencies)):
            ratio_vals.append([x/y for x, y in zip(con_vals[i], con_vals[0])])
            
        colors = plt.get_cmap('tab10')
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 5.5), sharex=True, gridspec_kw={'height_ratios': [4, 1]})
        
        for i, con in enumerate(concurrencies):
            ax1.plot(instances, con_vals[i], 'o-', color=colors(i), label=f'{con} concurrent requests')
            
        for i, con in enumerate(concurrencies[1:]):
            ax2.plot(instances, ratio_vals[i], 'o-', color=colors(i+1), label=f'{con} concurrent requests')
            
        ax1.set_ylabel(ylabel, loc='top')
        ax1.legend()
        ax1.grid(True, linewidth=0.25)
        
        ax2.set_xlabel('Number of Instances', loc='right')
        ax2.set_ylabel('Ratio')
        ax2.grid(True)
        
        plt.subplots_adjust(hspace=0) 
        plt.savefig(f'{args.output_directory}/{save_name}', bbox_inches='tight')
        
    else:
        plt.figure(figsize=(5, 5))
        for con in concurrencies:
            plt.plot(instances, con_vals[con], 'o-', label=f'{con} concurrent requests')
        plt.xlabel('Number of Instances', loc='right')
        plt.ylabel(ylabel, loc='top')
        plt.legend()
        plt.grid(True)
        
        plt.savefig(f'{args.output_directory}/{save_name}', bbox_inches='tight')
        
def plot_var_vs_concurrency(data_dict, 
                            variable='Inferences/Second', 
                            ylabel='GPU Throughput (infer/sec)',
                            save_name='concurrency_vs_throughput_gpu.pdf',
                            ratio=True,
                            max_concurrency=5):
    
    instances = sorted(data_dict.keys())
    concurrencies = data_dict[1]['Concurrency'].values
    
    if ratio:
        
        ratio_vals = []
        for i in range(1, len(instances)):
            ratio_vals.append([x/y for x, y in zip(data_dict[i][variable].values, data_dict[1][variable].values)])
            
        colors = plt.get_cmap('tab10')
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 5.5), sharex=True, gridspec_kw={'height_ratios': [4, 1]})
        
        for i, instance in enumerate(instances):
            if i < max_concurrency:
                ax1.plot(concurrencies, data_dict[instance][variable].values, 'o-', color=colors(i), label=f'{instance} instances')
            
        for i, instance in enumerate(instances[1:]):
            if i < max_concurrency:
                ax2.plot(concurrencies, ratio_vals[i], 'o-', color=colors(i+1), label=f'{instance} instances')
            
        ax1.set_ylabel(ylabel, loc='top')
        ax1.legend()
        ax1.grid(True, linewidth=0.25)
        
        ax2.set_xlabel('Number of Concurrent Requests', loc='right')
        ax2.set_ylabel('Ratio')
        ax2.grid(True)
        
        plt.subplots_adjust(hspace=0) 
        plt.savefig(f'{args.output_directory}/{save_name}', bbox_inches='tight')
    
    else:  
        plt.figure(figsize=(5, 5))
        for i, instance in enumerate(instances):
            if i < max_concurrency:
                plt.plot(concurrencies, data_dict[instance][variable].values, 'o-', label=f'{instance} instances')
        plt.xlabel('Number of Concurrent Requests', loc='right')
        plt.ylabel(ylabel, loc='top')
        plt.legend()
        plt.grid(True)
        
        plt.savefig(f'{args.output_directory}/{save_name}', bbox_inches='tight')

def main():
    
    cpu_data_instances, gpu_data_instances = process_csv_dir(args.input_directory)
    
    plot_var_vs_instance(gpu_data_instances)
    plot_var_vs_concurrency(gpu_data_instances)
    plot_var_vs_instance(cpu_data_instances, 
                         ylabel='CPU Throughput (infer/sec)',
                         save_name='instances_vs_throughput_cpu.pdf')
    plot_var_vs_concurrency(cpu_data_instances,
                            ylabel='CPU Throughput (infer/sec)',
                            save_name='concurrency_vs_throughput_cpu.pdf')
    plot_var_vs_instance(gpu_data_instances, 
                         variable='Avg latency', 
                         ylabel='GPU Latency (us)',
                         save_name='instances_vs_latency_gpu.pdf')
    plot_var_vs_instance(cpu_data_instances,
                         variable='Avg latency',
                         ylabel='CPU Latency (us)',
                         save_name='instances_vs_latency_cpu.pdf')
    plot_var_vs_instance(gpu_data_instances,
                         variable='total_gpu_usage',
                         ylabel='GPU Utilization (%)',
                         save_name='instances_vs_gpu_utilization.pdf')
    plot_var_vs_instance(gpu_data_instances,
                         variable='max_gpu_memory',
                         ylabel='GPU Memory Usage (GB)',
                         save_name='instances_vs_gpu_memory.pdf')
    plot_var_vs_instance(gpu_data_instances,
                         variable='percent_gpu_memory',
                         ylabel='GPU Memory Usage (%)',
                         save_name='instances_vs_gpu_memory_percent.pdf')
    
    for i in range(1, 6):
        plot_instance_cpu_gpu(cpu_data_instances, gpu_data_instances, concurrency=i,
                            save_name=f'instances_vs_throughput_compare_con{i}.pdf')
        plot_instance_cpu_gpu(cpu_data_instances, gpu_data_instances, 
                            concurrency=4,
                            variable='Avg latency',
                            ylabel='Average Latency (us)',
                            save_name=f'instances_vs_latency_compare_con{i}.pdf')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-directory", 
                        default='data/instances',
                        type=str, help="Input directory path")
    parser.add_argument("-o", "--output-directory", 
                        default='plots',
                        type=str, help="Output directory path")
    args = parser.parse_args()
    
    main()