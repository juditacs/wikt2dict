from sys import argv
from wiktionary import Wiktionary
import logging

def main():
    if argv[2] == 'all' and len(argv) > 3:
        wc_f = open(argv[3])
        wikicodes = [wc.strip() for wc in wc_f]
    else:
        wikicodes = [wc.strip() for wc in argv[2:]]
    cfg_fn = argv[1]
    logger = logging.getLogger('wikt2dict')
    for wc in wikicodes:
        print wc
        try:
            wiktionary = Wiktionary(wc, cfg_fn)
            logger.info('%s Wiktionary object built', wiktionary.cfg['fullname'])
            wiktionary.parse_all_articles()
            logger.info('%s Wiktionary articles parsed', wiktionary.cfg['fullname'])
            wiktionary.write_pairs()
            logger.info('%s Wiktionary translations written to file', wiktionary.cfg['fullname'])
        except AttributeError:
            continue
        except Exception as e:
            print wc, str(e)
            continue

if __name__ == '__main__':
    main()

