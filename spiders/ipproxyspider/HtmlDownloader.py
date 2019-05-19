
import random
from until import config
from until.helptool import HelpTool
import json
from db.ipproxydb.DataStore import sqlhelper


import requests
import chardet


class Html_Downloader(object):
    @staticmethod
    def download(url):
        try:
            r = requests.get(url=url, headers=HelpTool().get_header(), timeout=config.TIMEOUT)
            #r.encoding = chardet.detect(r)['encoding']
            print(r.text)
            if (not r.ok) or len(r.text) < 500:
                raise ConnectionError
            else:
                return r.text.encode("utf-8",ingore=False)

        except Exception:
            count = 0  # 重试次数
            proxylist = sqlhelper.select(10)
            if not proxylist:
                return None

            while count < config.RETRY_TIME:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=HelpTool().get_header(), timeout=config.TIMEOUT, proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None
