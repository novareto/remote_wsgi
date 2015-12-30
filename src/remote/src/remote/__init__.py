# -*- coding: utf-8 -*-

import json
from wsgiproxy.app import WSGIProxyApp
from barrel import cooper
from paste.urlmap import URLMap, parse_path_expression
from .resources import js, css

REALM = "grok"
USERS = [('admin', 'admin')]

auth = cooper.basicauth(users=USERS, realm=REALM)


def lister(value):
    if value is None:
        return None
    if isinstance(value, (list, set, tuple)):
        return value
    return [v.strip() for v in value.split(',')]


def wrapper(app):
    def caller(environ, start_response):
        js.need()
        css.need()
        return app(environ, start_response)
    return caller


def hub_factory(loader, global_conf, **local_conf):
    if 'not_found_app' in local_conf:
        not_found_app = local_conf.pop('not_found_app')
    else:
        not_found_app = global_conf.get('not_found_app')
    if not_found_app:
        not_found_app = loader.get_app(not_found_app, global_conf=global_conf)
    urlmap = RemoteHub(not_found_app=not_found_app)
    for path, app_name in local_conf.items():
        path = parse_path_expression(path)
        app = loader.get_app(app_name, global_conf=global_conf)
        urlmap[path] = app
    return urlmap


class HubDetails(object):

    def __init__(self, hub):
        self.hub = hub

    def __call__(self, environ, start_response):
        result = dict(self.hub.about(environ))
        response_body = json.dumps(result)
        status = '200 OK'
        response_headers = [('Content-Type', 'application/json'),
                            ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return [response_body]


class RemoteHub(URLMap):

    def about(self, environ):
        for (domain, app_url), app in self.applications:
            if app_url != '/__about__':
                yield (environ['HTTP_HOST'] + app_url,
                       getattr(app, 'title', app_url))

    def __init__(self, *args, **kwargs):
        URLMap.__init__(self, *args, **kwargs)
        self['/__about__'] = HubDetails(self)


def make_proxy(*global_conf, **local_conf):
    href = local_conf.get('href')
    secret_file = local_conf.get('secret_file')
    string_keys = lister(local_conf.get('string_keys'))
    unicode_keys = lister(local_conf.get('unicode_keys'))
    json_keys = lister(local_conf.get('json_keys'))
    pickle_keys = lister(local_conf.get('pickle_keys'))

    application = WSGIProxyApp(
        href,
        secret_file=secret_file,
        string_keys=string_keys,
        unicode_keys=unicode_keys,
        json_keys=json_keys,
        pickle_keys=pickle_keys,
    )
    app = wrapper(application)
    app.title = local_conf.get('title') or 'No title'
    return app
