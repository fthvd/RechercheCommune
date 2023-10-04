# -*- coding: utf-8 -*-
# Python 3

from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from console import *
import sys, os.path;

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(os.path.dirname(__file__)) 

# Import the code for the dialog
from RechercheCommune6 import doDlgBox1, doAbout

class MainPlugin(object):
      
    def __init__(self,iface):
        self.name = "Recherche Commune"
        # Initialise et sauvegarde l'interface QGIS en cours
        self.iface = iface

    def initGui(self):
        #déclaration des actions élémentaires
        menuIcon = resolve("RechercheCommuneIco.jpg")
        self.commande1 = QAction(QIcon(menuIcon),"Recherche Commune",self.iface.mainWindow())
        self.commande1.setText("Recherche Commune")

        menuIcon1 = resolve("about.png")
        self.about = QAction(QIcon(menuIcon1), "A propos ...", self.iface.mainWindow())
        self.about.setText("A propos ...")
        
        #Connection de la commande à l'action PYQT5
        self.commande1.triggered.connect(self.LoadDlgBoxQt1)
        self.about.triggered.connect(self.doInfo)
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.commande1)
        self.iface.addPluginToMenu("Recherche Commune", self.commande1)

#        # ouvre une console Qpython (pour debug et affichage commandes "print(), à désactiver pour l'utilisation)
#        maconsole = console.PythonConsole(self.iface.mainWindow())    # fenetre fixe
#        maconsole.setWindowTitle("Console RechercheCommunes6")
#        maconsole.setVisible(True)

    def unload(self): 
  
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Recherche Commune",self.commande1)
        self.iface.removeToolBarIcon(self.commande1)

    def LoadDlgBoxQt1(self):
        d = doDlgBox1.Dialog()
        #d.show()
        d.exec_()
     
    def doInfo(self):
        d = doAbout.Dialog()
        d.exec_()
 
#Fonction de reconstruction du chemin absolu vers la ressource image ou autre fichier
def resolve(name, basepath=None):
  if not basepath:
    basepath = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(basepath, name)  
