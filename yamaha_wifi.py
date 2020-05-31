#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage: yamaha_wifi.py [-h] -c CONF ADDR

WLX にログインしてAmazon の購入履歴データから，時系列グラフを生成します．

Arguments:
  ADDR              WLX402/WLX312 IP アドレス

Options:
  -f CONF           ログイン情報を記載した YAML ファイル

CONF には次の形式で，ログインするためのユーザ名とパスワードを記載しておく．

USER: 「ユーザ名」
PASS: 「パスワード」
"""

from docopt import docopt

import yaml
import urllib.request
import base64
import re
from lxml import html

class wlx402:
    ITEM_MAP = [
        [ 'システム情報', 	'CPU稼働率',	'cpu_usage' ],
        [ 'システム情報', 	'メモリ使用率', 'mem_usage' ],
        [ 'システム情報', 	'筐体内温度',   'temperature'],
        [ '無線情報 (2.4GHz)', 	'接続端末台数', '2ghz_client'],
        [ '無線情報 (5GHz)', 	'接続端末台数', '5ghz_client'],
    ]
    def gen_url(addr):
        return 'http://{0:s}/cgi-bin/admin/manage-system.sh'.format(addr)
    def get_map(page):
        value_map = {}
        for item_def in wlx402.ITEM_MAP:
            xpath = '//h3//*[contains(text(), "{0:s}")]/../..//td[contains(text(), "{1:s}")]/../td[2]'.format(
                item_def[0], item_def[1]
            )
            value = page.xpath(xpath)[0].text.strip()
            value_map[item_def[2]] = re.search('[0-9.]*', value).group()
        return value_map
        
def get_data(addr, device, login_config):
    url = device.gen_url(addr)
    
    token = base64.b64encode('{}:{}'.format(config['USER'],
                                            config['PASS']).encode('utf-8'))
    req = urllib.request.Request(
        url, 
        headers={'Authorization': 'Basic ' + token.decode('utf-8')}
    )
    page = html.fromstring(urllib.request.urlopen(req).read())

    return device.get_map(page)


conf_file = docopt(__doc__).get('CONF')
addr = docopt(__doc__).get('ADDR')

config = yaml.load(open(conf_file, 'r'), Loader=yaml.BaseLoader)
addr = '192.168.2.10'
data = get_data(addr, wlx402, config)

print(data)


                                          
                                          
