#!/usr/bin/python2.7

import cStringIO
from ConfigParser import SafeConfigParser
import json
import os


class Settings:

    def __init__(self, settings_type=None):
        """ Initialize a Settings object as public or private. """

        if settings_type == "private":
            filename = "settings_private.cfg"
        else:
            filename = "settings.cfg"

        self.config = SafeConfigParser()
        self.config.readfp(open(filename))
        self.config.settings_type = settings_type
        self.config.file_path = os.path.abspath(filename)


    def get(self, section, key):
        """ Gets a value. Tries to do some duck-typing. """

        raw_value = self.config.get(section,key)
        if raw_value in ["True","False"]:
            return self.config.getbool(section,key)
        else:
            try:
                return self.config.getint(section,key)
            except:
                pass

        return raw_value


    def jsonify(self):
        """ Renders the config object as JSON. """

        d = {}
        for section in self.config.sections():
            d[section] = {}
            for option in self.config.options(section):
                d[section][option] = self.get(section,option)   # use the custom get() method
        self.config.json = json.dumps(d)


    def json_file(self):
        """ Returns a cStringIO object that looks like a file object. """

        self.jsonify()
        s_file = cStringIO.StringIO()
        s_file.write(self.config.json)
        s_file.seek(0)
        return s_file


if __name__ == "__main__":
    S = Settings()
