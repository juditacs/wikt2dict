from article_parsers import DefaultArticleParser, LangnamesArticleParser
import re
from os import path

wiktionary_defaults = {
    'wikicodes_file': '../res/wikicodes',
    'dump_path_base': '../dat/wiktionary_2014_febr',
    'dump_file_postfix': 'wiktionary.txt',
}

parser_defaults = {
    'translation_prefix': ur't[\u00f8\+\-]?',
    'wc_field': 1,
    'word_field': 2,
    'blacklist': ['PAGENAME'],  # words that should not appear
}

langname_parser_defaults = {
}

class WiktionaryConfig(object):

    def __init__(self):
        for key, value in wiktionary_defaults.iteritems():
            self[key] = value
        self.full_name = ''
        self.wc = ''
        self.parsers = list()
        self._wikicodes = None

    def __getitem__(self, key):
        return self.__dict__.get(key, None)
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    @property
    def wikicodes(self):
        if not self._wikicodes:
            with open(self.wikicodes_file) as f:
                self._wikicodes = set([l.strip() for l in f])
        return self._wikicodes

    @property
    def dump_filename(self):
        return self.wc + self.dump_file_postfix 


class ParserConfig(object):

    defaults = {
    }
    def __init__(self, wikt_cfg=None, parser_cfg=None):
        for key, value in self.defaults.iteritems():
            self[key] = value
        if parser_cfg:
            for key, value in parser_cfg.iteritems():
                self[key] = value
        if wikt_cfg:
            for key, value in wikt_cfg.iteritems():
                self[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__.get(key, None)


class DefaultParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(parser_defaults)
        self._trad_re = None
        self._skip_trans_re = None
        super(DefaultParserConfig, self).__init__(wikt_cfg, parser_cfg)

    @property
    def skip_translation_re(self):
        if not self._skip_trans_re:
            self._skip_trans_re = re.compile(
                ur'(' + '|'.join(self.blacklist) + ')', re.UNICODE)
        return self._skip_trans_re

    @property
    def trad_re(self):
        if not self._trad_re:
            re_str = (r'\{\{' + self.translation_prefix +
                      r'\|([^}|]+)\|'  # wikicode 
                      r'([^}|]*)'  # word
                      r'(\|[^}]*)*\}\}')  # rest
            self._trad_re = re.compile(re_str, re.UNICODE)
        return self._trad_re


class LangnamesParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(langname_parser_defaults)
        super(LangnamesParserConfig, self).__init__(wikt_cfg, parser_cfg)


class EsperantoConfig(WiktionaryConfig):

    def __init__(self):
        super(EsperantoConfig, self).__init__()
        self.full_name = 'Esperanto'
        self.wc = 'eo'
        self.default_cfg = DefaultParserConfig()
        self.langnames_cfg = LangnamesParserConfig()
        self.parsers = [#(DefaultArticleParser, self.default_cfg),
                           (LangnamesArticleParser, self.langnames_cfg),
                          ]

    @property
    def dump_path(self):
        #TODO exception if path does not exist
        return path.join(self.dump_path_base, self.full_name, self.dump_filename)


configs = [EsperantoConfig()]

