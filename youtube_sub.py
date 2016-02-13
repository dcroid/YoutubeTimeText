#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'Youtube Time Text'
__date__ = ''
__author__ = 'andreyteterevkov'


from grab import Grab
import re
import urllib
import url_parsing
import xmltodict
import json

grab = Grab()
grab.go('https://www.youtube.com/watch?v=pnnDz1DBUKo')

p = re.compile(ur'caption_tracks":\"(.*?)\"', re.IGNORECASE | re.DOTALL)
for script in grab.doc.select('//script').text_list():
    if 'ytplayer.config' in script:
        url = re.search(p, script).group(1).split('u=')[1]
        url = urllib.unquote(url).decode('utf8')
        url = urllib.unquote(url).decode('utf8').replace('\u0026', '&')
        u = url_parsing.Url(url)
        try:
            del (u.query['v'])
            url = u.url
        except:
            pass

        grab.go(url)

        o = xmltodict.parse(grab.doc.select('//*').html())
        print json.dumps(o)


