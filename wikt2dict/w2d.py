"""
Wikt2Dict

Usage:
  w2d.py (download|textify|extract|triangulate) (--wikicodes=file|<wc>...)

Options:
  -h --help              Show this screen.
  --version              Show version.
  -w, --wikicodes=file   File containing a list of wikicodes.
"""
from docopt import docopt
from sys import stderr
from itertools import combinations
import logging

from wikt2dict.wiktionary import Wiktionary
from wikt2dict.triangulator import Triangulator
import wikt2dict.config as config

logger = logging.getLogger('wikt2dict')


def download_wiktionaries(fn=None, wc_list=None):
    # TODO
    logger.info('Downloading Wiktionaries')


def extract_translations(wc_list=None, fn=None):
    logger.info('Extracting translations')
    if wc_list:
        to_parse = filter(lambda c: c.wc in wc_list, config.configs)
    else:
        to_parse = config.configs
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
        if arguments['--wikicodes']:
            download_wiktionaries(fn=arguments['--wikicodes'])
        else:
            download_wiktionaries(wc_list=arguments['--wikicodes'])
    if arguments['extract']:
        if arguments['--wikicodes']:
            extract_translations(fn=arguments['--wikicodes'])
        else:
            extract_translations(wc_list=arguments['<wc>'])
    if arguments['triangulate']:
        triangulate(wc_set)

if __name__ == '__main__':
    main()
