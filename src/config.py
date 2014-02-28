from article_parsers import DefaultArticleParser, LangnamesArticleParser


class WiktionaryConfig(object):

    full_name = ''
    wc = ''
    parsers = list()


class ParserConfig(object):
    pass


class DefaultParserConfig(ParserConfig):
    pass

class LangnamesParserConfig(ParserConfig):
    pass


class EsperantoConfig(WiktionaryConfig):

    full_name = 'Esperanto'
    wc = 'eo'
    default_cfg = DefaultParserConfig()
    langnames_cfg = LangnamesParserConfig()
    parsers = [(DefaultArticleParser, default_cfg),
                       (LangnamesArticleParser, langnames_cfg),
                      ]

configs = [EsperantoConfig()]

