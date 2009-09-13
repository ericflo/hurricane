from datetime import datetime
import threading
import uuid
import Cookie

import simplejson

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.handlers.base import BaseHandler
from hurricane.base import Message
from hurricane.utils import HttpResponse, json_timestamp, import_string

from django.contrib.auth.models import User

from socialgraph.models import UserLink

def get_session_id_from_req(request):
    # TODO: Remove hateful nesting
    session_id = ''
    if 'Cookie' in request.headers:
        cookies = Cookie.BaseCookie()
        cookies.load(request.headers['Cookie'])
        if 'sessionid' in cookies:
            session_id = cookies['sessionid'].value
    return session_id

class CometHandler(BaseHandler):
    def initialize(self):
        self.requests = []
        self.response_queues = []
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.session_engine = engine = import_string(self.settings.SESSION_ENGINE)

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'id': str(uuid.uuid4()),
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        self.respond_to_requests(msg)

    def handle_request(self, request):
        # TODO: Make the query parts async (create a handler to get sessionid/userinfo/socialgraph stuff?)
        # TODO: Remove hateful nesting
        if request.method == 'POST':
            session_id = get_session_id_from_req(request)
            if session_id:
                session = self.session_engine.SessionStore(session_id)
                user_id = session.get('_auth_user_id')
                if user_id:
                    data = simplejson.loads(request.body)
                    data['user'] = int(user_id)
                    self.publish(Message('hubbub', datetime.now(), data))
            try:
                request.write(HttpResponse(201).as_bytes())
            except (IOError, AssertionError):
                return
            request.finish()
        else:
            self.requests.append(request)
    
    def should_respond(self, request, msg):
        # TODO: Make the query parts async (create a handler to get sessionid/userinfo/socialgraph stuff?)
        session_id = get_session_id_from_req(request)
        if not session_id:
            return False
        session = self.session_engine.SessionStore(session_id)
        user_id = session.get('_auth_user_id')
        if not user_id:
            return False
        user = User.objects.get(id=user_id)
        user_ids_following_user = list(UserLink.objects.filter(to_user=user)\
            .values_list('from_user', flat=True))
        user_ids_following_user.append(user_id)
        if msg['raw_data']['user'] in user_ids_following_user:
            return True
        return False

    def respond_to_requests(self, msg):
        # TODO: Come up with a way to remove old, stale, requests
        print "REQUESTS:", [r.uri + '\n' for r in self.requests]
        for i, request in enumerate(self.requests):
            request = self.requests[0]
            if self.should_respond(request, msg):
                # Remove the request from the list of active requests
                del self.requests[i]
                # Now, respond to it
                json = simplejson.dumps({'messages': [msg]})
                response = HttpResponse(200, 'application/json', json)
                try:
                    request.write(response.as_bytes())
                except (IOError, AssertionError):
                    return
                request.finish()
