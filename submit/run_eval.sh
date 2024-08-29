#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

# salloc --nodes 1 --qos interactive --time 04:00:00 --constraint gpu --gpus=1 --account=m3443 --cpus-per-gpu=10
# shifter --module=gpu --image=docexoty/tritonserver:latest

# "$DIR/run_analyzer.sh" 1 4 "" 200000 "performance/data/initialize_everything" 8

for i in {2..8}
do
    echo ""
    echo "Running with $i model instances"
    echo "-------------------------------"
    echo ""
    "$DIR/run_analyzer.sh" $i 1 "" 200000 "performance/data/initialize_everything"
done