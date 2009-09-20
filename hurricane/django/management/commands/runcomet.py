import os
from subprocess import Popen
import sys
from multiprocessing import Process

from twisted.internet import reactor
from twisted.web import proxy, server

from django.core.management.base import BaseCommand
from django.conf import settings

from hurricane.runner import main

def start_proxy():
    main_site = proxy.ReverseProxyResource('localhost', 8000, '')
    main_site.putChild('comet/',
        proxy.ReverseProxyResource('localhost', 8001, 'comet/'))
    reactor.listenTCP(8080, server.Site(main_site))
    reactor.run()

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
        Process(target=start_proxy).start()
        #Popen([
        #    sys.executable, 
        #    os.path.abspath(os.path.join(os.path.dirname(__file__),
        #        '..', '..', '..', 'runner.py')),
        #    '--settings=%s' % settings.SETTINGS_MODULE
        #])
        
        main(settings)