wc=$1

mkdir -p dat/wiktionary dat/triangle log res/langnames

grep ^${wc} ../res/wiktionaries-full.tsv > ../res/wiktionaries_to_download.tsv
bash download_wiktionaries.sh ../res/wiktionaries_to_download.tsv ../dat/wiktionary
bash wiktionary2text.sh ../res/wiktionaries_to_download.tsv ../dat/wiktionary

cd ../src
export PYTHONPATH=$PYTHONPATH:$(pwd)
cd ../bin

python extract_translations.py ../cfg/w2d.cfg $wc

