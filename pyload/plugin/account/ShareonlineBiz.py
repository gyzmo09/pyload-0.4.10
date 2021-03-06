# -*- coding: utf-8 -*-

import re

from pyload.plugin.Account import Account


class ShareonlineBiz(Account):
    __name    = "ShareonlineBiz"
    __type    = "account"
    __version = "0.33"

    __description = """Share-online.biz account plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    def api_response(self, user, req):
        return req.load("http://api.share-online.biz/cgi-bin",
                        get={'q'       : "userdetails",
                             'aux'     : "traffic",
                             'username': user,
                             'password': self.getAccountData(user)['password']})


    def loadAccountInfo(self, user, req):
        premium     = False
        validuntil  = None
        trafficleft = -1
        maxtraffic  = 100 * 2 ** 30  #: 100 GB

        api = {}
        for line in self.api_response(user, req).splitlines():
            if "=" in line:
                key, value = line.split("=")
                api[key] = value

        self.logDebug(api)

        if api['a'].lower() != "not_available":
            req.cj.setCookie("share-online.biz", 'a', api['a'])

            premium = api['group'] in ("PrePaid", "Premium", "Penalty-Premium")

            validuntil = float(api['expire_date'])

            traffic     = float(api['traffic_1d'].split(";")[0])

            if maxtraffic > traffic:
                trafficleft = maxtraffic - traffic
            else:
                trafficleft = -1

        return {'premium'    : premium,
                'validuntil' : validuntil,
                'trafficleft': trafficleft,
                'maxtraffic' : maxtraffic}


    def login(self, user, data, req):
        html = self.api_response(user, req)
        err  = re.search(r'\*\*(.+?)\*\*', html)
        if err:
            self.logError(err.group(1))
            self.wrongPassword()
