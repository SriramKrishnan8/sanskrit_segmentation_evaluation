#!/usr/bin/env python3

import os
import sys

from collections import Counter
import re
import numpy as np
import json

script, gold, test, res = sys.argv


def score(sol, pred):
    """ Precision, Recall and Fscore for each solution """
    
    numerator = len(list((Counter(sol) & Counter(pred)).elements()))
    rec = numerator / len(sol)
    prec = numerator / len(pred)
    f1 = 2*prec*rec/(prec + rec) if (not ((prec + rec) == 0)) else 0.0
    return (rec, prec, f1)
    

def scoring_without_cpds(gold_seg_sols, test_seg_sol):
    """ Scores the recall, precision and f1 score and considers only
        word segmentation
    """
    
    results_tuple = []
    
    test_preds = re.split(r' |-', test_seg_sol)
    
    for gold_seg in gold_seg_sols:
        gold_sols = re.split(r' |-', gold_seg)
        result = score(gold_sols, test_preds)
        results_tuple.append(result)
    
    (rec, prec, f1) = max(results_tuple, key=lambda x:x[2])
    
    return (rec, prec, f1)
    

#def scoring_with_cpds(gold_seg_sols, test_seg_sol):
#    """ Scores the recall, precision and f1 score and considers both
#        word segmentation and compound segmentation
#    """
#    
#    pada_results_tuple = []
#    comp_results_tuple = []
#    
#    test_preds = test_seg_sol.split(" ")
#    test_padas = []
#    test_comps = []
#    for test_word in test_preds:
#        if "-" in test_words:
#            test_comps.append(test_word.split("-"))
#        else:
#            test_padas.append(test_word)
#    
#    for gold_seg in gold_seg_sols:
#        gold_sols = gold_seg.split(" ")
#        padas = []
#        comps = []
#        for gold_word in gold_sols:
#            if "-" in gold_word:
#                comps.append(gold_word.split("-"))
#            else:
#                padas.append(gold_word)
#                
#        pada_result = score(gold_sols, test_preds)
#        pada_results_tuple.append(pada_result)
#        
#        comp_rec = []
#        comp_prec = []
#        comp_f1 = []
#        for comp in comps:
#            for test_comp in test_comps:
#                
#    
#    (recall, precision, f1_score) = max(results_tuple, key=lambda x:x[2])
#    
#    return (recall, precision, f1_score)
    

def scoring_perfect_match(gold_seg_sols, test_seg_sols):
    """ Scores the perfect match and position """
    
    position = 0
    perfect_match = False
    for test_seg_sol in test_seg_sols:
        position += 1
        
        if test_seg_sol in gold_seg_sols:
            perfect_match = True
            break
    
    (pm, pos) = (1.0, position) if perfect_match else (0.0, 0)
    
    return (pm, pos)


def compare_results(gold_value, test_value, with_compounds=False):
    """ Comparing the test values with the possible gold values and
        generating the precision, recall, f1_score and position
    """
    
    rec = 0.0
    prec = 0.0
    f1 = 0.0
    
    gold_seg_sols = gold_value.get("segmented_sentences", [])
    test_seg_sols = test_value.get("segmented_sentences", [])
    
    (pm_c, pos_c) = scoring_perfect_match(gold_seg_sols, test_seg_sols)
    
    gold_seg_sols = [seg.replace("-", " ") for seg in gold_seg_sols]
    test_seg_sols = [seg.replace("-", " ") for seg in test_seg_sols]
    
#    gold_seg_sols = [seg for seg in gold_value.get("segmented_sentences", [])]
#    test_seg_sols = [seg for seg in test_value.get("segmented_sentences", [])]
    
    (pm_nc, pos_nc) = scoring_perfect_match(gold_seg_sols, test_seg_sols)
    
#    scoring_fn = scoring_with_cpds if with_compounds else scoring_without_cpds
    
    (rec, prec, f1) = scoring_without_cpds(gold_seg_sols, test_seg_sols[0])
    
    return (rec, prec, f1, pm_c, pos_c, pm_nc, pos_nc)
    
    
