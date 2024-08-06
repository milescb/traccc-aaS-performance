# `Traccc` as-a-service Performance Studies

Set of scripts to analyze performance from the output of the `perf_analyzer` tool used to analyze performance of models using the NVIDIA triton server. These scripts are designed to analyze the performance of `traccc` as-a-service in particular. The backend for this and instructions about getting the model can be found [in this git repo](https://github.com/milescb/traccc-aaS). 

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

Immediately, one can make plots vs. concurrency with `python plot_concurrency_studies.py`. More interesting are plots as a function of model instances. In order to change the number of instances, edit the config files in the model repository to increase the number of model instances. Then, re-run the above `perf_analyzer` command, changing the name of the output file as `gpu_Xinstances.csv` where `X` is the number of model instances. Perform the same for CPU as well, then make plots via:

```
python plot_model_instance_studies.py -i <input_dir> -o <output_dir>
```

The script `submit/submit_perf_analyzer_jobs.py` performs all the above in one go. To make accurate measurements, spin up a dedicated node with GPUs and run the `submit_perf_analyzer_jobs.py` script. 

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