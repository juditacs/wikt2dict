from ConfigParser import NoSectionError

from handlers import ConfigHandler, LogHandler
from article_parsers import DefaultArticleParser, ArticleParserWithLangnames

class Wiktionary(object):

    def __init__(self, wc, cfg_fn, article_parser=None):
        try:
            self.wc = wc
            self.cfg = ConfigHandler(wc, cfg_fn)
            self.log_handler = LogHandler(wc, self.cfg)
            self.init_parser_of_type()
            self.dump_path = (self.cfg['dumpdir'] + '/' + self.cfg['fullname'] + '/' +
                    self.wc + 'wiktionary.txt')
        except KeyError as e:
            self.log_handler.error(e.message + \
                                   " parameter must be defined in config file ")
        except NoSectionError as e:
            self.log_handler.error("Section not defined " + wc)
        except Exception as e:
            self.log_handler.error("Unknown error " + e)

    def init_parser_of_type(self):
        type_ = self.cfg['parser_type']
        if type_ == 'default':
            self.article_parser = DefaultArticleParser(self)
        elif type_ == 'langnames':
            self.article_parser = ArticleParserWithLangnames(self)

    def set_parser(self, parser):
        self.article_parser = parser

    def read_dump(self):
        txt_f = open(self.dump_path)
        page_sep = '%%#PAGE'        
        this_title = unicode()
        this_article = unicode()
        last_title = unicode()
        last_article = unicode()
        for l in txt_f:
            if l.startswith(page_sep):
                if this_article and this_title:
                    last_article = this_article
                    last_title = this_title
                    this_article = unicode()
                    this_title = l.split(page_sep)[-1].strip().decode('utf8')
                    yield tuple([last_title, last_article])
                else:
                    this_title = l.split(page_sep)[-1].strip().decode('utf8')
            else:
                this_article += l.decode('utf8')
        txt_f.close()
        yield tuple([this_title, this_article])

    def parse_all_articles(self):
        for article in self.read_dump():
            self.article_parser.parse_article(article)

    def write_pairs(self):
        self.article_parser.write_word_pairs_to_file()

        
        
            
