import urllib2

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse

from django.contrib.auth.models import User

from messaging.models import Message

def index(request):
    newest_users = User.objects.filter(is_active=True).order_by('-date_joined')
    newest_messages = Message.objects.order_by('-timestamp')
    context = {
        'newest_users': newest_users,
        'newest_messages': newest_messages,
    }
    return render_to_response('index.html', context,
        context_instance=RequestContext(request))
