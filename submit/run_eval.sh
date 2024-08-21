#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

for i in {6..8}
do
  "$DIR/run_analyzer.sh" $i
done