#!/bin/env bash


DATASET="../../data/raw/bach_choral_set_dataset.xls"
OUTDIR="../../data/processed/"


csvcut -c 1,3-14 "$DATASET" | tail -n +2 | sed -e 's/YES/1/g' -e 's/NO/0/g' | awk -F',' -v out="$OUTDIR" '
{
    file = out $1
    $1 = ""
    sub(/^,/, "")
    print >> (file)
}'
