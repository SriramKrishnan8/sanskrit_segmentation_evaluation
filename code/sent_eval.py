#!/usr/bin/env python3

import os
import sys

import collections
import re

script, gold, test, solution, missed, wrong, all_sol, sol_num, with_cpd = sys.argv

def get_text(data_file):
    """ """
    
    dict_ = {}
    input_text_list = []
    all_data = data_file.read()
    lines = list(filter(None, all_data.split("\n")))
    
    for item in lines:
        split_item = item.split("\t")
        id_ = split_item[0]
        joint_sent = split_item[1]
        seg_sent = split_item[2] if (len(split_item) == 3) else ""
        
        item_dict = {}
        item_dict["joint_sent"] = joint_sent
        item_dict["seg_sent"] = seg_sent
        dict_[id_] = item_dict
    
    return dict_
    

def handle_sa(text):
    """ """
    
    updated_text = re.sub(r'^sa ', 'saH ', text)
    updated_text = re.sub(r';sa ', ';saH ', updated_text)
    updated_text = re.sub(r' sa ', ' saH ', updated_text)
    updated_text = re.sub(r'^eRa ', 'eRaH ', updated_text)
    updated_text = re.sub(r';eRa ', ';eRaH ', updated_text)
    updated_text = re.sub(r' eRa ', ' eRaH ', updated_text)
    
    return updated_text


def assign_freq(lst_):
    """ """
    
    ctr = collections.Counter(lst_)
    items_lst = [ (str(k), str(v)) for k, v in ctr.items() if k]
    
    return items_lst


def write_to_file(lst_, file_name):
    """ """
    
    file_ = open(file_name, 'w', encoding="utf-8")
    joined_lst = ["\t".join(item) for item in lst_]
    file_.write("\n".join(joined_lst))


def main():
    """ """
    
    gold_file = open(gold, 'r')
    gold_input_text_dict = get_text(gold_file)
    
    test_file = open(test, 'r')
    test_input_text_dict = get_text(test_file)
    
    missed_lst = []
    all_sol_lst = []
    sol_lst = []
    wrong_lst = []
    sol_num_lst = []
    
    for input_key in gold_input_text_dict.keys():
        gold_item = gold_input_text_dict[input_key]
        
        if input_key not in test_input_text_dict.keys():
            missed_lst.append((str(input_key), gold_item["joint_sent"]))
            all_sol_lst.append((str(input_key), gold_item["joint_sent"], "MISSED", "-1"))
            sol_num_lst.append("-1")
            continue
        
        test_item = test_input_text_dict[input_key]
        
        gold_seg = gold_item["seg_sent"]
        test_seg = test_item["seg_sent"]
        
        if not test_seg:
            missed_lst.append((str(input_key), gold_item["joint_sent"]))
            all_sol_lst.append((str(input_key), gold_item["joint_sent"], "MISSED", "-1"))
            sol_num_lst.append("-1")
            continue
        
        test_seg_updated = handle_sa(test_seg)
        
        if with_cpd == "f":
            test_seg_updated = test_seg_updated.replace("-", " ")
            gold_seg = gold_seg.replace("-", " ")
        
        gold_seg_sols = gold_seg.split(";")
        test_seg_sols = test_seg_updated.split(";")
        
        found = False
        for i in range(len(test_seg_sols)):
            if test_seg_sols[i] in gold_seg_sols:
                found = True
                sol_lst.append((str(input_key), gold_item["joint_sent"], str(i + 1)))
                all_sol_lst.append((str(input_key), gold_item["joint_sent"], "FOUND", str(i + 1)))
                sol_num_lst.append(str(i + 1))
                break
        
        if not found:
            wrong_lst.append((str(input_key), gold_item["seg_sent"], test_item["seg_sent"]))
            all_sol_lst.append((str(input_key), gold_item["joint_sent"], "WRONG", "0"))
            sol_num_lst.append("0")
    
    write_to_file(missed_lst, missed)
    write_to_file(all_sol_lst, all_sol)
    write_to_file(sol_lst, solution)
    write_to_file(wrong_lst, wrong)
    write_to_file(assign_freq(sol_num_lst), sol_num)
                
                
if __name__ == "__main__":
    main()
