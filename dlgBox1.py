# -*- coding: utf-8 -*-
# Python 3

from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.gui import *
from qgis.utils import iface
from qgis.core import *

# Import libs 
import sys, os.path; sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import fonctions_localisercommune
import doAbout

#Fonction de reconstruction du chemin absolu vers la ressource image
def resolve(name, basepath=None):
  if not basepath:
    basepath = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(basepath, name)  

class Ui_Dialog(object):
    def setupUi(self,Dialog):
              
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,250).size()).expandedTo(Dialog.minimumSizeHint()))
        
        # QLabel lancer recherche
        self.label10 = QLabel(Dialog)
        self.label10.setGeometry(QtCore.QRect(15,25,150,18))
        self.label10.setObjectName("label10")
        self.label10.setText(" Selectionner :  ")
        
        #Exemple de QLabel de Région
        self.label = QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15,50,80,23))
        self.label.setObjectName("label")
        self.label.setText("<b>Région </b>")

        #definition QRegionComboBox
        #ListeRegion=("AUVERGNE-RHONE-ALPES","BOURGOGNE-FRANCHE-COMTE","BRETAGNE","CENTRE-VAL DE LOIRE","CORSE","GRAND EST",
        #             "HAUTS-DE-FRANCE","ILE-DE-FRANCE","NORMANDIE","NOUVELLE-AQUITAINE","OCCITANIE","PAYS DE LA LOIRE","PROVENCE-ALPES-COTE D'AZUR")
        ListeRegion=("AUVERGNE RHONE ALPES", "BOURGOGNE FRANCHE COMTE", "BRETAGNE", "CENTRE VAL DE LOIRE", "CORSE", "GRAND EST",
                        "GUADELOUPE", "GUYANE", "HAUTS DE FRANCE", "ILE DE FRANCE", "LA REUNION", "MARTINIQUE", "MAYOTTE",
                        "NORMANDIE", "NOUVELLE AQUITAINE", "OCCITANIE", "PAYS DE LA LOIRE", "PROVENCE ALPES COTE D'AZUR")
        self.RegionComboBox = QComboBox(Dialog)
        self.RegionComboBox.setGeometry(QtCore.QRect(100,50,280,23))
        self.RegionComboBox.setObjectName("RegionComboBox")
        #Exemple d'alimentation de la QComboBox avec LstOPGEO
        for i in range(len(ListeRegion)):  self.RegionComboBox.addItem(ListeRegion[i])

        # *** MODIF F. THEVAND *** Lecture de l'index de la dernière région choisie et écriture dans un fichier texte
        # avec contrôle de l'existence du fichier
        #fichMemReg = os.path.dirname(__file__)+"/data/dernier_choix_region.txt";
        fichMemReg = resolve("dernier_choix_region.txt")
        #QMessageBox.information(None,"information:","la liste des regions est dans : "+ fichMemReg)

        try:
            with open(fichMemReg, "r") as fichierReg:
                choixReg = int(fichierReg.read())
        except:
            with open(fichMemReg, "w") as fichierReg:
                fichierReg.write("0")
            with open(fichMemReg, "r") as fichierReg:
                choixReg = int(fichierReg.read())
        self.RegionComboBox.setCurrentIndex(choixReg)

        #Exemple de QLabel de Departement
        self.label = QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15,100,80,23))
        self.label.setObjectName("label")
        self.label.setText("<u>Departement</u>")

        #definition QDepartementComboBox
        #ListeDepartements = ("")
        
        # *** MODIF F. THEVAND *** Lecture de l'index du dernier département choisi et écriture dans un fichier texte
        # avec contrôle de l'existence du fichier

        try:
            #fichMemDep = os.path.dirname(__file__)+"/data/dernier_choix_departement.txt";
            fichMemDep = resolve("dernier_choix_departement.txt")
            with open(fichMemDep, "r") as fichierDep:
                choixDep = int(fichierDep.read())
        except:
            #fichMemDep = os.path.dirname(__file__)+"/data/dernier_choix_departement.txt";
            fichMemDep = resolve("dernier_choix_departement.txt")
            with open(fichMemDep, "w") as fichierDep:
                fichierDep.write("1")
            with open(fichMemDep, "r") as fichierDep:
                choixDep = int(fichierDep.read())

        self.DepartementComboBox = QComboBox(Dialog)
        self.DepartementComboBox.setGeometry(QtCore.QRect(100,100,280,23))
        self.DepartementComboBox.setObjectName("DepartementComboBox")

        # Alimentation de la QComboBox
        Selection = self.RegionComboBox.currentText()
        # Variable globale pour la mise à jour des listes départements et communes
        global uri
        uri = resolve("COMMUNE_avec_etendues.csv")
        erreur, dictDpt = fonctions_localisercommune.ouvre_csv_communes(uri)
        if erreur=="OK":
            if Selection != (""):
                self.DepartementComboBox.clear()
                ListeDepartements,DictDptModif = fonctions_localisercommune.cherche_Dpt(Selection,dictDpt)
                #QMessageBox.information(None,"information:","la liste des dpts est : "+ str(ListeDepartements))
                for i in range(len(ListeDepartements)):  self.DepartementComboBox.addItem(ListeDepartements[i])

        # *** MODIF F. THEVAND ***
        self.DepartementComboBox.setCurrentIndex(choixDep)

        #Exemple de QLabel de Commune
        self.label = QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15,150,80,23))
        self.label.setObjectName("label")
        self.label.setText("<i>Commune</i>")

        #definition QCommuneComboBox
        #ListeCommunes = ("")        
        # *** MODIF F. THEVAND *** Lecture de l'index de la dernière commune choisie et écriture dans un fichier texte
        # avec contrôle de l'existence du fichier
        #fichMemCom = os.path.dirname(__file__)+"/data/dernier_choix_commune.txt";
        fichMemCom = resolve("dernier_choix_commune.txt")
        try:
            with open(fichMemCom, "r") as fichierCom:
                choixCom = int(fichierCom.read())
        except:
            with open(fichMemCom, "w") as fichierCom:
                fichierCom.write("1")
            with open(fichMemCom, "r") as fichierCom:
                choixCom = int(fichierCom.read())

        self.CommuneComboBox = QComboBox(Dialog)
        self.CommuneComboBox.setGeometry(QtCore.QRect(100,150,280,23))
        self.CommuneComboBox.setObjectName("CommuneComboBox")
        #Exemple d'alimentation de la QComboBox avec LstOPGEO

        # *** MODIF F. THEVAND *** 
        global DictCommunesModif
        Selection = self.RegionComboBox.currentText()
        erreur, dictDpt = fonctions_localisercommune.ouvre_csv_communes(uri)
        #print("dictDpt : ", dictDpt)
        if erreur=="OK":
            ListeDepartements2,DictC = fonctions_localisercommune.cherche_Dpt(Selection,dictDpt)
        Selection2 = self.DepartementComboBox.currentText()
        if Selection2 != (""):
                self.CommuneComboBox.clear()
                ListeCommunes,DictCommunesModif = fonctions_localisercommune.cherche_Com(Selection2,DictC)
                for j in range(len(ListeCommunes)): self.CommuneComboBox.addItem(ListeCommunes[j])
        self.CommuneComboBox.setCurrentIndex(choixCom)

        #Exemple de QPushButton
        self.CloseButton = QPushButton(Dialog)
        self.CloseButton.setMinimumSize(QtCore.QSize(200, 20))
        self.CloseButton.setMaximumSize(QtCore.QSize(200, 20))        
        self.CloseButton.setGeometry(QtCore.QRect(100, 200,200, 20))
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.setText(" Quitter !")
        
        #Exemple de QPushButton
        self.aboutButton = QPushButton(Dialog)
        self.aboutButton.setMinimumSize(QtCore.QSize(70, 20))
        self.aboutButton.setMaximumSize(QtCore.QSize(70, 20))        
        self.aboutButton.setGeometry(QtCore.QRect(15, 200, 70, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.aboutButton.setText(" A propos...")
        
        # Connexion des slots et des actions liées
        #self.about.triggered.connect(self.doInfo)
        self.RegionComboBox.activated[str].connect(self.onCombo)
        self.DepartementComboBox.activated[str].connect(self.onCombo2)
        self.CommuneComboBox.activated[str].connect(self.onCombo3)
        self.aboutButton.clicked.connect(self.doAbout)
        self.CloseButton.clicked.connect(Dialog.reject)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    # définitions des actions que lancent les slots   
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Localisateur de Communes")
    
# *** Modifications F. THEVAND DDT04/UICTAS *** 
    def onCombo(self):
        Selection = self.RegionComboBox.currentText()
        uri = resolve("COMMUNE_avec_etendues.csv")
        erreur, dictDpt = fonctions_localisercommune.ouvre_csv_communes(uri)
        if erreur=="OK":
            if Selection != (""):
                self.DepartementComboBox.clear()
                ListeDepartements,DictDptModif = fonctions_localisercommune.cherche_Dpt(Selection,dictDpt)
                for i in range(len(ListeDepartements)):  self.DepartementComboBox.addItem(ListeDepartements[i])
                # *** MODIF F. THEVAND *** Mise à jour des départements et des communes en fonction de la région choisie région choisie
                self.DepartementComboBox.setCurrentIndex(1)
                Selection2 = self.DepartementComboBox.currentText()
                #QMessageBox.information(None,"information:","Selection2 est: "+ str(Selection2))
                self.CommuneComboBox.clear()
                ListeCommunes,DictCommunesModif=fonctions_localisercommune.cherche_Com(Selection2,DictDptModif)
                for j in range(len(ListeCommunes)): self.CommuneComboBox.addItem(ListeCommunes[j])
                self.CommuneComboBox.setCurrentIndex(1)
                #QMessageBox.information(None,"information:","la liste des coms est: "+ str(ListeCommunes))
        
        # *** MODIF F. THEVAND *** Ecriture dans un fichier texte de l'index de la dernière région choisie
        IndexReg = self.RegionComboBox.currentIndex()
        IdxReg = str(IndexReg)
        #fichMemReg = os.path.dirname(__file__)+"/data/dernier_choix_region.txt";
        fichMemReg = resolve("dernier_choix_region.txt")
        with open(fichMemReg, "w") as fichierReg:
            fichierReg.write(IdxReg)
        #fichMemDep = os.path.dirname(__file__)+"/data/dernier_choix_departement.txt";
        fichMemDep = resolve("dernier_choix_departement.txt")
        with open(fichMemDep, "w") as fichierDep:
            fichierDep.write("1")
        #fichMemCom = os.path.dirname(__file__)+"/data/dernier_choix_commune.txt";
        fichMemCom = resolve("dernier_choix_commune.txt")
        with open(fichMemCom, "w") as fichierCom:
            fichierCom.write("1")
        self.onCombo2()
        self.onCombo3()    

    def onCombo2(self):
        global DictCommunesModif
        Selection = self.RegionComboBox.currentText()
        erreur, dictDpt = fonctions_localisercommune.ouvre_csv_communes(uri)
        if erreur=="OK":
            ListeDepartements2,DictC = fonctions_localisercommune.cherche_Dpt(Selection,dictDpt)
        Selection2 = self.DepartementComboBox.currentText()
        if Selection2 != (""):
            self.CommuneComboBox.clear()
            ListeCommunes,DictCommunesModif=fonctions_localisercommune.cherche_Com(Selection2,DictC)
            for j in range(len(ListeCommunes)): self.CommuneComboBox.addItem(ListeCommunes[j])
        
        # *** MODIF F. THEVAND *** Ecriture dans un fichier texte de l'index du dernier département choisi
        self.CommuneComboBox.setCurrentIndex(1)
        IndexDep = self.DepartementComboBox.currentIndex()
        IdxDep = str(IndexDep)
        #fichMemDep = os.path.dirname(__file__)+"/data/dernier_choix_departement.txt";
        fichMemDep = resolve("dernier_choix_departement.txt")
        with open(fichMemDep, "w") as fichierDep:
            fichierDep.write(IdxDep)
        #fichMemCom = os.path.dirname(__file__)+"/data/dernier_choix_commune.txt";
        fichMemCom = resolve("dernier_choix_commune.txt")
        with open(fichMemCom, "w") as fichierCom:
            fichierCom.write("1")
        self.onCombo3()

    def onCombo3(self):    
        Selection3 = self.CommuneComboBox.currentText()
        Selec3=str(Selection3)
        if Selection3 != (""):
            insee_trouveL =fonctions_localisercommune.cherche_nom(Selec3,DictCommunesModif)
            self.affiche_resultat_et_zoom(insee_trouveL,DictCommunesModif)
        
        # *** MODIF F. THEVAND *** Ecriture dans un fichier texte de l'index de la dernière commune choisie
        IndexCom = self.CommuneComboBox.currentIndex()
        IdxCom = str(IndexCom)
        #fichMemCom = os.path.dirname(__file__)+"/data/dernier_choix_commune.txt";
        fichMemCom = resolve("dernier_choix_commune.txt")
        with open(fichMemCom, "w") as fichierCom:
            fichierCom.write(IdxCom)

    def doAbout(self):
        d = doAbout.Dialog()
        d.exec_()
      
    def affiche_resultat_et_zoom(self,insee,dict_communes):
        resultat=fonctions_localisercommune.infos_commune(insee,dict_communes)
        #QMessageBox.information(None,"information:","La commune trouvée est :\n " + str(resultat[0])+ "/n avec les coords : " + str(int(resultat[1])))
        #if resultat[0]>100000:
        #self.zoom_extent(resultat[1],resultat[2],resultat[3],resultat[4])
        self.zoom_extent(insee,resultat[5],resultat[6],resultat[7],resultat[8])
    
    def zoom_extent(self,insee,xmin,ymin,xmax,ymax):
        xmin=int(xmin)
        ymin=int(ymin)
        xmax=int(xmax)
        ymax=int(ymax)
        
        #On agrandit l'emprise au cas ou (min 500m)
        if xmax-xmin<500:
            xmin = xmin - (500-(xmax-xmin))/2
            xmax = xmax + (500-(xmax-xmin))/2
        if ymax-ymin<500:
            ymin = ymin - (500-(ymax-ymin))/2
            ymax = ymax + (500-(ymax-ymin))/2
        
        #Creation du rectangle d'emprise :
        rec = QgsRectangle(xmin, ymin, xmax, ymax)
        """
        QMessageBox.information(None,"information:","La commune s'inscrit dans une emprise de "
                                + str(rec.height())+ " de haut \n" + " par " + str(rec.width())
                                + " de large \n" + " son code insee est : " + str(insee) )
        """
        self.iface = iface
        self.iface.mapCanvas = iface.mapCanvas
        self.iface.mapCanvas().setExtent(rec)
        self.iface.mapCanvas().refresh()
