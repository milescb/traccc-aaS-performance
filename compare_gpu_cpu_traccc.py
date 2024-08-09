import os
import re
import matplotlib.pyplot as plt
import argparse

def process_log_file(filepath, is_gpu):
    with open(filepath, 'r') as file:
        content = file.read()
        mu_match = mu_pattern.search(filepath)
        if mu_match:
            mu = int(mu_match.group(1))
            if is_gpu:
                time_match = gpu_time_pattern.search(content)
            else:
                time_match = cpu_time_pattern.search(content)
            if time_match:
                time = float(time_match.group(1))
                key = 'gpu' if is_gpu else 'cpu'
                data[key][mu] = time
            else:
                print(f"Could not find time in {filepath}")
        else:
            print(f"Could not find mu in {filepath}")

def plot_data(data):

    plt.figure(figsize=(5, 5))

    cpu_mu = sorted(data['cpu'].keys())
    cpu_time = [data['cpu'][mu] for mu in cpu_mu]
    plt.plot(cpu_mu, cpu_time, label='AMD EPYC 7763 (48 CPU cores)', marker='o')

    gpu_mu = sorted(data['gpu'].keys())
    gpu_time = [data['gpu'][mu] for mu in gpu_mu]
    
    plt.plot(gpu_mu, gpu_time, label='NVIDIA A100 SXM4 80GB (2 CPU cores)', marker='s')
    plt.xlabel('Average interactions per bunch crossing', loc='right')
    plt.ylabel('Throughput for full-chain (events / sec)', loc='top')
    plt.legend()
    plt.yscale('log')
    plt.grid(True)

    # Show the plot
    plt.savefig(f'{args.log_dir}/mu_vs_throughput.pdf', bbox_inches='tight')

def main():
    
    # Process all log files in the directory
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            if 'gpu' in filename:
                process_log_file(os.path.join(log_dir, filename), is_gpu=True)
            elif 'cpu' in filename:
                process_log_file(os.path.join(log_dir, filename), is_gpu=False)
        else:
            print(f"Skipping {filename}. Not a log file.")
                
    plot_data(data)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--log_dir", 
                        default='data/logs', 
                        type=str, help="Directory containing log files")
    args = parser.parse_args()
    
    log_dir = args.log_dir
    
    # search for relevant lines in log files
    mu_pattern = re.compile(r'mu(\d+)')
    # cpu_time_pattern = re.compile(r'Clusterization\s+(\d+)\s*m')
    # gpu_time_pattern = re.compile(r'Clusterization \(cuda\)\s+(\d+)\s*ms')
    cpu_time_pattern = re.compile(r'Event processing\s+\d+\.\d+\s+ms/event,\s+(\d+\.\d+)\s*events/s')
    gpu_time_pattern = cpu_time_pattern
    
    # initialize data
    data = {'gpu': {}, 'cpu': {}}
    
    main()