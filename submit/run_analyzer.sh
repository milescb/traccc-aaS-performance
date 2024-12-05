# Description: This script is used to run the perf_analyzer tool for the traccc-aaS model.

# Author: Haoran Zhao
# Edits: Miles Cochran-Branson
# Date: 2024-07-19

#!/bin/bash
uname -a

# Default configurations
n_instance_per_gpu=${1:-1}
n_gpus=${2:-1}
output_csv_name=${3:-"perf_analyzer"}
_measurement_interval=${4:-50000}
output_dir=${5:-"performance/data/main_traccc_nom"}  # Default to the specified directory
concurrency_start=${6:-1}
concurrency_end=${7:-8}
concurrency_step=${8:-1}
model_repo_name=${9:-"models"}
input_data=${10:-"performance/data/dummy_data.json"}
remote_server=${11:-"false"}  # Default to false
max_attempts=5  # Maximum attempts to generate the file

# Display help information
help_function() {
    echo "Usage: $0 [n_instance_per_gpu] [n_gpus] [output_csv_name] [measurement_interval] [output_dir] [concurrency_end] [concurrency_step]"
    echo ""
    echo "n_instance_per_gpu:     Number of instances per GPU (default: 1)"
    echo "n_gpus:                 Number of GPUs (default: 1)"
    echo "output_csv_name:        Base name for the output CSV files (default: 'perf_analyzer')"
    echo "measurement_interval:   Initial measurement interval in milliseconds (default: 120000)"
    echo "output_dir:             Directory to store the output CSV files (default: '/workspace/evaluate/slurm/')"
    echo "concurrency_end:        End value for concurrency range (default: 16)"
    echo "concurrency_step:       Step value for concurrency range (default: 1)"
}

# If help is requested, display help and exit
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    help_function
    exit 0
fi

export INSTALLDIR=/global/cfs/projectdirs/m3443/data/traccc-aaS/software/prod/ver_09152024/install
export PATH=$INSTALLDIR/bin:$PATH
export LD_LIBRARY_PATH=$INSTALLDIR/lib:$LD_LIBRARY_PATH

# Update model repository configuration
output_dir=$output_dir/${n_instance_per_gpu}insts_${n_gpus}gpus/ # avoid conflict of difference instance config

mkdir -p $output_dir
cp -r $INSTALLDIR/$model_repo_name $output_dir/
# sed -i "s/count: 1/count: ${n_instance_per_gpu}/" $output_dir/${model_repo_name}/traccc-cpu/config.pbtxt
sed -i "s/count: 1/count: ${n_instance_per_gpu}/" $output_dir/${model_repo_name}/traccc-gpu/config.pbtxt

gpus_array=$(seq 0 $((n_gpus - 1)) | tr '\n' ',' | sed 's/,$//')
sed -i "/gpus:/c\    gpus: [ $gpus_array ]" $output_dir/${model_repo_name}/traccc-gpu/config.pbtxt

check_server_ready() {
    local max_retries=100
    local retry_interval=20  # wait 10 seconds before re-trying
    local retry_count=0
    local server_ready=0  # 0 means not ready, 1 means ready

    echo "Checking if server is ready..."

    while [[ $retry_count -lt $max_retries && $server_ready -eq 0 ]]; do
        # Use curl to check the server's status. The -s flag silences curl's output, and -o /dev/null discards the actual content.
        local response=$(curl -s -o /dev/null -w "%{http_code}" localhost:8000/v2/health/ready)
        echo "Response: $response"
        if [[ "$response" == "200" ]]; then
            server_ready=1
            echo "Server is ready!"
            echo ""
        else
            echo "Server not ready, retrying in $retry_interval seconds..."
            echo ""
            retry_count=$((retry_count + 1))
            sleep $retry_interval
        fi
    done

    if [[ $server_ready -eq 0 ]]; then
        echo "Server didn't become ready after $max_retries attempts. Exiting..."
        exit 1
    fi
}


