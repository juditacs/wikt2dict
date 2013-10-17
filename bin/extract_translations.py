from sys import argv, path
path.append('../src')

from wiktionary import Wiktionary
import logging

def main():
    if argv[2] == 'all' and len(argv) > 3:
        wc_f = open(argv[3])
        wikicodes = [wc.strip() for wc in wc_f]
    else:
        wikicodes = [wc.strip() for wc in argv[3:]]
    cfg_fn = argv[1]
    logger = logging.getLogger('wikt2dict')
    for wc in set(wikicodes):
        try:
            #print 'Parsing ' + wc + 'wiktionary'
            wiktionary = None #FIXME error handling workaround 
            wiktionary = Wiktionary(wc, cfg_fn)
            logger.info('%s Wiktionary object built', wiktionary.cfg['fullname'])
            wiktionary.parse_all_articles()
            logger.info('%s Wiktionary articles parsed', wiktionary.cfg['fullname'])
            #print '   Extracted {0} pairs'.format(len(wiktionary.article_parser.pairs))
            wiktionary.write_pairs(fn=argv[2] + '/' + wc + '.wikt.dict')
            logger.info('%s Wiktionary translations written to file', wiktionary.cfg['fullname'])
        except NotImplementedError as e:
            if wiktionary and wiktionary.cfg and wiktionary.cfg['fullname']:
                logger.error('%s Wiktionary unrecognized parser type', wiktionary.cfg['fullname'])
            else:
                logger.error('%s Wiktionary unrecognized parser type', wc)
            continue
        except AttributeError as e:
            print e
            continue
        except Exception as e:
            print wc, str(e)
            continue

if __name__ == '__main__':
    main()

