#! /usr/bin/bash

DOWNLOAD_URL="https://api.checklistbank.org/dataset/307664/export.zip?extended=true&format=DwCA"

mkdir -p zip
wget -q --show-progress "$DOWNLOAD_URL" -O "zip/catalogueoflife.zip"

mkdir -p raw
unzip zip/catalogueoflife.zip -d raw
