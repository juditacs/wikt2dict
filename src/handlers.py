from ConfigParser import ConfigParser, NoSectionError
from sys import stderr
import logging

class ConfigHandler(object):
    """ Configuration handler class
    An instance of this class is created for all Wiktionary instances.
    In the configuration file there should be a section named 'general'
    and optionally a section named as the Wiktionary code of the
    language. Parameters in the latter override parameters from the
    general section. Another defaults file can be specified where
    global defaults are placed. """

    def __init__(self, wc, cfg_fn):
        """ 
        @param wc: Wiktionary code
        @param cfg_fn: path and name of the configuration file
        """
        self.wc = wc
        c_parser = ConfigParser()
        c_parser.read(cfg_fn)
        self.cfg_general = dict([t for t in c_parser.items('general')])
        if not wc == "general":
            self.read_specific_config(c_parser)
            self.add_missing_params()
            self.convert_bool_params()
        else:
            self.cfg_wc = self.cfg_general

    def read_specific_config(self, c_parser):
        """ Read the specific section named as the Wiktionary code
        in the config file. """
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
        """ Read defaults file """
        f = open(self.cfg_wc['defaults'])
        for l in f:
            param, value = l.decode('utf8').strip().split('=')
            if not param in self.cfg_wc:
                self.cfg_wc[param] = value
        f.close()

    def convert_bool_params(self):
        """ Convert string parameters to boolean """
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
    """ A simple wrapper class for the logging module """

    def __init__(self, cfg):
        self.logger = logging.getLogger(cfg['logger'])
        self.logger.setLevel(int(cfg['loglevel']))
        if not self.logger.handlers:
            fh = logging.FileHandler(cfg['logfile'])
            formatter = logging.Formatter('%(levelname)s - %(module)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def log_msg(self, msg, level):
        self.logger.log(level, str(msg))

    def info(self, msg):
        self.logger.log(logging.INFO, str(msg))

    def debug(self, msg):
        self.logger.log(logging.DEBUG, str(msg))

    def error(self, msg):
        self.logger.log(logging.ERROR, str(msg))



