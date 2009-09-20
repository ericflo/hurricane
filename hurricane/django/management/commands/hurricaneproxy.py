from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.resource import Resource

from django.core.management.base import BaseCommand

class ProxyResource(Resource):
    def getChild(self, path, request):
        if path.startswith('comet'):
            return proxy.ReverseProxyResource('localhost', 8001, '/comet')
        elif path.startswith('global'):
            return proxy.ReverseProxyResource('localhost', 8001, '/global')
        return proxy.ReverseProxyResource('localhost', 8000, '/' + path)

class Command(BaseCommand):

    def handle(self, *args, **options):
        root = ProxyResource()
        reactor.listenTCP(8080, server.Site(root))
        reactor.run()