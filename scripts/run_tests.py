#!/usr/bin/env python3
from os.path import dirname
from os.path import join
import os
import sys

from nose.plugins.base import Plugin
import nose


os.chdir(join(dirname(__file__), os.pardir, 'tests'))


class ExtensionPlugin(Plugin):
    name = "ExtensionPlugin"

    def options(self, parser, env):
        Plugin.options(self,parser,env)

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.enabled = True

    def wantFile(self, file):
        return file.endswith('.py')

    def wantDirectory(self,directory):
        return True

    def wantModule(self,file):
        return True


if __name__ == '__main__':
    include_dirs = ["-w", "."]
    nose.main(addplugins=[ExtensionPlugin()],
        argv=sys.argv.extend(include_dirs))
