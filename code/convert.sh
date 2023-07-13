#!/usr/bin/env bash

input=$1
gold=$2
pred=$3

COUNT=$(wc -l < $input)
seq 1 $COUNT > ids.tsv
paste ids.tsv $input $gold > sandhied_data_GOLD.tsv
paste ids.tsv $input $pred > segmented_data_TEST.tsv

rm ids.tsv
