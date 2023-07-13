#!/usr/bin/env bash

SOURCE=$1
MODEL=$2
RES=$3

mkdir -p observations/word_eval observations/sent_eval

OBS_W=observations/word_eval
OBS_S=observations/sent_eval

sh sent_eval.sh $SOURCE $MODEL $OBS_S
sh word_eval.sh $SOURCE $MODEL $OBS_W

rsync -a $OBS_S $MODEL
rsync -a $OBS_W $MODEL

mkdir -p $RES
cp $OBS_W/results.json $RES

rm -rf $OBS_S $OBS_W observations
