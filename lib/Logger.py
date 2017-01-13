# -*- coding: utf-8 -*-
import logging


class Logger():
    formatter = logging.Formatter(
        '%(levelname)s | %(asctime)s | %(name)s | %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')

    def __init__(self, logname, loglevel="INFO"):
        self.logger = logging.getLogger(logname)
        parse_log_level = self.parse_log_level(loglevel)
        self.logger.setLevel(parse_log_level)
        self._init_stream_hanlder(parse_log_level)

    def parse_log_level(self, loglevel):
        return getattr(logging, loglevel.upper(), logging.INFO)

    def _init_stream_hanlder(self, parse_loglevel):
        ch = logging.StreamHandler()
        ch.setLevel(parse_loglevel)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
