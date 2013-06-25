from sys import argv
from wiktionary import Wiktionary
import logging

def main():
    wikicodes = [wc.strip() for wc in argv[2:]]
    cfg_fn = argv[1]
    logger = logging.getLogger('wikt2dict')
    for wc in wikicodes:
        print wc
        wiktionary = Wiktionary(wc, cfg_fn)
        logger.info('%s Wiktionary object built', wiktionary.cfg['fullname'])
        wiktionary.parse_all_articles()
        logger.info('%s Wiktionary articles parsed', wiktionary.cfg['fullname'])
        wiktionary.write_pairs()
        logger.info('%s Wiktionary translations written to file', wiktionary.cfg['fullname'])

if __name__ == '__main__':
    main()

