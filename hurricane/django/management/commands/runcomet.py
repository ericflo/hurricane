from subprocess import Popen
import sys
from multiprocessing import Process
 
from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.resource import Resource
 
from django.core.management.base import BaseCommand
from django.conf import settings
 
from hurricane.runner import main

class ProxyResource(Resource):
    def getChild(self, path, request):
        if path.startswith('comet'):
            return proxy.ReverseProxyResource('localhost', settings.COMET_PORT, '/comet')
        elif path.startswith('global'):
            return proxy.ReverseProxyResource('localhost', settings.COMET_PORT, '/global')
        return proxy.ReverseProxyResource('localhost', 8080, '/' + path)

def start_proxy():
    root = ProxyResource()
    reactor.listenTCP(8000, server.Site(root))
    reactor.run()
 
class Command(BaseCommand):
    help = ("Starts a lightweight Comet server, and django development server "
        "for development.")
 
    def handle(self, *args, **options):
        Popen([
            sys.executable,
            sys.argv[0],
            'runserver',
            '0.0.0.0:8080',
            '--settings=%s' % settings.SETTINGS_MODULE
        ])
        Process(target=start_proxy).start()
        
        main(settings)
