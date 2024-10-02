#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

# salloc --nodes 1 --qos interactive --time 04:00:00 --constraint gpu --gpus=1 --account=m3443 --cpus-per-gpu=10
# shifter --module=gpu --image=docexoty/tritonserver:latest

outdir=${1:-"performance/data/main_traccc"}
model_name=${2:-"models"}
multi_gpu=${3:-"false"} # or set to true

for i in {1..8}
do
    echo ""
    echo "Running with $i model instances"
    echo "-------------------------------"
    echo ""
    "$DIR/run_analyzer.sh" $i 1 "" 100000 $ourdir $i $i 1 $model_name
done

# plot
python3 "$DIR/../make_single_gpu_plots.py" --indir=$outdir --outdir=$outdir

if [ "$multi_gpu" == "true" ]; then
    echo ""
    echo "Running with 1 model instance on 4 GPUs"
    echo "---------------------------------------"
    echo ""
    "$DIR/run_analyzer.sh" 4 1 "" 100000 $outdir 1 8 1 $model_name
    "$DIR/run_analyzer.sh" 1 1 "" 100000 $outdir 1 8 1 $model_name

    python3 "$DIR/../make_multi_gpu_plots.py" --indir=$outdir --outdir=$outdir --n-instances 1
fi