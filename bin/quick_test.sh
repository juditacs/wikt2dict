#!/bin/bash
wc_test=$1

mkdir -p ../dat/wiktionary ../dat/triangle ../log ../res/langnames

grep ^${wc_test} ../res/wiktionaries-full.tsv > ../res/wiktionaries_to_download.tsv
bash download_wiktionaries.sh ../res/wiktionaries_to_download.tsv ../dat/wiktionary
bash wiktionary2text.sh ../res/wiktionaries_to_download.tsv ../dat/wiktionary

cd ../src
pw=`pwd`
export PYTHONPATH=$PYTHONPATH:${pw}
cd ../bin

python extract_translations.py ../cfg/w2d.cfg ${wc_test}

