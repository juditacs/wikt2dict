root=$2;
this=`pwd`
while IFS=$'\t' read -r -a myArray
do
 wc=${myArray[0]}
 wcdir=${myArray[1]}
 if [ -f $root/${wcdir}/${wc}wiktionary-latest-pages-meta-current.xml ]; then
     if [ ! -f $root/${wcdir}/${wc}wiktionary.txt ]; then
         echo $wc
         echo $wcdir
         cd ${root}/${wcdir}
         cat ${wc}wiktionary-latest-pages-meta-current.xml | python ${this}/external/articles.py > ${wc}wiktionary.txt
         cd ../..
     fi
 fi
done < ${1}
