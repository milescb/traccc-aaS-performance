#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

# Function to print help message
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --help, -h           Show this help message"
    echo "  --input-data <file>  Set input data file (default: data/perf_data_odd_mu200.json)"
    echo "  --outdir <dir>       Set output directory (default: data/main_traccc_nom/)"
    echo "  --remote             Enable remote server mode"
    echo ""
    echo "Local server options:"
    echo "  --multi-gpu          Enable multi-GPU mode"
    echo "  --model-repo <name>  Set model repository name (default: models)"
    echo ""
    echo "Remote server options:"
    echo "  --device-name <name> Set device name for plotting (default: NVIDIA A100 SXM4 40GB)"
    echo "  --n-gpus <n>         Set number of GPUs used for plotting (default: 1)"
    echo "  --n-instances <n>    Set number of model instances used for plotting (default: 1)"
    echo
    exit 0
}

# Default values
outdir="data/main_traccc_nom/"
model_repo_name="models"
input_data="data/perf_data_odd_mu200.json"
multi_gpu=false
remote_server=false
device_name="NVIDIA-A100-SXM4-40GB"
n_gpus=1
n_instances=1

# Parse flags
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_help
            ;;
        --multi-gpu)
            multi_gpu=true
            shift
            ;;
        --remote)
            remote_server=true
            shift
            ;;
        --outdir)
            outdir="$2"
            shift 2
            ;;
        --model-repo)
            model_repo_name="$2"
            shift 2
            ;;
        --input-data)
            input_data="$2"
            shift 2
            ;;
        --device-name)
            device_name="$2"
            shift 2
            ;;
        --n-gpus)
            n_gpus="$2"
            shift 2
            ;;
        --n-instances)
            n_instances="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help or -h for usage information"
            exit 1
            ;;
    esac
done

if [ "$remote_server" == "true" ]; then
    echo "Running on remote server"
    echo "------------------------"
    echo ""
    echo "Please make sure that the remote server is deployed and running"
    echo ""

    "$DIR/run_remote_analyzer.sh" $outdir $input_data $n_gpus $n_instances 10000 1 10 1

    echo "Making plots..."
    python3 "$DIR/../make_remote_deploy_plots.py" --indir=$outdir --outdir=$outdir \
        --infile="${n_gpus}gpus_${n_instance_per_gpu}instance.csv" --device=$device_name --n-GPUs=$n_gpus --n-instances=$n_instances
else
    echo "Running on local server"
    echo ""

    for i in {1..8}
    do
        echo ""
        echo "Running with $i model instances"
        echo "-------------------------------"
        echo ""
        "$DIR/run_analyzer.sh" $i 1 "" 10000 $outdir $i $i 1 $model_repo_name $input_data $remote_server
    done

    # plot
    python3 "$DIR/../make_single_gpu_plots.py" --indir=$outdir --outdir=$outdir

    if [ "$multi_gpu" == "true" ]; then
        echo ""
        echo "Running with 1 model instance on 4 GPUs"
        echo "---------------------------------------"
        echo ""
        "$DIR/run_analyzer.sh" 1 4 "" 10000 $outdir 1 8 1 $model_repo_name $input_data $remote_server
        "$DIR/run_analyzer.sh" 1 1 "" 10000 $outdir 1 8 1 $model_repo_name $input_data $remote_server

        python3 "$DIR/../make_multi_gpu_plots.py" --indir=$outdir --outdir=$outdir --n-instances 1
    fi

fi