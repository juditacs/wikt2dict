class Wiktionary(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.init_parsers()

    def init_parsers(self):
        self.parsers = list()
        for parser_cl, parser_cfg in self.cfg.parsers:
            self.parsers.append(parser_cl(self.cfg, parser_cfg))

    def parse_articles(self, write_immediately=True):
        for title, text in self.read_dump():
            pairs = self.extract_translations(title, text)
            if pairs:
                if write_immediately:
                    self.write_one_article_translations(pairs)
                else:
                    self.store_translations(pairs)

    def extract_translations(self, title, text):
        if self.skip_article(title, text):
            return
        pairs = list()
        for parser in self.parsers:
            pairs.extend([(self.cfg.wc, title, wc2, word2)
                          for wc2, word2 in parser.extract_translations(title, text)])
        return pairs

    def skip_article(self, title, text):
        if not title.strip() or not text.strip():
            return True
        if ':' in title:  # skipping namespaced articles
            return True
        return False

    def write_one_article_translations(self, pairs):
        for p in pairs:
            wc1, w1, wc2, w2 = p[0:4]
            if wc1 < wc2:
                print('\t'.join(p).encode('utf8'))
            else:
                print('\t'.join((wc2, w2, wc1, w1)).encode('utf8'))

    def store_translations(self, pairs):
        pass

    def write_translations(self):
        pass
    
    def read_dump(self):
        with open(self.cfg.dump_path) as f:
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



