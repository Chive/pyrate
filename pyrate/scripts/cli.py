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
    pyrate do <service> <command>
    pyrate do <service> (get|post|put|delete|options) <target>
    pyrate config set <service> <variable>=<value>...
    pyrate config reset
    pyrate list [-a]
    pyrate (-h | --help)
    pyrate --version

Options:
    -H --head=<c>  Request Header content
    -B --body=<c>   Request Body content
    -h --help           Show this screen.
"""
from pyrate import __version__
import pyrate.services
import pkgutil
from docopt import docopt
import json
from os.path import expanduser

CONFIG_PATH = expanduser("~") + '/.pyrate'


def update_config(config, service):
    loaded = load_from_file(None)
    updated = dict()
    updated[service] = config
    loaded.update(updated)
    write_config(loaded)


def init_config():
    template = json.loads(open('credentials.template.json').read())
    write_config(template)


def write_config(config):
    with open(CONFIG_PATH, 'w+') as file:
        json.dump(config, file)


def load_from_file(servicename):
    try:
        with open(CONFIG_PATH) as f:
            # check if file is empty
            if not f.read():
                f.close()
                init_config()
    except IOError:
        init_config()

    c = json.loads(open(CONFIG_PATH).read())
    if not servicename:
        return c

    else:
        return c[servicename]


def load_config(servicename):
    sp = "pyrate.services." + servicename
    try:
        __import__(sp)
    except ImportError:
        text = "Could not import service '" + servicename + "'.\nThese are the available services: \n"
        for importer, modname, ispkg in pkgutil.iter_modules(pyrate.services.__path__):
            text += " - " + modname + "\n"
        raise ImportError(text.rstrip("\n"))

    return load_from_file(servicename)


def check_config(config):
    for k in config:
        if not config[k]:
            return False

    return True


def main():
    args = docopt(__doc__, version='Pyrate ' + __version__)
    print("WARNING: THIS IS HEAVILY EXPERIMENTAL AND UNTESTED")
    s = args['<service>']
    if args['config']:
        if args['reset']:
            init_config()
            print("Reset config")

        elif args['set']:
            conf = load_config(s)
            for arg in args["<variable>=<value>"]:
                key, value = arg.split('=')
                try:
                    if key in conf:
                        conf[key] = value
                except KeyError:
                    raise Exception("Invalid key")

            update_config(conf, s)
            print("Stored " + str(len(args["<variable>=<value>"])) + " values in config")

    elif args['do']:
        conf = load_config(s)
        if check_config(conf):
            cmd = "pyrate.services." + s + "." + s.title() + "Pyrate("
            for k in conf:
                cmd += "'" + conf[k] + "',"

            cmd = cmd.rstrip(",") + ")"
            c = eval(cmd)
            print json.dumps(c.do(args['<command>'], content=args['--body'], headers=args['--head']))
        else:
            print("Please set your config using 'pyrate config set'")

    elif args['list']:
        print("Available services:")
        for importer, modname, ispkg in pkgutil.iter_modules(pyrate.services.__path__):
            text = " - " + modname
            if args['-a']:
                text += " (pyrate.services." + modname + "." + modname.title() + "Pyrate)"
            print text

# debugging
#if __name__ == '__main__':
#    main()
