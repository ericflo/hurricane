import mimetypes
import os

from hurricane.utils import HttpResponse

def get_media_view(base_path, url_part):
    def media(request):
        path = os.path.join(base_path, request.path[len(url_part):].lstrip('/'))    
        try:
            f = open(path).read()
        except (OSError, IOError):
            path = os.path.join(path, 'index.html')
            try:
                f = open(path).read()
            except (OSError, IOError):
                request.write(HttpResponse(404).as_bytes())
                request.finish()
                return
        (content_type, encoding) = mimetypes.guess_type(path)
        length = len(f)
        request.write(HttpResponse(200, content_type, f).as_bytes())
        request.finish()
    return media