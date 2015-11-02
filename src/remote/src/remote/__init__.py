# -*- coding: utf-8 -*-

from wsgiproxy.app import WSGIProxyApp


def lister(value):
    if value is None:
        return None
    return [v.strip() for v in value.split(',')]


def make_proxy(href, secret_file=None, string_keys=None, unicode_keys=None,
               json_keys=None, pickle_keys=None, **kwargs):
    
    application = WSGIProxyApp(
        href,
        secret_file=secret_file,
        string_keys=lister(string_keys),
        unicode_keys=lister(unicode_keys),
        json_keys=lister(json_keys),
        pickle_keys=lister(pickle_keys),
    )
    return application
