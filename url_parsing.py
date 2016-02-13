#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'test'
__date__ = ''
__author__ = 'andreyteterevkov'

import cgi, urllib, urlparse

class Url(object):
    """
    Helper class to help add/remove GET args from an existing URL.

    Usage:
    url = Url('http://www.koonkii.com/apps/?type=Android&page=5#top')
    del url.args['type']
    print url.url
    >>> 'http://www.koonkii.com/apps/?page=5#top'

    @see http://stackoverflow.com/questions/2873438/is-there-a-better-way-to-write-this-url-manipulation-in-python
    """
    def __init__(self, url):
        """
        Construct from a string, Url object or Django's HttpRequest.
        """
        if isinstance(url, Url):
            url = url.url

        # Django HTTP request
        try:
            from django.http import HttpRequest
            if isinstance(url, HttpRequest):
                url = url.get_full_path()
        except ImportError:
            pass

        # http://, www.koonkii.com, /apps/, ?, {'type':'Android','page':'5'}, top
        self.scheme, self.domain, self.path, self.params, self.query, self.fragment = urlparse.urlparse(url)
        self.args = dict(cgi.parse_qsl(self.query))

    @property
    def url(self):
        return str(self)

    @property
    def query_string(self):
        """
        Returns args as a query string
        """
        args = dict(self.args)

        # Must be encoded in UTF-8
        for k, v in args.items():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                v.decode('utf8')
            args[k] = v

        # In case we've modified args
        self.query = urllib.urlencode(args)
        return '?%s' % self.query if len(self.args) else ''

    def __str__(self):
        """
        Turn back into a URL and special-case the %UID%

        URLs are not UTF-8 compatible and non-ascii characters should be url-encoded.
        """
        self.query = urllib.urlencode(self.args)
        return "%s" % urlparse.urlunparse((self.scheme, self.domain, self.path, self.params, self.query, self.fragment))