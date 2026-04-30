#!/bin/bash

# Primary source
archive1=bach-chorale-harmony-data.zip
url1=https://www.kaggle.com/api/v1/datasets/download/lsind18/bach-chorale-harmony-data
data1=bach_choral_set_dataset.csv

# Fallback source
archive2=bach+choral+harmony.zip
url2=https://archive.ics.uci.edu/static/public/298/$archive2
data2=jsbach_chorals_harmony.data

# Paths
tmpDir=tmp/
dataDir=data/raw/

outFile=bach_chorales.dataset

cleanup() {
    rm -rf "$tmpDir"
}

mkdir -p "$tmpDir"
mkdir -p "$dataDir"

download_and_extract () {
    local url=$1
    local archive=$2
    local data=$3

    echo "Provo a scaricare il dataset da $url..."
    if curl -sLo "$tmpDir$archive" "$url"; then
        echo -e "\tDataset scaricato"
    else
        echo -e "\tDownload fallito"
        return 1
    fi

    echo "Decomprimo l'archivio..."
    if unzip -q "$tmpDir$archive" -d "$tmpDir"; then
        echo -e "\tArchivio decompresso"
    else
        echo -e "\tErrore decompressione"
        return 1
    fi

    if [ -f "$tmpDir$data" ]; then
        echo "Sposto il file in $dataDir$outFile"
        if mv "$tmpDir$data" "$dataDir$outFile"; then
            echo -e "\tTutto pronto"
            return 0
        else
            echo -e "\tErrore nello spostamento"
            return 1
        fi
    else
        echo -e "\tFile $data non trovato"
        return 1
    fi
}

# Try primary source
if download_and_extract "$url1" "$archive1" "$data1"; then
    cleanup
    exit 0
fi

echo "Fallback al dataset alternativo..."

# Cleanup before fallback just in case :)
rm -rf "$tmpDir"*

# Try fallback
if download_and_extract "$url2" "$archive2" "$data2"; then
    cleanup
    exit 0
else
    echo "Entrambi i download sono falliti. :/"
    echo "Prova a scaricare uno dei dataset manualmente ed inseriscilo in $dataDir$outFile"
    cleanup
    exit 1
fi
