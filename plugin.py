###
# Copyright (c) 2012, xo
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from BeautifulSoup import BeautifulSoup
import requests
import re

class Kwotes(callbacks.Plugin):
    """rip pd7 known cum guzzler"""
    
    domain = "kwotes.420excess.com"

    def kwote(self, irc, msg, args):
        r = requests.get("http://%s/random.php" % self.domain)
        if r.status_code != 200:
            irc.reply("Status code %s" % r.status_code, prefixNick=False)
            return
        soup = BeautifulSoup(r.text, convertEntities=BeautifulSoup.HTML_ENTITIES)
        kwote_id = ''.join(soup.find(id="id").extract().findAll(text=True))
        kwote_date = soup.find(id="date").extract().findAll(text=True)[0]
        lines = soup.find(id="kwotes").findAll(text=True)
        irc.reply("%s %s" % (kwote_id, kwote_date), prefixNick=False)
        good_lines = filter(lambda x: x != '', [line.strip() for line in lines])
        for line in good_lines[0:5]:
            irc.reply(line, prefixNick=False)

        if len(good_lines) > 5:
            irc.reply("... [ http://%s/direct.php?id=%s ]" % (self.domain, self._extract_digits(kwote_id)), prefixNick=False)

    @staticmethod
    def _extract_digits(s):
        m = re.search('(\d+)', s)
        return m.group(1)
        

Class = Kwotes


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
