# -*- coding: utf-8 -*-
# Python 3

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from PyQt5 import QtCore
from qgis.PyQt.QtWidgets import QGridLayout, QLabel, QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QApplication

# Import libs 
import sys, os.path; sys.path.append(os.path.dirname(os.path.abspath(__file__)))
 
#Fonction de reconstruction du chemin absolu vers la ressource image
def resolve(name, basepath = None):
  if not basepath:
    basepath = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(basepath, name)  

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,350,400).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QLabel(Dialog)
        self.labelImage = QLabel(Dialog)
        carIcon = QImage(resolve("FranceLogo.jpg"))
        self.labelImage.setPixmap(QPixmap.fromImage(carIcon))

        font = QFont()
        font.setPointSize(15) 
        font.setWeight(50) 
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,2)
        self.gridlayout.addWidget(self.labelImage,1,5,1,2)

        self.textEdit = QTextEdit(Dialog)

        palette = QPalette()

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active,QPalette.Base,brush)

        brush = QBrush(QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive,QPalette.Base,brush)

        brush = QBrush(QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled,QPalette.Base,brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 380
        self.textEdit.height = 380
        #self.textEdit.setFrameShape(QFrame.NoFrame)
        #self.textEdit.setFrameShadow(QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
       
        self.gridlayout.addWidget(self.textEdit,1,1,5,2) 

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,4,2,1,1) 

        spacerItem = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,5,1,1)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QApplication.translate("Dialog", "Recherche Commune", None))
        self.label_2.setText(QApplication.translate("Dialog", "Recherche Commune 5", None))
        self.textEdit.setHtml(QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:300; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        "Recherche Commune 6 :</span>" "  Ce plugin est conçu pour les agents souhaitant disposer dans Qgis 3"+
                                                           " d'une fonctionnalité permettant de localiser une commune.                                                                            "+
                                                           " Il fonctionne hors connexion internet à partir d'un fichier csv associé au plugin.                                                   "+
                                                           " Ce fichier csv est produit à partir des données de la couche ADMIN-EXPRESS-COG_2-1__SHP__FRA du 29 juillet 2020.                                                                               "+
                                                           " Il s'inspire librement de l'outil : 'Zoomer de la région à la parcelle' "+
                                                           " de M. Mathieu Rajerison (DREAL PACA), du document : 'Conception d'un plugin "+
                                                           " Python pour Qgis' de M. Remy Morel (CETE Nord Picardie) "+
                                                           " et du plugin éponyme de M. Jean-Christophe Baudin, de l'AFBiodiversite DIR9."+
                                                           " Cette extension ne fait pas partie du moteur de Qgis. Toute demande est à adresser à l'auteur : </p></td></tr></table>"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        #"<font color='#0000FF'><b><u> François Thévand</u></b></font><br><br>"
        "<b>francois.thevand@alpes-de-haute-provence.gouv.fr</b><br><b>DDT04 UICTAS </b><br>"
        "<br><i>Version 6.0 (18 août 2020).</i></p></body></html>", None))
        self.pushButton.setText(QApplication.translate("Dialog", "OK", None))

