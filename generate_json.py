import pandas as pd
import json
import argparse
import glob
import os

def process_event(csv_file_path):
    """Process a single event CSV file and return its data structure."""
    df = pd.read_csv(csv_file_path)
    
    cell_positions_columns = ['geometry_id', 'measurement_id', 'channel0', 'channel1']
    cell_properties_columns = ['timestamp', 'value']
    
    cell_positions = df[cell_positions_columns].astype(int).values.flatten().tolist()
    cell_properties = df[cell_properties_columns].astype(float).values.flatten().tolist()
    return {
        "CELL_POSITIONS": {
            "content": cell_positions,
            "shape": [len(df), 4]
        },
        "CELL_PROPERTIES": {
            "content": cell_properties,
            "shape": [len(df), 2]
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
            process_event(file) 
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
                    default='../client/event000000000-cells.csv',
                    type=str, help="Input CSV file path (first event)")
    parser.add_argument("-o", "--output", 
                    default='data/perf_data_itk.json', 
                    type=str, help="Output JSON file path")
    parser.add_argument("-n", "--num-events", type=int, default=1,
                    help="Number of events to process (default: 1)")
    args = parser.parse_args()

    main()