"""
Wikt2Dict

Usage:
  w2d.py (download|extract|triangulate) (--wikicodes=file|<wc>...)

Options:
  -h --help              Show this screen.
  --version              Show version.
  -w, --wikicodes=file   File containing a list of wikicodes.
"""
from docopt import docopt
from sys import stderr
from itertools import combinations
from urllib import urlretrieve
from os import path
from subprocess import call
import logging

from wikt2dict.wiktionary import Wiktionary
from wikt2dict.triangulator import Triangulator
import wikt2dict.config as config

logging.basicConfig()
logger = logging.getLogger('wikt2dict')
logger.setLevel(logging.INFO)


def download_wiktionaries(wc_set):
    logger.info('Downloading Wiktionaries')
    to_download = filter(lambda c: c.wc in wc_set, config.configs)
    for cfg in to_download:
        logger.info(cfg.dump_url)
        urlretrieve(cfg.dump_url, cfg.bz2_path)
        wiki_textify_path = path.join(config.base_dir, 'external/articles.py')
        call(['bzcat {0} | python {1} > {2}'.format(
            cfg.bz2_path, wiki_textify_path, cfg.dump_path)], shell=True)


def extract_translations(wc_set):
    logger.info('Extracting translations')
    to_parse = filter(lambda c: c.wc in wc_set, config.configs)
    for cfg in to_parse:
        print cfg.wc
        wikt = Wiktionary(cfg)
        wikt.parse_articles()


def triangulate(wc_set):
    n = 53
    num_of_tr = n * (n - 1) * (n - 2) / 6
    i = 1
    for triangle_wc in combinations(wc_set, 3):
        stderr.write(str(i) + '/' + str(num_of_tr) + repr(triangle_wc) + '\n')
        i += 1
        logger.info(' '.join(triangle_wc) + ' triangle')
        triangulator = Triangulator(triangle_wc)
        triangulator.collect_triangles()
        triangulator.write_triangles()


def main():
    arguments = docopt(__doc__, version='Wikt2dict 1.1')
    if arguments['--wikicodes']:
        with open(arguments['--wikicodes']) as f:
            wc_set = set([l.strip() for l in f])
    else:
        wc_set = set(arguments['<wc>'])
    if arguments['download']:
        download_wiktionaries(wc_set)
    if arguments['extract']:
        extract_translations(wc_set)
    if arguments['triangulate']:
        triangulate(wc_set)

if __name__ == '__main__':
    main()
