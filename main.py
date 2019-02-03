#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)


import sys
from PyQt4.QtGui import QApplication
from common import FMainWindow
from invoice_view import InvoiceViewWidget

app = QApplication(sys.argv)


class MainWindow(FMainWindow):

    def __init__(self):
        FMainWindow.__init__(self)

        # self.setWindowIcon(QIcon.fromTheme(
        #     'logo', QIcon(u"{}".format(Config.APP_LOGO))))

        self.change_context(InvoiceViewWidget)


def main():
    window = MainWindow()
    # setattr(FWindow, 'window', window)
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
