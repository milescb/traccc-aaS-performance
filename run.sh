#!/bin/bash

n_events=${1:-10}
compare_nominal=${2:-true}

if [[ $compare_nominal == "true" ]]; then
    echo "Running standalone traccc"
    mkdir -p "data/traccc-aaS_standalone/"
    bash submit/run_traccc_standalone.sh \
        "data/traccc-aaS_standalone/" \
        $n_events
fi

echo "Running as-a-Service"

for mu in 20 40 60 80 100 140 200 300; do
    echo "Processing mu = ${mu}"
    
    # Generate JSON file with ten events for every mu
    python generate_json.py \
        -n $n_events \
        -i "$DATADIR/odd-simulations-20240509/geant4_ttbar_mu${mu}/" \
        -o "data/perf_data_odd_mu${mu}_${n_events}event.json"
    echo "Generated data/perf_data_odd_mu${mu}_${n_events}event.json"

    # Create output directory
    mkdir -p "data/traccc-aaS_nominal_mu${mu}_${n_events}event"
    
    # Run evaluation
    bash submit/run_eval.sh \
        --outdir data/traccc-aaS_nominal_mu${mu}_${n_events}event/ \
        --model-repo models \
        --input-data data/perf_data_odd_mu${mu}_${n_events}event.json

    echo "Evaluation completed for mu = ${mu}"

    # Generate plots
    python make_single_gpu_plots.py \
        --indir "data/traccc-aaS_nominal_mu${mu}_${n_events}event/" \
        --title "ODD detector, μ = ${mu}, traccc v0.23.0"
done

if [[ $compare_nominal == "true" ]]; then
    python make_aaS_vs_standalone_plots.py \
        --indir "data/" \
        --standalone-indir "data/traccc-aaS_standalone/" \
        --title "1 NVIDIA A100 SXM4 80GB on Perlmutter, ODD detector, traccc v0.23.0"
fi
