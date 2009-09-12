#!/usr/bin/env python

import multiprocessing
import optparse

from hurricane.utils import run_until_stopped, import_string

def main(settings):
    manager = import_string(settings.APPLICATION_MANAGER)
    app_manager = manager.ApplicationManager(settings)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings', dest='settings',
        default='hurricane.default_settings')

    options, args = parser.parse_args()
    settings = import_string(options.settings)
    main(settings)
