from flask.sessions import SessionInterface, SessionMixin


class MySessionInterface(SessionInterface):

    def open_session(self, app, request):
        # return Session(dict, SessionMixin)
        return None

    def save_session(self, app, session,response):
        pass