def evaluate(gold_dict, test_dict):
    """
    Returns the macro averaged - precision, recall, f1_score, position
    and position counter - as a dict
    """
    
    precisions = []
    recalls = []
    f1_scores = []
    perfect_matches_with_cpd = []
    perfect_matches_without_cpd = []
    positions_with_cpd = []
    positions_without_cpd = []
    
    for key in gold_dict.keys():
        if key not in test_dict.keys():
            (rec, prec, f1, pm_c, pos_c, pm_nc, pos_nc) = (0.0,0.0,0.0,0.0,0.0,0.0,0.0)
        else:
            gold_val = gold_dict.get(key)
            test_val = test_dict.get(key)
            (rec, prec, f1, pm_c, pos_c, pm_nc, pos_nc) = compare_results(gold_val, test_val)
    
        precisions.append(prec)
        recalls.append(rec)
        f1_scores.append(f1)
        perfect_matches_with_cpd.append(pm_c)
        perfect_matches_without_cpd.append(pm_nc)
        positions_with_cpd.append(pos_c)
        positions_without_cpd.append(pos_nc)

    avg_prec = np.mean(precisions)*100.0
    avg_recall = np.mean(recalls)*100.0
    avg_f1_score = np.mean(f1_scores)*100.0
    avg_perfect_matches_with_cpd = np.mean(perfect_matches_with_cpd)*100.0
    avg_perfect_matches_without_cpd = np.mean(perfect_matches_without_cpd)*100.0
    avg_positions_with_cpd = np.mean(positions_with_cpd)%100.0
    avg_positions_without_cpd = np.mean(positions_without_cpd)%100.0
    positions_counter_with_cpd = dict(Counter(positions_with_cpd).most_common())
    positions_counter_without_cpd = dict(Counter(positions_without_cpd).most_common())
    
    scores = {
        'precision': avg_prec,
        'recall': avg_recall,
        'f1score': avg_f1_score,
        'perfect_match_with_cpd': avg_perfect_matches_with_cpd,
        'position_with_cpd': avg_positions_with_cpd,
        'position_counter_with_cpd': positions_counter_with_cpd,
        'perfect_match_without_cpd': avg_perfect_matches_without_cpd,
        'position_without_cpd': avg_positions_without_cpd,
        'position_counter_without_cpd': positions_counter_without_cpd
    }
    
    print('Scores:')
    print(scores)
    
    return scores
    

def saH_eRaH(text):
    """ Systems like SH produce forms sa and eRa as it is.  
        These are converted to saH and eRaH in the segmentation
        solutions.
    """
    
    updated_text = re.sub(r'^sa\ ', 'saH ', text)
    updated_text = updated_text.replace(';sa ', ';saH ')
    updated_text = updated_text.replace(' sa ', ' saH ')
    updated_text = updated_text.replace(r'^eRa ', 'eRaH ')
    updated_text = updated_text.replace(';eRa ', ';eRaH ')
    updated_text = updated_text.replace(' eRa ', ' eRaH ')
    
    return updated_text
    

def marks(text):
    """
    """
    
    updated_text = re.sub(r'(\||!|=)', '', text)
    
    return updated_text


def get_dict(text, update_sa=False, handle_marks=True):
    """ To obtain the gold segmentation in a format suitable for 
        evaluation
    """
    
    lines = list(filter(None, text.split("\n")))
    
    dict_ = {}
    
    for sent_item in lines:
        split_sent_item = sent_item.split("\t")
        sent_id = split_sent_item[0]
        joint_sentence = split_sent_item[1]
        seg_sents = split_sent_item[2] if (len(split_sent_item) == 3) else ""
        if seg_sents == "":
            continue
        segmented_sentences = saH_eRaH(seg_sents) if update_sa else seg_sents
        segmented_sentences = marks(segmented_sentences) if handle_marks else segmented_sentences
        segmented_sentence_lst = segmented_sentences.split(";")
#        seg_sols = []
#        for sol in segmented_sentence_lst:
#            words = sol.split(" ")
#            word_count = Counter(words)
#            word_count_dict = dict(word_count.most_common())
#            seg_sols.append(word_count_dict)
        
        item_dict = {}
        item_dict["joint_sentence"] = joint_sentence
        item_dict["segmented_sentences"] = segmented_sentence_lst
#        item_dict["segmentation_solutions"] = seg_sols
        dict_[sent_id] = item_dict
    
    return dict_


def main():
    gold_file = open(gold, 'r')
    gold_text = gold_file.read()
    gold_file.close()
    gold_dict = get_dict(gold_text)
    
    test_file = open(test, 'r')
    test_text = test_file.read()
    test_file.close()
    test_dict = get_dict(test_text, update_sa=True, handle_marks=True)
    
    updated_gold_dict = gold_dict
    updated_gold_dict = {}
    test_keys = test_dict.keys()
    for key in gold_dict.keys():
        if key in test_keys:
            updated_gold_dict[key] = gold_dict[key]
    
    scores = evaluate(updated_gold_dict, test_dict)
    
    with open(res, 'w') as f:
        json.dump(scores, f)
    

if __name__ == "__main__":
    main()
