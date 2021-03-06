#!/usr/bin/env python

import optparse

from hurricane.utils import import_string

def runcli():
    parser = optparse.OptionParser()
    parser.add_option('--settings', dest='settings',
        default='hurricane.default_settings')

    options, args = parser.parse_args()
    settings = import_string(options.settings)
    main(settings)


def main(settings):
    manager = import_string(settings.APPLICATION_MANAGER)
    app_manager = manager.ApplicationManager(settings)
    try:
        app_manager.run()
    except KeyboardInterrupt:
        print "interrupted"

if __name__ == '__main__':
    runcli()
