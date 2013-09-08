#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
                       _
                      | |
 _ __  _   _ _ __ __ _| |_ ___
| '_ \| | | | '__/ _` | __/ _ \\
| |_) | |_| | | | (_| | ||  __/
| .__/ \__, |_|  \__,_|\__\___|
| |     __/ |
|_|    |___/

Usage:
  pyrate <service> <command>
  pyrate config <service> <variable>=<value>...
  pyrate (-h | --help)
  pyrate --version

Options:
  -h --help     Show this screen.
"""

from pyrate import __version__
import pyrate.services
import pkgutil
from docopt import docopt
import json
from os.path import expanduser


def main():
    args = docopt(__doc__, version='Pyrate ' + __version__)
    services = []
    s = None
    sn = args['<service>']  # service name
    sp = "pyrate.services." + sn  # service path
    sc = sn.title() + "Pyrate"  # service class name
    config_path = expanduser("~") + '/.pyrate'

    for importer, modname, ispkg in pkgutil.iter_modules(pyrate.services.__path__):
        services.append(modname)

    try:
        __import__(sp)
    except ImportError:
        print("Could not import service '" + sn + "'. These are the available services:")
        for service in services:
            print("- " + service)
        exit()

    # load config file
    try:
        config = json.load(open(config_path))
    except IOError:
        raise IOError("Config file could not be loaded!")

    cmd = "s = %s" % sp + "." + sc + "("
    for key, val in config[sn]:
        # FIXME: ValueError: too many values to unpack
        cmd += key + "='" + val + "',"
    cmd = cmd[:-1]
    cmd += ")"
    print cmd
    exec(cmd)

    if args['config']:
        # TODO: Finish function
        try:
            cmd = "s = %s" % sp + "." + sc + "("
            for arg in args["<variable>=<value>"]:
                parts = arg.split('=')
                cmd += parts[0] + "='" + parts[1] + "',"
            cmd = cmd[:-1]
            cmd += ")"
            exec(cmd)
        except TypeError:
            # FIXME: Add better check for required params
            raise TypeError("Invalid Parameters given. Please check the Documentation online.")

        # FIXME: process it to right format, only overwrite same entries..
        config = ''
        # store it
        json.dump(config, open(config_path, 'w+'))

    else:
        # TODO: There's lots..
        print s.do(args['<command>'])

# debugging
if __name__ == '__main__':
    main()
