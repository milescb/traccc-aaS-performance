# `Traccc` as-a-service Performance Studies

Set of scripts to analyze performance from the output of the `perf_analyzer` tool used to analyze performance of models using the NVIDIA triton server. These scripts are designed to analyze the performance of `traccc` as-a-service in particular. The backend for this and instructions about getting the model can be found [in this git repo](https://github.com/milescb/traccc-aaS). 

## Do everything in one go

The file `submit/run_eval.sh` runs performance studies and makes plots. A full command looks like

```
./submit/run_eval.sh <output_data_dir> <model_name> <bool_multi_gpu>
```

## Create input for `perf_analyzer`

Create input json file with 

```
python generate_json.py -i <input_file> -o <output_file>
```

## Performance Analyzer

Run `perf_analyzer` with the following:

```
perf_analyzer -m traccc-gpu --input-data $DATADIR/../test_data/test_perf_data.json
```

## Performance Plots

### Throughput as a function of concurrency

Run `perf_analyzer` with the CPU and GPU configuration

```
perf_analyzer -m traccc-gpu --input-data $DATADIR/../test_data/test_perf_data.json \
    --concurrency-range <start>:<end>:<step> \
    --verbose-csv --collect-metrics \
    --measurement-interval 10000 \
    -f gpu_1instances.csv 
```

Then, we can make plots with the provide python notebooks. 

### Compare CPU / GPU performance on `traccc` examples

First, make `.log` files containing the output of running the `traccc` examples via (for instance)

```
$INSTALLDIR/bin/traccc_seq_example_cuda \
    --use-detray-detector \
    --detector-file=$DATADIR/tml_detector/trackml-detector.csv \
    --digitization-file=$DATADIR/tml_detector/default-geometric-config-generic.json \
    --input-directory=$DATADIR/tml_full/ttbar_mu100 &> data/logs/gpu_mu100.log
```

then run the following to create the plot:

```
python compare_gpu_cpu_traccc.py
```

## Test k8 server performance

To run `perf_analyzer` on a k8 cluster such as nautilus, follow the instructions on setting up the server in [traccc-aas](https://github.com/milescb/traccc-aaS). Then, forward the following ports:

```
kubectl port-forward service/triton-atlas 8001:8001 -n atlas-sonic
```

and 

```
kubectl port-forward service/triton-atlas 8002:8002 -n atlas-sonic
```

Then, run the performance script:

```
./submit/run_analyzer.sh <outdir> "" "" "" true
```

Finally, make plots with the produced data as before. 

### !! Important !!

Do not forget to uninstall the remote server when done testing:

```
helm uninstall super-sonic -n atlas-sonic
```