import os
from subprocess import Popen
import sys

from twisted.internet import reactor
from twisted.web import proxy, server

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = ("Starts a lightweight Comet server, and django development server "
        "for development.")

    def handle(self, *args, **options):
        Popen([
            sys.executable, 
            sys.argv[0], 
            'runserver', 
            '--settings=%s' % settings.SETTINGS_MODULE
        ])
        Popen([
            sys.executable, 
            os.path.abspath(os.path.join(os.path.dirname(__file__),
                '..', '..', '..', 'runner.py')),
            '--settings=%s' % settings.SETTINGS_MODULE
        ])
        
        main_site = proxy.ReverseProxyResource('localhost', 8000, '')
        main_site.putChild('comet/',
            proxy.ReverseProxyResource('localhost', 8001, 'comet/'))
        reactor.listenTCP(8080, server.Site(main_site))
        reactor.run()
