#!/usr/bin/env bash

SOURCE=$1
MODEL=$2
OBS=$3

python3 word_eval.py $SOURCE/sandhied_data_GOLD.tsv $MODEL/segmented_data_TEST.tsv $OBS/results.json
