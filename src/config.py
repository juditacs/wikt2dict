from article_parsers import DefaultArticleParser, LangnamesArticleParser
import re
from os import path

wiktionary_defaults = {
    'wikicodes_file': '../res/wikicodes',
    'dump_path_base': '../dat/wiktionary_2014_febr',
    'dump_file_postfix': 'wiktionary.txt',
    'output_file': 'translation_pairs',
    'verbose_output': True,
}

parser_defaults = {
    'blacklist': ['PAGENAME'],  # words that should not appear
    'placeholder': [],
}

default_parser_defaults = {
    'translation_prefix': ur't[\u00f8\+\-]?',
    'wc_field': 1,
    'word_field': 2,
    'features': ['defaultparser'],
}

langname_parser_defaults = {
    'language_name_field': 1,
    'translation_field': 2,
    'translation_entity_delimiter': ',',
    'translation_re': re.compile(r'\[\[([^\[\]]+)\]\]', re.UNICODE),
    'features': ['langnamesparser'],
}


class DictLikeClass(object):

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class WiktionaryConfig(DictLikeClass):

    def __init__(self):
        for key, value in wiktionary_defaults.iteritems():
            self[key] = value
        self._parsers = None
        self._parser_configs = None
        self._wikicodes = None

    @property
    def wikicodes(self):
        if not self._wikicodes:
            with open(self.wikicodes_file) as f:
                self._wikicodes = set([l.strip() for l in f])
        return self._wikicodes

    @property
    def dump_filename(self):
        return self.wc + self.dump_file_postfix

    @property
    def dump_path(self):
        return path.join(self.dump_path_base, self.full_name, self.dump_filename)

    @property
    def output_path(self):
        return path.join(self.dump_path_base, self.full_name, self.output_file)

    @property
    def parsers(self):
        if not self._parsers:
            self._parsers = list()
            if self._parser_configs:
                for parser_cl, parser_cfg_cl, parser_cfg in self._parser_configs:
                    self._parsers.append((parser_cl, parser_cfg_cl(parser_cfg)))
        return self._parsers


class ParserConfig(DictLikeClass):

    defaults = parser_defaults

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self._skip_trans_re = None
        for key, value in self.defaults.iteritems():
            self[key] = value
        if parser_cfg:
            for key, value in parser_cfg.iteritems():
                self[key] = value
        if wikt_cfg:
            for key, value in wikt_cfg.iteritems():
                self[key] = value

    @property
    def skip_translation_re(self):
        if not self._skip_trans_re:
            self._skip_trans_re = re.compile(
                ur'(' + '|'.join(self.blacklist) +
                '|'.join(self.placeholder) + ')',
                re.UNICODE)
        return self._skip_trans_re

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__.get(key, None)


class DefaultParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(default_parser_defaults)
        self._trad_re = None
        super(DefaultParserConfig, self).__init__(wikt_cfg, parser_cfg)

    @property
    def trad_re(self):
        if not self._trad_re:
            self._trad_re = re.compile(r'\{\{' + self.translation_prefix +
                                       r'\|([^}|]+)\|'  # wikicode
                                       r'([^}|]*)'  # word
                                       r'(\|[^}]*)*\}\}', re.UNICODE)  # rest
        return self._trad_re


class LangnamesParserConfig(ParserConfig):

    def __init__(self, wikt_cfg=None, parser_cfg=None):
        self.defaults.update(langname_parser_defaults)
        self._bracket_re = None
        self._delimiter_re = None
        super(LangnamesParserConfig, self).__init__(wikt_cfg, parser_cfg)

    @property
    def bracket_re(self):
        if not self._bracket_re:
            self._bracket_re = re.compile(r'\([^)]*\)', re.UNICODE)
        return self._bracket_re

    @property
    def delimiter_re(self):
        if not self._delimiter_re:
            self._delimiter_re = re.compile(self.translation_entity_delimiter,
                                            re.UNICODE)
        return self._delimiter_re


class DefaultWiktionaryConfig(WiktionaryConfig):

    def __init__(self):
        super(DefaultWiktionaryConfig, self).__init__()
        try:
            cfg = self.default_cfg
        except AttributeError:
            cfg = {}
        self._parser_configs = [
            [DefaultArticleParser, DefaultParserConfig, cfg]
        ]


class BasqueConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Basque'
        self.wc = 'eu'
        self.default_cfg = {
            'translation_prefix': r'itz',
        }
        super(BasqueConfig, self).__init__()


class BulgarianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Bulgarian'
        self.wc = 'bg'
        self.default_cfg = {
            'translation_prefix': u'\u043f',
        }
        super(BulgarianConfig, self).__init__()


class CatalanConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Catalan'
        self.wc = 'ca'
        self.default_cfg = {
            'translation_prefix': r'trad[\-\+]?',
            'placeholder': r'\?',
        }
        super(CatalanConfig, self).__init__()


class CroatianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Croatian'
        self.wc = 'hr'
        self.default_cfg = {
            'translation_prefix': 'pr',
        }
        super(CroatianConfig, self).__init__()


class CzechConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Czech'
        self.wc = 'cs'
        self.default_cfg = {
            'translation_prefix': r'P',
        }
        super(CzechConfig, self).__init__()


class EnglishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'English'
        self.wc = 'en'
        super(EnglishConfig, self).__init__()


