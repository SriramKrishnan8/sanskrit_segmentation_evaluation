#!/usr/bin/env bash

#python3 run_all.py ../data/bhagavad_gita/
#python3 run_all.py ../data/hackathon_test/
#python3 run_all.py ../data/meghaduta/
#python3 run_all.py ../data/rcnn_test_full/
#python3 run_all.py ../data/rcnn_test_sample/
#python3 run_all.py ../data/sankshepa_ramayanam/
#python3 run_all.py ../data/sighum_test/

for d in ../data/*; do
    python3 run_all.py $d/ ../res/
done
