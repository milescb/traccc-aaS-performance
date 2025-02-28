
output_dir=${1-"data/main_traccc_nom/"}
input_data=${2-"data/perf_data_odd_mu200.json"}
_n_gpus=${3-1}
n_instance_per_gpu=${4-1}
_measurement_interval=${5-10000}
concurrency_start=${6-1}
concurrency_end=${7-10}
concurrency_step=${8-1}
_metrics_url=${9-"http://localhost:8003/metrics"}
max_attempts=${10-3}

# # Start port forwarding
# kubectl port-forward service/traccc-sonic 8001:8001 -n traccc & PID1=$!
# kubectl port-forward svc/traccc-sonic-metrics-collector 8003:8003 -n traccc & PID2=$!

# # Add cleanup trap
# cleanup() {
#     echo "Cleaning up port forwarding..."
#     kill $PID1 $PID2 2>/dev/null
# }
# trap cleanup EXIT

# Function to run perf_analyzer
run_perf_analyzer() {
    local n_gpus=${_n_gpus}
    local metrics_url=${_metrics_url}
    local output_csv="${output_dir}/${n_gpus}gpus_${n_instance_per_gpu}instance"
    local attempt=0
    local measurement_interval=${_measurement_interval}
    local mode_flag=""
    local concurrency_range=${concurrency_end}
    local concurrency_step=${concurrency_step}
    local concurrency_start=${concurrency_start}
    echo "Concurrency Range: $concurrency_start:$concurrency_range:$concurrency_step"

    while [[ ! -f ${output_csv} && $attempt -lt $max_attempts ]]; do
        echo "Running perf_analyzer (${mode}) with measurement_interval: $measurement_interval..."
        perf_analyzer -m traccc-gpu -i grpc --input-data $input_data \
        --measurement-interval ${measurement_interval} -r 30 \
        --concurrency-range $concurrency_start:$concurrency_range:$concurrency_step \
        --metrics-url ${_metrics_url}\
        -f ${output_csv}".csv" -b 1 --collect-metrics --verbose-csv > ${output_csv}".log"

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
    if [[ ! -f ${output_csv}".csv" ]]; then
        echo "Failed to generate the file ${output_csv} after $max_attempts attempts."
        exit 1
    fi
}


echo "Warm up"
perf_analyzer -m traccc-gpu -i grpc \
    --input-data $input_data \
    --concurrency 2:3:1 --measurement-interval 10000

echo "Warm up done"

# Collect data
echo ""
echo "Running perf_analyzer for the sync mode with GPU"
run_perf_analyzer
echo "Sync mode GPU done"