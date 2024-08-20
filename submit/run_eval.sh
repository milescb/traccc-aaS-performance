#!/bin/bash

DIR="$(dirname "${BASH_SOURCE[0]}")"

for i in {1..5}
do
  "$DIR/evaluate_triton.sh" $i
done