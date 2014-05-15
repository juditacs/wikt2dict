# wikt2dict

Wiktionary translation parser tool for many language editions.

Wikt2dict parses only the translation sections.
It also has a triangulation mode which combines the extracted translation pairs to
generate new ones. 

## News

Wikt2dict changed completely, hope for the better. If you would like to keep using the old one:
https://github.com/juditacs/wikt2dict/tree/a08cc896c22dc78db62e1b790c3ec157d00ad08f

* Changed interface. See below for details (April 2014)
* Added support for German Wiktionary (Aug 2013)
* Had a poster at the Building and Using Comparable Corpora Workshop (BUCC) at ACL13, updated Bibtex accordingly
  * The paper is available here: http://www.aclweb.org/anthology-new/W/W13/W13-2507.pdf
* All dictionaries are available here: http://hlt.sztaki.hu/resources

## Requirements

Wikt2dict should run on any mainstream Linux distribution. It needs Python2.7 and basic command line
tools that should be found on most Linux distributions (wget, bzcat).
If you're working with large Wiktionaries such as the English Wiktionary, you need at least 10GB of
free space, preferrably more.
For all Wiktionary editions supported, you need about 35GB of free space.

## Installation

    git clone https://github.com/juditacs/wikt2dict.git
    cd wikt2dict
    sudo pip install -e .

You can install wikt2dict in virtualenv if you do not have root access.

A very quick guide to virtualenv:

    virtualenv w2d_env
    source w2d_env/bin/activate
    git clone https://github.com/juditacs/wikt2dict.git
    cd wikt2dict
    pip install -e .

Note that this way wikt2dict can only be used once the virtualenv was activated.
You need to run source w2d\_env/bin/activate every time you login.

## Very quick start

Wikt2dict's basic functionalities can be accessed using the w2d.py script (which should be directly callable after running pip install).

    $ w2d.py -h
    Wikt2Dict
    
    Usage:
      w2d.py (download|extract|triangulate|all) (--wikicodes=file|<wc>...)
    
    Options:
      -h --help              Show this screen.
      --version              Show version.
      -w, --wikicodes=file   File containing a list of wikicodes.

W2d.py currently supports 3+1 actions. All actions need a list of Wiktionary codes to work with.
You can either list the codes manually or provide them in a file (--wikicodes option).

The actions are:

1. download: download the Wiktionary dumps. Convert them from XML to plaintext with a special page separator.
The files are saved in the directory specified in config.py:wiktionary\_defaults['dump\_path\_base'].
The default is wikt2dict/dat/wiktionary/<language name>
1. extract: extract translations.
The translations are saved to the file specified in config.py:wiktionary\_defaults['output\_path'].
By default this file is wikt2dict/dat/wiktionary/<language name>/translation\_pairs.
1. triangulate: use triangulation to generate more translations.
Triangles are saved to the directory config.py:wiktionary\_defaults['triangle\_dir'] in separate files
named as <wc1>\_<wc2>\_<wc3>. This file would contain pairs in wc1-wc3 languages triangulated via wc2.
For more information on triangulating, see: http://aclweb.org/anthology/W/W13/W13-2507.pdf
Note that triangulating only makes sense if you specify at least 3 languages.
1. all: do all of the above.

Let's try it out on a few small Wiktionary editions.

Downloading the Slovak, the Slovenian and the Occitan Wiktionaries:

    w2d.py download sk sl li

The downloaded and textified Wiktionaries should appear in dat/wiktionary/<language name>/<wikicode>wiktionary.txt

Extracting translations:

    w2d.py extract sk sl li

The extracted translations should appear in dat/wiktionary/<language name>/translation\_pairs.

Now let's try triangulating to get a bunch of new translations:

    w2d.py triangulate sk sl li

The results should appear in dat/triangle/ arranged in subdirectories with a maximum of 1000 files per directory
to avoid filesystem problems.
Using only 3 such small editions for triangulating does not make much sense (it yielded 4 pairs on the April 2014 dumps).

Or do all of it at once:

    w2d.py all sk sl li

## Output

The output is a tab-separated file. 
If you only want the translation pairs you should just cut the first 4 columns:
    
    cut -f1-4 <output_file> > <dictionary>

Or without Wiktionary codes:

    cut -f2,4 <output_file> > <dictionary>

Where <output\_file> should be replaced by the output of either the Wiktionary extraction
or the triangulating, and <dictionary> is the file where the filtered columns are saved.

The columns explained in details are below.

The one extracted from the Wiktionaries has the following columns:

1. Wiktionary code 1 (language 1)
2. Word or expression in language 1
3. Wiktionary code 2 (language 2)
4. Word or expression in language 2
5. Wiktionary code of the Wiktionary from which the pair was extracted
6. Article from which the pair was extracted
7. Type of parser used (you probably don't need this)

An example:

    en      dog     fr      chien   en      dog     defaultparser

The triangulating output has the following columns:

1. Wiktionary code 1 (language 1)
2. Word or expression in language 1
3. Wiktionary code 2 (language 2)
4. Word or expression in language 2
5. 5-10. The articles and their source Wiktionary that were used to generate this pair

    hu      kutya   oc      chin    hu      kutya   el      σκύλος  oc      chin

The pairs are listed with all possible ways they were found. I provided a little script to 
sort, unify and count the number of times one pair appears.
Usage (from wikt2dict base directory):

    cat <triangle_files_to_merge> | bash bin/merge_triangle.sh > output_file

To use with all triangle files:

    cat <triangle_dir>/*/* | bash bin/merge_triangle.sh > output_file

where the <triangle\_dir> should be replaced with the directory where the individual triangle files are
stored (triangle\_dir option).

Congratulations, you have successfully finished the test tutorial of wikt2dict.
Please send your feedback to judit@sch.bme.hu.

## Cite

Please cite:

    @InProceedings{acs-pajkossy-kornai:2013:BUCC,  
      author    = {Acs, Judit  and  Pajkossy, Katalin  and  Kornai, Andras},  
      title     = {Building basic vocabulary across 40 languages},  
      booktitle = {Proceedings of the Sixth Workshop on Building and Using Comparable Corpora},  
      month     = {August},  
      year      = {2013},  
      address   = {Sofia, Bulgaria},  
      publisher = {Association for Computational Linguistics},  
      pages     = {52--58},  
      url       = {http://www.aclweb.org/anthology/W13-2507}  
    }  

## Known Bugs

* FIXED - Lithuanian and a few other Wiktionaries have translation tables in many articles
not only for Lithuanian words and these are parsed as they were Lithuanian words. 
Language detection for all articles should be added. This issue is fixed but configuration
should be updated.

* Logging is not always accurate

## Upcoming

* 4lang coverage, finding translations for a list of words

  * Check out our basic vocabulary at: http://hlt.sztaki.hu/resources/4lang/

<!---
You can create statistics of the coverage of 4lang and uroboros by calling:

    cat ../dat/lang/*/res/word_pairs | python fourlang_coverage.py ../res/4lang/coverage

This would take all translations extracted from the Wiktionaries and compute
the coverage of 4lang and uroboros based on each language of 4lang and all of them
combined as well.
The statistics are saved in ../res/4lang/ with the coverage prefix.
-->


