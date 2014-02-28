class Wiktionary(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.init_parsers()

    def init_parsers(self):
        self.parsers = list()
        for parser_cl, parser_cfg in self.cfg.parsers:
            self.parsers.append(parser_cl(self.cfg, parser_cfg))

    def parse_articles(self, write_immediately=False):
        for title, text in self.parse_dump():
            pairs = self.extract_translations(title, text)
            if write_immediately:
                self.write_one_article_translations(pairs)
            else:
                self.store_translations(pairs)

    def write_one_article_translations(self, pairs):
        pass

    def store_translations(self, pairs):
        pass

    def write_translations(self):
        pass
    
    def read_dump(self):
        with open(self.cfg.get_dump_path()) as f:
            title = u''
            article = u''
            page_sep = '%%#PAGE'
            for l_ in f:
                l = l_.decode('utf8')
                if l.startswith(page_sep):
                    if title and article:
                        yield title, article
                    title = l.split(page_sep)[-1].strip()
                    article = u''
                else:
                    article += l
            yield title, article