class EsperantoConfig(WiktionaryConfig):

    def __init__(self):
        super(EsperantoConfig, self).__init__()
        self.full_name = 'Esperanto'
        self.wc = 'eo'
        langnames_cfg = {
            'translation_line': '\*\s*\{{([^}]+)}}:\s*(.+)',
            'langnames': False,
            'junk_re': re.compile(r'(:[^:]*:|\{\{|\}\}|xxx)', re.UNICODE),
        }
        self.langnames_cfg = LangnamesParserConfig(langnames_cfg)
        self.parsers = [
            (DefaultArticleParser, DefaultParserConfig()),
            (LangnamesArticleParser, self.langnames_cfg),
        ]


class FrenchConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'French'
        self.wc = 'fr'
        self.default_cfg = {
            'translation_prefix': r'trad[\-\+]?',
        }
        super(FrenchConfig, self).__init__()


class GalicianConfig(FrenchConfig):

    def __init__(self):
        super(GalicianConfig, self).__init__()
        self.full_name = 'Galician'
        self.wc = 'gl'
        print self.parsers


class GeorgianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Georgian'
        self.wc = 'ka'
        self.default_cfg = {
            'translation_prefix': u'\u10d7x*',
        }
        super(GeorgianConfig, self).__init__()


class GreekConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Greek'
        self.wc = 'el'
        self.default_cfg = {
            'translation_prefix': u'\u03c4',
            'placeholder': ur'[xX\u03c7\u03a7]{3}',
        }
        super(GreekConfig, self).__init__()


class HungarianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Hungarian'
        self.wc = 'hu'
        super(HungarianConfig, self).__init__()


class IcelandicConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Icelandic'
        self.wc = 'is'
        self.default_cfg = {
            'translation_prefix': ur'\xfe\xfd\xf0ing',
        }
        super(IcelandicConfig, self).__init__()


class KurdishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Kurdish'
        self.wc = 'ku'
        self.default_cfg = {
            'translation_prefix': r'(?:W\+?|trad)',
        }
        super(KurdishConfig, self).__init__()


class LatinConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Latin'
        self.wc = 'la'
        self.default_cfg = {
            'translation_prefix': r'x(\|[^|]*=[^|]*)?',
        }
        super(LatinConfig, self).__init__()


class LimburgishConfig(FrenchConfig):

    def __init__(self):
        super(LimburgishConfig, self).__init__()
        self.full_name = 'Limburgish'
        self.wc = 'li'


class NorwegianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Norwegian'
        self.wc = 'no'
        self.default_cfg = {
            'translation_prefix': ur'(?:o|overs|t[\u00f8\+\-]?)',
        }
        super(NorwegianConfig, self).__init__()


class OccitanConfig(FrenchConfig):

    def __init__(self):
        super(OccitanConfig, self).__init__()
        self.full_name = 'Occitan'
        self.wc = 'oc'


class PortugueseConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Portuguese'
        self.wc = 'pt'
        self.default_cfg = {
            'translation_prefix': r'(?:trad[\-\+]?|xlatio)',
        }
        super(PortugueseConfig, self).__init__()


class SerbianConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Serbian'
        self.wc = 'sr'
        self.default_cfg = {
            'translation_prefix': u'\u041f',
            'word_field': -1,
        }
        super(SerbianConfig, self).__init__()


class SlovakConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Slovak'
        self.wc = 'sl'
        self.default_cfg = {
            'translation_prefix': 'P',
        }
        super(SlovakConfig, self).__init__()


class SpanishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Spanish'
        self.wc = 'es'
        self.default_cfg = {
            'translation_prefix': r'(?:trad|t)[\u00f8\+\-]?',
        }
        super(SpanishConfig, self).__init__()


class SwahiliConfig(FrenchConfig):

    def __init__(self):
        super(SwahiliConfig, self).__init__()
        self.full_name = 'Swahili'
        self.wc = 'sw'


class SwedishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Swedish'
        self.wc = 'sv'
        self.default_cfg = {
            'translation_prefix': ur'\u00f6.?',
        }
        super(SwedishConfig, self).__init__()


class TurkishConfig(DefaultWiktionaryConfig):

    def __init__(self):
        self.full_name = 'Turkish'
        self.wc = 'tr'
        self.default_cfg = {
            'translation_prefix': u'\xe7eviri',
        }
        super(TurkishConfig, self).__init__()


class DanishConfig(SpanishConfig):

    def __init__(self):
        super(SpanishConfig, self).__init__()
        self.full_name = 'Danish'
        self.wc = 'da'


class DutchConfig(FrenchConfig):

    def __init__(self):
        super(DutchConfig, self).__init__()
        self.full_name = 'Dutch'
        self.wc = 'nl'


class RomanianConfig(FrenchConfig):

    def __init__(self):
        super(RomanianConfig, self).__init__()
        self.full_name = 'Romanian'
        self.wc = 'ro'


class IndonesianConfig(FrenchConfig):

    def __init__(self):
        super(IndonesianConfig, self).__init__()
        self.full_name = 'Indonesian'
        self.wc = 'id'


configs = [
    BasqueConfig(),
    BulgarianConfig(),
    CatalanConfig(),
    CzechConfig(),
    CroatianConfig(),
    DanishConfig(),
    DutchConfig(),
    EnglishConfig(),
    #EsperantoConfig(),
    FrenchConfig(),
    GalicianConfig(),
    GreekConfig(),
    GeorgianConfig(),
    HungarianConfig(),
    IcelandicConfig(),
    IndonesianConfig(),
    KurdishConfig(),
    LatinConfig(),
    LimburgishConfig(),
    NorwegianConfig(),
    OccitanConfig(),
    PortugueseConfig(),
    RomanianConfig(),
    SerbianConfig(),
    SlovakConfig(),
    SpanishConfig(),
    SwahiliConfig(),
    SwedishConfig(),
    TurkishConfig()
]
