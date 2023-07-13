#!/usr/bin/env bash

SOURCE=$1
MODEL=$2
OBS=$3

mkdir -p $OBS/with_cpd $OBS/without_cpd

WITH_CPD=$OBS/with_cpd
WITHOUT_CPD=$OBS/without_cpd

python3 sent_eval.py $SOURCE/sandhied_data_GOLD.tsv $MODEL/segmented_data_TEST.tsv $WITH_CPD/solution.tsv $WITH_CPD/missed.tsv $WITH_CPD/wrong.tsv $WITH_CPD/all_sol.tsv $WITH_CPD/sol_num.tsv "t"

cut -f3,4 -d'	' $WITH_CPD/all_sol.tsv > $WITH_CPD/result.tsv

python3 sent_eval.py $SOURCE/sandhied_data_GOLD.tsv $MODEL/segmented_data_TEST.tsv $WITHOUT_CPD/solution.tsv $WITHOUT_CPD/missed.tsv $WITHOUT_CPD/wrong.tsv $WITHOUT_CPD/all_sol.tsv $WITHOUT_CPD/sol_num.tsv "f"

cut -f3,4 -d'	' $WITHOUT_CPD/all_sol.tsv > $WITHOUT_CPD/result.tsv
