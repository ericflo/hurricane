from django.conf import settings

def comet_url(request):
    return {
        'COMET_URL': settings.COMET_URL,
    }
