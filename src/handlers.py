from ConfigParser import ConfigParser, NoSectionError
from sys import stderr
import logging

class ConfigHandler(object):

    def __init__(self, wc, cfg_fn):
        self.wc = wc
        c_parser = ConfigParser()
        c_parser.read(cfg_fn)
        self.cfg_general = dict([t for t in c_parser.items('general')])
        self.read_specific_config(c_parser)
        self.add_missing_params()
        self.convert_bool_params()

    def read_specific_config(self, c_parser):
        try:
            cfg_wc = dict([t for t in c_parser.items(self.wc)])
            self.cfg_wc = dict()
            for param, value in self.cfg_general.iteritems():
                if not param in cfg_wc:
                    self.cfg_wc[param] = value
            for param, value in cfg_wc.iteritems():
                self.cfg_wc[param] = value
        except NoSectionError:
            self.cfg_wc = self.cfg_general
        except Exception as e:
            stderr.write(e)

    def add_missing_params(self):
        f = open(self.cfg_wc['defaults'])
        for l in f:
            param, value = l.decode('utf8').strip().split('=')
            if not param in self.cfg_wc:
                self.cfg_wc[param] = value
        f.close()

    def convert_bool_params(self):
        bool_params = [('uses_specific_logfile', False)]
        for param, value in bool_params:
            if param in self.cfg_wc:
                self.cfg_wc[param] = self.bool_parse(self.cfg_wc[param])
            else:
                self.cfg_wc[param] = value

    def bool_parse(self, value):
        if value.strip().lower() in ['yes', '1', 'true']:
            return True
        return False

    def get_config(self):
        return self.cfg_wc

    def __getitem__(self, item):
        if item in self.cfg_wc:
            return self.cfg_wc[item]
        else:
            return None
    #def check_all_files
    
class LogHandler(object):

    def __init__(self, wc, cfg):
        self.logger = logging.getLogger(cfg['logger'])
        self.logger.setLevel(int(cfg['loglevel']))
        fh = logging.FileHandler(cfg['logfile'])
        formatter = logging.Formatter('%(levelname)s - %(module)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log_msg(self, msg, level):
        self.logger.log(level, msg)

    def info(self, msg):
        self.logger.log(logging.INFO, msg)

    def debug(self, msg):
        self.logger.debug(logging.DEBUG, msg)

    def error(self, msg):
        self.logger.error(logging.ERROR, msg)



