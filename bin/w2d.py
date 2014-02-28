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
import logging

from wiktionary2 import Wiktionary

logger = logging.getLogger('wikt2dict')

def download_wiktionaries(fn=None, wc_list=None):
    logger.info('Downloading Wiktionaries')


def extract_translations(wc_list=None):
    logger.info('Extracting translations')
    import config
    if wc_list:
        to_parse = filter(config.configs, lambda c: c.wc in wc_list)
    else:
        to_parse = config.configs
    for cfg in to_parse:
        wikt = Wiktionary(cfg)  #TODO
        wikt.parse_articles()  #TODO


def main():
    arguments = docopt(__doc__, version='Wikt2dict 1.1')
    if arguments['download']:
        if arguments['--wikicodes']:
            download_wiktionaries(fn=arguments['--wikicodes'])
        else:
            download_wiktionaries(wc_list=arguments['--wikicodes'])
    if arguments['extract']:
        if arguments['--wikicodes']:
            extract_translations(fn=arguments['--wikicodes'])
        else:
            extract_translations(wc_list=arguments['--wikicodes'])
    print(arguments)

if __name__ == '__main__':
    main()
