#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

# Function to print help message
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --help, -h          Show this help message"
    echo "  --multi-gpu         Enable multi-GPU mode for running on 4 GPUs"
    echo "  --remote            Enable remote server mode"
    echo "  --outdir <dir>      Set output directory (default: data/main_traccc_nom/)"
    echo "  --model-repo <name> Set model repository name (default: models)"
    echo "  --input-data <file> Set input data file (default: data/perf_data_odd_mu200.json)"
    echo
    exit 0
}

# Default values
outdir="data/main_traccc_nom/"
model_repo_name="models"
input_data="data/perf_data_odd_mu200.json"
multi_gpu=false
remote_server=false

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
        *)
            echo "Unknown option: $1"
            echo "Use --help or -h for usage information"
            exit 1
            ;;
    esac
done

for i in {1..8}
do
    echo ""
    echo "Running with $i model instances"
    echo "-------------------------------"
    echo ""
    "$DIR/submit/run_analyzer.sh" $i 1 "" 100000 $outdir $i $i 1 $model_repo_name $input_data $remote_server
done

# plot
python3 "$DIR/make_single_gpu_plots.py" --indir=$outdir --outdir=$outdir

if [ "$multi_gpu" == "true" ]; then
    echo ""
    echo "Running with 1 model instance on 4 GPUs"
    echo "---------------------------------------"
    echo ""
    "$DIR/run_analyzer.sh" 1 4 "" 100000 $outdir 1 8 1 $model_repo_name $input_data $remote_server
    "$DIR/run_analyzer.sh" 1 1 "" 100000 $outdir 1 8 1 $model_repo_name $input_data $remote_server

    python3 "$DIR/make_multi_gpu_plots.py" --indir=$outdir --outdir=$outdir --n-instances 1
fi