# sanskrit_segmentation_evaluation

Evaluation of Sanskrit Segmentation Predictions. Presently contains the evaluation code and results of various latest models on specific test sets. There are two evaluation strategies: sentence-based and word-based.

In sentence-based evaluation (available at ```./code/sent_eval.sh```), the entire sentence is taken into account for comparing the predictions with the gold. This is useful for understanding where the segmentation results deviate from the ground truth.

In word-based evaluation (available at ```./code/word_eval.sh```), the macro-averaged precision, recall, f_score, perfect_match and solution_distribution are calculate with a counter-based comparison over the words in the predictions.

In both the cases, the evaluation is done by both considering the compound word predictions and ignoring them.

## Input

The gold and predictions are to be presented as *sandhied_data_GOLD.tsv* and *segmented_data_TEST.tsv*, respectively. *sandhied_data_GOLD.tsv* should have three columns: (id, unsegmented sentence, possible gold segmentation solutions separated by ";"). *segmented_data_TEST.tsv* should have three columns: (id, unsegmented sentence, possible predicted segmentation solutions separated by ";").

In case the input, gold and predictions are present in three different files, then these can be fed to ```./code/convert.sh``` as follows:

```
cd code/
sh convert.sh input.txt gold.txt pred.txt
```

This will generate the *sandhied_data_GOLD.tsv* and *segmented_data_TEST.tsv*.

## Sentence Evaluation

The sentence-based evaluation can be directly run as:

```
cd code/
sh sent_eval.sh sandhied_dir segmented_dir results_dir
```

The results are recorded onto .tsv files (solution, sol_num, missed, wrong, etc) in the specified results_dir

## Word Evaluation

The sentence-based evaluation can be directly run as:

```
cd code/
sh word_eval.sh sandhied_dir segmented_dir results_dir
```

The results (macro-averaged precision, recall, perfect_match, solution_distribution) are recorded onto result.json in the specified results_dir. The solution distribution is useful for segmenters which rank the solutions.