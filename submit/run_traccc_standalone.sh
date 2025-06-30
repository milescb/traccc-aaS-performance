#!/usr/bin/bash

outdir=${1:-"data/traccc-throughput/"}
nevents=${2:-1}

# fix environment settings
unset LANG
export LC_ALL=C

for i in 20 40 60 80 100 140 200 300
do
    echo "submitting CPU traccc throughput study for mu = $i"
    $INSTALLDIR/bin/traccc_throughput_mt \
        --detector-file=geometries/odd/odd-detray_geometry_detray.json \
        --material-file=geometries/odd/odd-detray_material_detray.json \
        --digitization-file=geometries/odd/odd-digi-geometric-config.json \
        --grid-file=geometries/odd/odd-detray_surface_grids_detray.json \
        --use-detray-detector=1 --use-acts-geom-source=1 --cpu-threads 48 --input-events $nevents \
        --input-directory=$DATADIR/odd-simulations-20240509/geant4_ttbar_mu$i/ \
        &> $outdir/out_cpu_mu$i.log

    echo "submitting GPU traccc throughput study for mu = $i"
    $INSTALLDIR/bin/traccc_throughput_mt_cuda \
        --detector-file=geometries/odd/odd-detray_geometry_detray.json \
        --material-file=geometries/odd/odd-detray_material_detray.json \
        --digitization-file=geometries/odd/odd-digi-geometric-config.json \
        --grid-file=geometries/odd/odd-detray_surface_grids_detray.json \
        --use-detray-detector=1 --use-acts-geom-source=1 --cpu-threads 1 --input-events $nevents \
        --input-directory=$DATADIR/odd-simulations-20240509/geant4_ttbar_mu$i/ \
        &> $outdir/out_gpu_mu$i.log
done

python make_traccc_nom_plots.py --indir=$outdir