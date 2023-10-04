# -*- coding: utf-8 -*-
# Python 3

def classFactory(iface):
    from .RechercheCommune6 import MainPlugin
    return MainPlugin(iface)


