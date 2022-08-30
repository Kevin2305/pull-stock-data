#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import date
class MyLoggerClass(object):
    def __init__(self, loggername: str, filename: str, level = 'warn', moreoutput = 1) -> None:
        '''loggername = app name in log file, filename = a full file path / a file name'''
        self._logger = logging.getLogger(loggername)
        self.filename = filename
        self.filehandler = logging.FileHandler(filename=self.filename,encoding="utf-8",delay=False)
        self.startstophandler = logging.FileHandler(filename=self.filename,encoding="utf-8",delay=False)
        self._logger.setLevel(logging.DEBUG)
        self.setLogLevel(level)
        self.startstophandler.setLevel(logging.INFO)
        datefmt = "%Y-%m-%d %H:%M:%S"
        fmt = "%(asctime)s.%(msecs)03d %(name)s %(levelname)s : %(message)s"
        logfmt = logging.Formatter(fmt=fmt,datefmt=datefmt)
        self.filehandler.setFormatter(logfmt)
        self.startstophandler.setFormatter(logfmt)
        self.moreoutput = moreoutput

    def setLogLevel(self, level: str):
        '''level = critical / debug / warn / error / info'''
        if level.lower() == "critical":
            self.filehandler.setLevel(logging.CRITICAL)
            self.currlevel = 'CRITICAL'
        if level.lower() == "debug":
            self.filehandler.setLevel(logging.DEBUG)
            self.currlevel = 'DEBUG'
        if level.lower() == "warn":
            self.filehandler.setLevel(logging.WARN)
            self.currlevel = 'WARN'
        if level.lower() == "error":
            self.filehandler.setLevel(logging.ERROR)
            self.currlevel = 'ERROR'
        if level.lower() == "info":
            self.filehandler.setLevel(logging.INFO)
            self.currlevel = 'INFO'

    def startLogger(self):
        if self.moreoutput:
            self._logger.addHandler(self.startstophandler)
            self._logger.info("log service started with level {}".format(self.currlevel))
            self._logger.removeHandler(self.startstophandler)
        self._logger.addHandler(self.filehandler)

    def stopLogger(self):
        self._logger.removeHandler(self.filehandler)
        self.filehandler.close()
        if self.moreoutput:
            self._logger.addHandler(self.startstophandler)
            self._logger.info("log service stopped with level {}".format(self.currlevel))
        self.startstophandler.close()
        

    def restartLogger(self, level):
        '''level = critical / debug / warn / error / info'''
        self._logger.removeHandler(self.filehandler)
        self.setLogLevel(level)
        self.startLogger()

    def writeCriticalLog(self, msg):
        self._logger.critical(msg)

    def writeErrorLog(self, msg):
        self._logger.error(msg)

    def writeWarnLog(self, msg):
        self._logger.warning(msg)

    def writeDebugLog(self, msg):
        self._logger.debug(msg)

    def writeInfoLog(self, msg):
        self._logger.info(msg)
