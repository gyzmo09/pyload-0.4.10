# -*- coding: utf-8 -*-

import time

from pyload.plugin.Account import Account
from pyload.utils import json_loads


class MyfastfileCom(Account):
    __name    = "MyfastfileCom"
    __type    = "account"
    __version = "0.04"

    __description = """Myfastfile.com account plugin"""
    __license     = "GPLv3"
    __authors     = [("stickell", "l.stickell@yahoo.it")]


    def loadAccountInfo(self, user, req):
        if 'days_left' in self.json_data:
            validuntil = time.time() + self.json_data['days_left'] * 24 * 60 * 60
            return {"premium": True, "validuntil": validuntil, "trafficleft": -1}
        else:
            self.logError(_("Unable to get account information"))


    def login(self, user, data, req):
        # Password to use is the API-Password written in http://myfastfile.com/myaccount
        html = req.load("http://myfastfile.com/api.php",
                        get={"user": user, "pass": data['password']})

        self.logDebug("JSON data: " + html)

        self.json_data = json_loads(html)
        if self.json_data['status'] != 'ok':
            self.logError(_('Invalid login. The password to use is the API-Password you find in your "My Account" page'))
            self.wrongPassword()
