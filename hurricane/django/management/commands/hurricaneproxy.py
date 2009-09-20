from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.resource import Resource

from django.core.management.base import BaseCommand

class ProxyResource(Resource):
    def getChild(self, path, request):
        if path.startswith('comet'):
            return proxy.ReverseProxyResource('localhost', settings.COMET_PORT, '/comet')
        elif path.startswith('global'):
            return proxy.ReverseProxyResource('localhost', settings.COMET_PORT, '/global')
        return proxy.ReverseProxyResource('localhost', 8080, '/' + path)

class Command(BaseCommand):

    def handle(self, *args, **options):
        root = ProxyResource()
        reactor.listenTCP(8000, server.Site(root))
        reactor.run()