if [[ "$remote_server" == "true" ]]; then
    echo "Remote server is set to true. Skipping server launch..."
    echo "Please ensure that the server is already running on the remote machine."
elif [[ "$remote_server" == "false" ]]; then
    echo "Remote server is set to false. Launching server..."
    log_filename="${output_dir}/${n_instance_per_gpu}insts_${n_gpus}gpus.log"
    nohup tritonserver --model-repository=$output_dir/models/ > ${log_filename} 2>&1 &
    server_pid=$!
    sleep 20

    # Set a trap to ensure tritonserver is always killed on exit
    trap 'echo "Killing triton server..."; kill "$server_pid"' EXIT
else
    echo "Invalid value for remote_server. Please set it to either 'true' or 'false'."
    exit 1s
fi


# Set a trap to ensure tritonserver is always killed on exit
trap 'echo "Killing triton server..."; kill "$server_pid"' EXIT

# Check server's readiness
check_server_ready

# Check for .csv files in the target directory and delete them
find "$output_dir" -type f -name "*.csv" -exec rm -f {} \;

# Function to run perf_analyzer
run_perf_analyzer() {
    local mode=$1  # sync or async
    local processor=$2 # cpu or gpu
    local output_csv="${output_dir}/${processor}_${n_instance_per_gpu}instance_${mode}.csv"
    local attempt=0
    local measurement_interval=${_measurement_interval}
    local mode_flag=""
    # local concurrency_range=$(( (3 * n_instance_per_gpu * n_gpus / 2) + 2 ))  # Multiply by 1.5 using integer arithmetic and + 1
    # local concurrency_range=16
    local concurrency_range=${concurrency_end}
    local concurrency_step=${concurrency_step}
    local concurrency_start=${concurrency_start}
    echo "Concurrency Range: $concurrency_start:$concurrency_range:$concurrency_step"


    # Set the mode flag based on sync or async
    if [[ "$mode" == "sync" ]]; then
        mode_flag="--sync"
    elif [[ "$mode" == "async" ]]; then
        mode_flag="--async"
    fi

    while [[ ! -f ${output_csv} && $attempt -lt $max_attempts ]]; do
        echo "Running perf_analyzer (${mode}) with measurement_interval: $measurement_interval..."
        perf_analyzer -m traccc-$processor --percentile=95 -i grpc --input-data $input_data \
        --measurement-interval ${measurement_interval} $mode_flag \
        --concurrency-range $concurrency_start:$concurrency_range:$concurrency_step -v \
        -f ${output_csv} -b 1 --collect-metrics --verbose-csv # --metrics-interval 10000

        # If the file isn't generated, double the measurement_interval and retry
        if [[ ! -f ${output_csv} ]]; then
            echo ""
            echo "File not generated. Doubling the measurement_interval and retrying..."
            echo ""
            measurement_interval=$((measurement_interval * 2))
            attempt=$((attempt + 1))
        fi
    done

    # Check if file was not created after all attempts
    if [[ ! -f ${output_csv} ]]; then
        echo "Failed to generate the file ${output_csv} after $max_attempts attempts."
        exit 1
    fi
}

echo "Warm up"
perf_analyzer -m traccc-gpu --percentile=95 -i grpc \
    --input-data $input_data \
    --concurrency 2:4:1 --measurement-interval 10000

echo "Warm up done"

# Run the perf_analyzer for both sync and async modes
echo ""
echo "Running perf_analyzer for the sync mode with GPU"
run_perf_analyzer "sync" "gpu"
echo "Sync mode GPU done"

# echo ""
# echo "Running perf_analyzer for the sync mode with CPU"
# run_perf_analyzer "sync" "cpu"
# echo "Sync mode CPU done"

# echo ""
# echo "Running perf_analyzer for the async mode"
# run_perf_analyzer "async"
# echo "the async mode is done"

echo "All Done!"