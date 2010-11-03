#!/usr/bin/env python

import sys
import os
import time
import ConfigParser
from optparse import OptionParser
import signal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Browser(QWebPage):

    def __init__(self, url, show_requests=False, wait=0):
        self.wait = wait

        self.app = QApplication([])
        QWebPage.__init__(self)
        self.html = None
	netManager = self.networkAccessManager()
        self.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebSettings.PrivateBrowsingEnabled, True)
        self.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
        if show_requests:
	    QObject.connect(netManager, SIGNAL("finished(QNetworkReply *)"), self._on_network_reply) 

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.connect(self, SIGNAL('loadFinished(bool)'), self._on_finished_loading)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 (.NET CLR 3.5.30729)"

    def _on_network_reply(self, networkReply):
	print networkReply.url().toString()

    def _on_finished_loading(self, result):
        if self.wait > 0:
            waitToTime = time.time() + self.wait
            while time.time() < waitToTime:
                while QApplication.hasPendingEvents():
                    QApplication.processEvents()

        self.html = self.mainFrame().toHtml()
        self.app.quit()

def main():
    usage = "usage: %prog [options] URL"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--requests",
        action="store_true",
        dest="show_requests",
        help="show the URLs that are being hit while the page loads",
        default=False
    )
    parser.add_option("-w", "--wait", 
        action="store",
        type="int",
        dest="wait",
        default=None,
        help="Time to wait before outputting the post DOM html",
        metavar="SECONDS"
    )
    parser.add_option("-p", "--postdom",
        action="store_true",
        dest="html",
        help="show the HTML post DOM",
        default=False
    )
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Please specify a URL to dominate")
    else:
        url = args[0]

        browser = Browser(url, options.show_requests, options.wait)
        if options.html:
            print browser.html.__str__().encode('ascii', 'replace')

if __name__ == '__main__':
    main()
