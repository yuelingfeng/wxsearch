# -*- coding: utf-8 -*-

from json import load
import urllib
from urllib.request import urlopen

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

_server_url = 'https://api.weixin.qq.com/sns'

def getOpenID(jscode):
    try:
        _appid = 'wx58ef76cb94a2c048'
        _secret = '947953bc018078b245d0d97bba95d1c1'
        _url = _server_url + u'/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (_appid,_secret,jscode)
        
        _result = urlopen(_url)
        _res = load(_result)
        _res['code'] = '0'
        return _res

    except Exception as e:
        return { 'code':'-1',
            'msg' : 'urlexts.getOpenID error %s' % e
            }
