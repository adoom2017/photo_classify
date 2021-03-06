#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config as HachoirConfig

from sys import argv, stderr, exit

HachoirConfig.quiet = True

class Metadata:
    def __init__(self, path):
        self.path = path

    def getCreateTime(self):
        parser = createParser(self.path)
        if not parser:
            logging.error("Unable to parse file %s." % self.path)
            return None

        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception as err:
                logging.error("File %s metadata extraction error: %s." % (self.path, err))
                metadata = None

        if not metadata:
            logging.error("Unable to extract metadata from file %s." % self.path)
            return None

        mime_type = metadata.getValues("mime_type")[0]
        if "video" in mime_type:
            create_times = metadata.getValues("creation_date")
        elif "image" in mime_type:
            create_times = metadata.getValues("date_time_original")
        else:
            create_times = None
        
        if len(create_times) > 0:
            return create_times[0].strftime("%Y%m%d_%H%M%S")

        return None
