# -*- coding: utf-8 -*-

from wsgiproxy.app import WSGIProxyApp


def lister(value):
    if value is None:
        return None
    if isinstance(value, (list, set, tuple)):
        return value
    return [v.strip() for v in value.split(',')]


def logger(app):
    def caller(environ, start_response):
        print caller
        return app(environ, start_response)
    return caller


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
    return logger(application)
