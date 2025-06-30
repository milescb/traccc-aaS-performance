import pandas as pd
import json
import argparse
import glob
import os

def process_event(csv_file_path, tml_detector=False):
    """Process a single event CSV file and return its data structure."""
    df = pd.read_csv(csv_file_path)
    
    if tml_detector:
        content = df.values.flatten().tolist()
        return {
            "FEATURES": {
                "content": content,
                "shape": [len(df), len(df.columns)]
            }
        }
    else:
        geo_id = df['geometry_id'].tolist()
        cells = df.drop('geometry_id', axis=1).values.flatten().tolist()
        return {
            "GEOMETRY_ID": {
                "content": geo_id,
                "shape": [len(df)]
            },
            "FEATURES": {
                "content": cells,
                "shape": [len(df), len(df.columns)-1]
            }
        }

def main():
    # Get list of event files
    base_path = os.path.dirname(args.input)
    pattern = os.path.join(base_path, "event*-cells.csv")
    event_files = sorted(glob.glob(pattern))[:args.num_events]
    
    if not event_files:
        raise FileNotFoundError(f"No event files found matching pattern: {pattern}")
    
    # Process all events
    json_data = {
        "data": [
            process_event(file, args.tml_detector) 
            for file in event_files
        ]
    }

    # Write the JSON data to a file
    with open(args.output, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    
    print(f"Processed {len(event_files)} events")
    print(f"Output written to: {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", 
                    default='/global/cfs/projectdirs/m3443/data/traccc-aaS/data/tml_pixels/event000000000-cells.csv',
                    type=str, help="Input CSV file path (first event)")
    parser.add_argument("-o", "--output", 
                    default='/global/cfs/projectdirs/m3443/data/traccc-aaS/test_data/perf_data_odd.json', 
                    type=str, help="Output JSON file path")
    parser.add_argument("-tml", "--tml-detector", action='store_true', 
                    help="Flag to indicate if the input data is for TML detector")
    parser.add_argument("-n", "--num-events", type=int, default=1,
                    help="Number of events to process (default: 1)")
    args = parser.parse_args()

    main()