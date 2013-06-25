root=$2;
while IFS=$'\t' read -r -a myArray
do
 wc=${myArray[0]}
 wcdir=${myArray[1]}
 if [ ! -f $root/${wcdir}/${wc}wiktionary-latest-pages-meta-current.xml ]; then
     echo $wc
     echo $wcdir
     mkdir -p ${root}/${wcdir}
     cd ${root}/${wcdir}
     wget http://dumps.wikimedia.org/${wc}wiktionary/latest/${wc}wiktionary-latest-pages-meta-current.xml.bz2
     bunzip2 ${wc}wiktionary-latest-pages-meta-current.xml.bz2
     cd ../..
 fi
done < ${1}
