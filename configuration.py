#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import os


class Config():
    """ docstring for Config """
    DATEFORMAT = u'%d-%m-%Y'

    # ------------------------- Organisation --------------------------#
    LSE = False
    DEBUG = False
    ORG_LOGO = None

    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))

    AUTOR = u"IBS Mali"

    # -------- Application -----------#
    NAME_MAIN = "main.py"
    APP_NAME = "Facturation"
    APP_VERSION = 1
    APP_DATE = u"02/2019"
    templates = os.path.join(ROOT_DIR, "templates")
    img_media = os.path.join(ROOT_DIR, "img")
    APP_LOGO = os.path.join(img_media, "logo.png")
    IBS_LOGO = os.path.join(img_media, "ibs.jpg")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
