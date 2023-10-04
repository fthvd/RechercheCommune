# -*- coding: utf-8 -*-
# Python 3

"""
/***************************************************************************
 Fichier des fonctions du plugin CommuneExplorer

 Zoom sur l'emprise d'une commune localisée
                              -------------------
        begin                : 2016-01-21
        copyright            : (C) 2020 par Francois Thévand DDT04/UICTAS
                               d'après le code de Jean-Christophe Baudin ONEMA DIR9
        email                : francois.thevand@alpes-de-haute-provence.gouv.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import csv
import re

def ouvre_csv_communes(input_file):
    """ Ouvre le fichier des commmunes et place le résultat
    dans un dictionnaire ayant comme clé le code INSEE
    """

    try:
        dict_communes = {}
        with open(input_file, newline='', encoding = 'utf-8') as f:
            reader = csv.reader(f, delimiter = ';', quotechar = '"')
            for ligne in reader:
                dict_communes[ligne[1]] = [ligne[2], ligne[3], ligne[4], ligne[5], ligne[6], ligne[7], ligne[8], ligne[9], ligne[10]]
        f.close()
        return "OK", dict_communes
    except: #return false (erreur) si il y a problème
        return "Erreur : lecture du fichier impossible", {}

def cherche_Dpt(message, dico):
    listeD = {}
    liste = []
    liste.append("")
    for n in list(dico.keys()):
        if dico[n][4] != (str(message)):
            del dico[n]
    for c in list(dico.keys()):
        listeD[(dico[c][1])] = [(dico[c][2])]
    for l in list(listeD.keys()):
        liste.append(str(listeD[l][0]))
    liste.sort()     
    return liste, dico
    
def cherche_Com(message, dico):
    listeC = {}
    liste2 = []
    liste2.append("")
    for n in list(dico.keys()):
        if dico[n][2] != (str(message)):
            del dico[n]
    for c in list(dico.keys()):
        listeC[c] = [(dico[c][0])]
    for l in listeC.keys():
        liste2.append(str(listeC[l][0]))
    liste2.sort()  
    return liste2, dico
  
def cherche_insee (insee,dict_communes):
    """ Cherche dans le tableau de données l'existence du code INSEE saisi
    retourne une chaine vide si le code n'existe pas
    """
    liste_codes=dict_communes.keys() # les codes INSEE sont les clefs
                                        # du dictionnaire
    if insee in liste_codes:
        return insee
    else:
        return ""

def fonction_test(nom):
    nomf = nettoie_chaine_majuscule(nom)
    if nomf=='':
        return''
    else:
        return nomf

def cherche_nom (nom,dict_communes):
    """ Cherche dans le tableau de données la ville
    dont le nom est le plus proche du nom saisi
    """
    # Nettoyage de la chaine en entrée
    nomN=nettoie_chaine_majuscule(nom)
    if nomN == '':
        return ''
    # Comparaison du nom saisi à tous les noms de communes
    distance_mini = 100000000000
    insee_mieux = ""
    for insee in dict_communes.keys():
        d = levenshtein(nomN,dict_communes[insee][0])
        if d < distance_mini:
            distance_mini = d
            insee_mieux = insee
        if d == 0:
            break
    return insee_mieux

def infos_commune(insee,dict_communes):
    """ Renvoie les infos d'une commune en fonction du code INSEE.
    C'est un tuple avec le libellé sans casse, xmin,ymin,xmax,ymax
    """
    try:
        return dict_communes[insee]
    except:
        return ["Aucune commune trouvée", 0, 0, 0, 0]
 
def nettoie_chaine_majuscule(chaineutf8):
    """ Met une chaine en majuscule, supprime les caractères accentués
    et supprime les blancs inutiles ( inclus les underscores)
    """
    
    # Met les majuscules
    chaineutf8 = chaineutf8.upper()
    # Enlève les caractères spéciaux
    chaineutf8 = re.sub('\W', ' ', chaineutf8)
    chaineutf8 = re.sub('_', ' ', chaineutf8)
    # Enlève les séries de blancs
    chaineutf8 = chaineutf8.strip()
    chaineutf8 = re.sub('\s-', ' ', chaineutf8)
    return chaineutf8

def levenshtein(a,b):
    """ Calcule la distance de Levenshtein
    entre les chaines a et b
    """
    n,m = len(a), len(b)
    if n > m:
        # vérifier n <= m, pour utiliser O(min(n,m))space
        a,b = b, a
        n,m = m, n
    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add,delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change +1
            current[j] = min(add, delete, change)
    return current[n]
