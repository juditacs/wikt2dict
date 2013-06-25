from sys import argv
from article_parsers import DefaultArticleParser, ArticleParserWithLangnames
from wiktionary import Wiktionary

def init_parser_of_type(parser_type, wikt):
    if parser_type == 'default':
        return DefaultArticleParser(wikt)
    elif parser_type == 'langnames':
        return ArticleParserWithLangnames(wikt)

def main():
    wikicodes = [wc.strip() for wc in argv[2:]]
    cfg_fn = argv[1]
    for wc in wikicodes:
        print wc
        wiktionary = Wiktionary(wc, cfg_fn)
        #this_parser = init_parser_of_type(parser_type, wiktionary)
        #wiktionary.set_parser(this_parser)
        print "Wiktionary object built"
        wiktionary.parse_all_articles()
        print "Articles parsed"
        wiktionary.write_pairs()
        print "Written to file"
        #all_langs.wikicode_to_obj[wc].extract_word_pairs(this_parser, wc + cfg['wiktionary_dump_suffix'])
        #outf_fn = all_langs.wikicode_to_obj[wc].dumpdir + '/' + wc + cfg['word_pairs_outfile']
        #this_parser.write_word_pairs_to_file(outf_fn)

if __name__ == '__main__':
    main()

