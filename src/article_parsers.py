import re
from collections import defaultdict

from article import ArticleParser

# tester method
def uprint(str_):
    print str_.encode('utf8')

class ArticleParserWithLangnames(ArticleParser):
    """ Class for parsing Wiktionaries that use simple lists for translations
    instead of templates """

    def __init__(self, wikt, filter_langs=None):
        ArticleParser.__init__(self, wikt, filter_langs)
        self.langname_field = int(self.cfg['language_name_field'])
        self.translation_field = int(self.cfg['translation_field'])
        self.translation_line_re = re.compile(ur'' + \
                   self.cfg['translation_line'].decode('utf8'), re.UNICODE)
        self.entity_delimiter = self.cfg['translation_entity_delimiter']
        if self.cfg['skip_translation']:
            self.skip_re_l = [i.decode('utf8') 
                              for i in self.cfg['skip_translation'].split(',')]
        else:
            self.skip_re_l = None
        self.read_langname_mapping(self.cfg)

    def read_langname_mapping(self, cfg):
        self.mapping = dict()
        if cfg['uses_langnames'] == '1':
            f = open(cfg['langnames'])
            for l in f:
                fields = l.strip().decode('utf8').split('\t')
                for langname in fields[1:]:
                    self.mapping[langname] = fields[0]
                    self.mapping[langname.title()] = fields[0]
            f.close()
        else:
            self.mapping = dict([(wc, wc) for wc in self.wikicodes])

    def get_pairs(self, text):
        translations = defaultdict(list)
        trans_lines = self.translation_line_re.finditer(text)
        for t in trans_lines:
            if self.skip_translation_line(t.group(0)):
                continue
            langname = t.group(self.langname_field)
            if langname in self.mapping:
                wc = self.mapping[langname.lower()]
                entities = re.sub('\([^)]*\)', '', t.group(self.translation_field))
                entities = re.split(self.entity_delimiter, entities)
                for entity in entities:
                    ent = self.trim_translation(entity, wc)
                    if ent:
                        if self.skip_translation_re and self.skip_translation_re.search(ent):
                            continue
                        translations[wc].append(ent)
        return translations

    def trim_translation(self, trans, wc=None):
        """ take wc as parameters to make it possible to parse based on language """
        if wc == 'ja' and '{' in trans:
            fd = re.search('\{\{([^}]*)\}\}', trans, re.UNICODE)
            if fd:
                try:
                    return fd.group(1).split('|')[1]
                except IndexError as e:
                    self.wiktionary.log_handler.error("IndexError in entity " + trans.encode('utf8'))
        #TODO fix [[kanojo]] [kanojo]
        trans = re.sub('\'\'+[^\']*\'+', '', trans)
        trans = re.sub('""+[^"]*"+', '', trans)
        trans = re.sub('\{\{[^}]*\}\}', '', trans)
        trans = trans.replace('[', '')
        trans = trans.replace(']', '')
        trans = trans.replace('{', '')
        trans = trans.replace('}', '')
        trans = trans.split('|')[0]
        trans = trans.split('/')[0]
        return trans.strip()



class DefaultArticleParser(ArticleParser):

    def __init__(self, wikt, filter_langs=None):
        ArticleParser.__init__(self, wikt, filter_langs)
        self.tr_prefix_l = [i.decode('utf8') 
                            for i in self.cfg['translation_prefix'].split(',')]
        self.wc_field = int(self.cfg['wc_field'])
        self.word_field = int(self.cfg['word_field'])
        self.line_field = int(self.cfg['line_field'])
        self.rest_of_fields = int(self.cfg['rest_of_fields'])
        self.build_trad_re()

    def build_trad_re(self):
        re_str = '\{\{(' + '|'.join(self.tr_prefix_l) + ')\|([^}]+)\}\}'
        self.trad_re = re.compile(ur'' + re_str, re.UNICODE)

    def get_pairs(self, text):
        translations = defaultdict(list)
        m = self.trad_re.finditer(text)
        if m:
            for t in m:
                pairs = self.unpack_trad_regex(t)
                if not pairs:
                    continue
                for fields in pairs:
                    if not fields:
                        continue
                    if fields[0] and fields[1]:
                        translations[fields[0]].append(fields[1]) 
        return translations

    def unpack_trad_regex(self, match):
        line = match.group(self.line_field)
        if self.skip_translation_line(line):
            return []
        if match.groups() < 2:
            return []
        current_pairs = list()
        fields = match.group(self.rest_of_fields).split('|')
        if len(fields) < 2:
            return []
        wc = fields[self.wc_field].strip()
        word = fields[self.word_field].strip()
        #FIXME dirty workaround for the Spanish Wiktionary
        if word.replace(',', '').replace(u'\u2013','').replace('-', \
              '').replace(u'\u2014', '').replace(' ', '').isdigit():
            if len(fields) > self.word_field + 1:
                word = fields[self.word_field+1].strip()
            else:
                return []
        if not wc or not word:
            return []
        if self.skip_translation_re and self.skip_translation_re.search(word):
            return []
        if wc in self.wikicodes and not wc == self.wc:
            current_pairs.append([wc, word])
        return current_pairs

