#!/bin/env bash

data=bach_chorales.dataset

dataDir=../../data/
rawDir=$dataDir"raw/"
outDir=$dataDir"processed/"

csvcut -c 1,3-14 "$rawDir$data" | tail -n +2 | sed -e 's/YES/1/g' -e 's/NO/0/g' | awk -F',' -v out="$outDir" '
{
    file = out $1
    $1 = ""
    sub(/^,/, "")
    print >> (file)
}'
