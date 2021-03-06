# -*- coding: utf-8 -*-

from pyload.plugin.internal.SimpleCrypter import SimpleCrypter


class XFSCrypter(SimpleCrypter):
    __name    = "XFSCrypter"
    __type    = "crypter"
    __version = "0.09"

    __pattern = r'^unmatchable$'

    __description = """XFileSharing decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    HOSTER_DOMAIN = None

    URL_REPLACEMENTS = [(r'&?per_page=\d+', ""), (r'[?/&]+$', ""), (r'(.+/[^?]+)$', r'\1?'), (r'$', r'&per_page=10000')]

    LINK_PATTERN = r'<(?:td|TD).*?>\s*(?:<.+>\s*)?<a href="(.+?)".*?>.+?(?:</a>)?\s*(?:<.+>\s*)?</(?:td|TD)>'
    NAME_PATTERN = r'<[Tt]itle>.*?\: (?P<N>.+) folder</[Tt]itle>'

    OFFLINE_PATTERN      = r'>\s*\w+ (Not Found|file (was|has been) removed)'
    TEMP_OFFLINE_PATTERN = r'>\s*\w+ server (is in )?(maintenance|maintainance)'


    def prepare(self):
        if not self.HOSTER_DOMAIN:
            if self.account:
                account      = self.account
            else:
                account_name = (self.__name__ + ".py").replace("Folder.py", "").replace(".py", "")
                account      = self.pyfile.m.core.accountManager.getAccountPlugin(account_name)

            if account and hasattr(account, "HOSTER_DOMAIN") and account.HOSTER_DOMAIN:
                self.HOSTER_DOMAIN = account.HOSTER_DOMAIN
            else:
                self.fail(_("Missing HOSTER_DOMAIN"))

        if isinstance(self.COOKIES, list):
            self.COOKIES.insert((self.HOSTER_DOMAIN, "lang", "english"))

        return super(XFSCrypter, self).prepare()
