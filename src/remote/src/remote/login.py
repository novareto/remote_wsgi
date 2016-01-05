# -*- coding: utf-8 -*-

from webob import Response, Request
from webob.exc import HTTPFound
from repoze.who.api import get_api

template = """
<html>
<body>
  <p>
    <form action="/dologin" method="POST">
      Username: <input type="text" name="login" value="" />
      <br />
      Password: <input type="password" name="password" value ="" />
      <br />
      <input type="submit" name="form.login" value="login" />
    </form>
  </p>
</body>
</html>
"""


class PortalsLoginPlugin(object):

    def try_login(self, hub, username, password):
        for path_info, app in hub.applications:
            method = getattr(app, 'login_method', None)
            if method is not None:
                print app, method
            else:
                print app, 'NO LOGIN'
        return None

    def authenticate(self, environ, identity):
        """Return username or None.
        """
        try:
            username = identity['login']
            password = identity['password']
            hub = environ['remote.hub']
        except KeyError:
            return None
        return self.try_login(hub, username, password)

    def add_metadata(self, environ, identity):
        username = identity.get('repoze.who.userid')
        if username is not None:
            identity['user'] = dict(
                username = username,
                name = 'Mr Foo',
            )


def login_app(environ, start_response):
    response = Response()
    identity = environ.get('repoze.who.identity')
    if identity is not None:
        came_from = params.get('came_from', None)
        if came_from:
            response.status = '304 Not Modified'
            response.location = str(came_from)
            return response(environ, start_response)

    response.write(template)
    return response(environ, start_response)


def login_center(hub):
    def login_view(environ, start_response):
        message = ''
        who_api = get_api(environ)
        request = Request(environ)
        environ['remote.hub'] = hub

        if 'form.login' in request.POST:
            creds = {}
            creds['login'] = request.POST['login']
            creds['password'] = request.POST['password']
            authenticated, headers = who_api.login(creds)
            if authenticated:
                return HTTPFound(location='/', headers=headers)

            message = 'Invalid login.'
        else:
            # Forcefully forget any existing credentials.
            _, headers = who_api.login({})

        request.response_headerlist = headers
        if 'REMOTE_USER' in request.environ:
            del request.environ['REMOTE_USER']

        return Response(message)(environ, start_response)
    return login_view
