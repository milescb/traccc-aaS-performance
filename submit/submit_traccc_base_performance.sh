#!/usr/bin/bash

for i in 20 40 60 80 100 140 200 300
do
    echo "submitting CPU traccc throughput study for mu = $i"
    $INSTALLDIR/bin/traccc_throughput_mt \
        --detector-file=geometries/odd/odd-detray_geometry_detray.json \
        --digitization-file=geometries/odd/odd-digi-geometric-config.json \
        --grid-file=geometries/odd/odd-detray_surface_grids_detray.json \
        --use-detray-detector --cpu-threads 48 --input-events 10 \
        --input-directory=$DATADIR/../data_odd_ttbar_large/geant4_ttbar_mu$i/ \
        &> data/logs_odd_main_throughput_10events/out_cpu_mu$i.log

    echo "submitting GPU traccc throughput study for mu = $i"
    $INSTALLDIR/bin/traccc_throughput_mt_cuda \
        --detector-file=geometries/odd/odd-detray_geometry_detray.json \
        --digitization-file=geometries/odd/odd-digi-geometric-config.json \
        --grid-file=geometries/odd/odd-detray_surface_grids_detray.json \
        --use-detray-detector --cpu-threads 2 --input-events 10 \
        --input-directory=$DATADIR/../data_odd_ttbar_large/geant4_ttbar_mu$i/ \
        &> data/logs_odd_main_throughput_10events/out_gpu_mu$i.log
done