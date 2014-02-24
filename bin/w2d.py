"""
Wikt2Dict

Usage:
  w2d.py (download|textify) (--wikicodes=file|<wc>...)

Options:
  -h --help              Show this screen.
  --version              Show version.
  -w, --wikicodes=file   File containing a list of wikicodes.
"""
from docopt import docopt
import logging

logger = logging.getLogger('wikt2dict')

def download_wiktionaries(fn=None, wc_list=None):
    logger.info('Downloading Wiktionaries')
    pass


def main():
    arguments = docopt(__doc__, version='Wikt2dict 1.1')
    if arguments['download']:
        if arguments['--wikicodes']:
            download_wiktionaries(fn=arguments['--wikicodes'])
        else:
            download_wiktionaries(wc_list=arguments['--wikicodes'])
    print(arguments)

if __name__ == '__main__':
    main()
