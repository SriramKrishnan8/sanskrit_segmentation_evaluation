#!/usr/bin/env python
# coding: utf-8

import os
import sys

import subprocess as sp

import numpy as np

script, data_dir_, res_dir_ = sys.argv

def evaluate(source_dir, model_dir, result_dir):
    """ """
    
    p = sp.Popen(['sh', 'evaluate.sh', source_dir, model_dir, result_dir], stdout=sp.PIPE)
    p.communicate()


data_dir__name = os.path.basename(os.path.dirname(data_dir_))
print(data_dir__name)

fold = os.listdir(data_dir_)

for folder in fold:
    print(folder)
    if 'source' in folder:
        continue
    elif 'alignment' in folder:
        modes = ['morph','word_trans', 'word']
        for mode in modes:
            print(mode)
            model_dir_files = os.listdir(data_dir_+folder+'/'+mode+'/')
            if 'segmented_data_TEST.tsv' not in model_dir_files:
                continue
            
            if "sandhied_data_GOLD.tsv" in model_dir_files:
                source_dir = os.path.join(data_dir_, folder, mode)
            else:
                source_dir = os.path.join(data_dir_, 'source')
            
            model_dir = os.path.join(data_dir_, folder, mode)
            result_dir = os.path.join(res_dir_, data_dir__name, folder, mode)
            evaluate(source_dir, model_dir, result_dir)
        
    else:
        model_dir_files = os.listdir(data_dir_+folder)
        
        if 'segmented_data_TEST.tsv' not in model_dir_files:
            continue
        
        if "sandhied_data_GOLD.tsv" in model_dir_files:
            source_dir = os.path.join(data_dir_, folder)
        else:
            source_dir = os.path.join(data_dir_, 'source')
        
        model_dir = os.path.join(data_dir_, folder)
        result_dir = os.path.join(res_dir_, data_dir__name, folder)
        evaluate(source_dir, model_dir, result_dir)

print("\n")
