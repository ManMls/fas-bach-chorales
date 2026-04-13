#!/bin/bash

archive=bach+choral+harmony.zip
data=jsbach_chorals_harmony.data

url=https://archive.ics.uci.edu/static/public/298/$archive

echo "Provo a scaricare il dataset..."
if wget -qP tmp/ $url; then
    echo -e "\tDataset scaricato"
else
    echo -e "\tErrore"
    echo -e "\tProva a scaricarlo manualmente da: $url"
    echo -e "\tdentro $(pwd)/tmp/ e a rieseguire questo script"
fi

echo "Decomprimo l'archivio..."
if unzip -q "tmp/$archive" -d "tmp"; then
    echo -e "\tArchivio decomporesso"
else
    echo -e "\tNon sono riuscito a decomprimere l'archivio"
    exit 1
fi

if [ -f "tmp/$data" ]; then
    if mv "tmp/$data" ../../data/raw/; then
        echo -e "\tTutto pronto"
    else
        echo -e "\tNon sono riuscito a spostare il file?"
        exit 1
    fi
else
    echo -e "\tNon ho trovato il file tmp/$data"
    exit 1
fi

rm -r tmp

echo -e "\nEseguo extract_chorale_events.sh"

bash extract_chorale_events.sh
