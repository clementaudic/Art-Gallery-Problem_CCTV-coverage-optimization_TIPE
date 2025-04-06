from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Polygon
import geopandas
import sys

'''partie 1: triangulation'''

def ear_clipping(polygone):
    
    if test_sens_horaire(polygone):
        polygone.reverse()
    
    nb_sommets = len(polygone)
    liste_indices = list(range(nb_sommets))
    liste_triangles = []

    while(nb_sommets>4):
        for indice_sommet in liste_indices:
            indice_indice_sommet = liste_indices.index(indice_sommet)
            sommet_prec = polygone[liste_indices[indice_indice_sommet-1]]
            sommet = polygone[indice_sommet]
            sommet_suiv = polygone[liste_indices[(indice_indice_sommet + 1) % nb_sommets]]

            if test_oreille(sommet_prec, sommet, sommet_suiv, polygone):
                liste_triangles.append((sommet_prec, sommet, sommet_suiv))
                del liste_indices[indice_indice_sommet]
                nb_sommets -= 1
                break

    liste_triangles.append((polygone[liste_indices[0]], polygone[liste_indices[1]], polygone[liste_indices[2]])) 
    
    return liste_triangles
    
# l'algorithme de ear clipping doit toujours traiter les sommets du polygone dans le même sens, ici, le sens trigonométrique a été choisi arbitrairement

def test_sens_horaire(polygone):
    aire_polygone = 0
    taille_polygone = len(polygone)
    for i in range(taille_polygone):
        sommet = polygone[i]
        sommet_suiv = polygone[(i + 1) % taille_polygone]
        aire_polygone += (sommet_suiv[0] - sommet[0]) * ((sommet_suiv[1] + sommet[1])/2)
    return aire_polygone > 0

# deux conditions pour qu'un sommet soit une oreille d'un polygone
def test_oreille(p1, p2, p3, polygone):
    booleen = test_saillant(p1, p2, p3) and test_triangle_contient_sommets(p1, p2, p3, polygone) 
    return booleen

# condition n°1 : l'angle interne induit par le sommet saillant
def test_saillant(prec, sommet, suiv):
    return aux_test_saillant(prec[0], prec[1], sommet[0], sommet[1], suiv[0], suiv[1]) < 0

def aux_test_saillant(x1, y1, x2, y2, x3, y3):
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)

# condition n°2: le triangle formé par le sommet et ces deux sommets voisins ne contient aucun autres sommets du polygone
def test_triangle_contient_sommets(p1, p2, p3, polygone):
    for pi in polygone:
        if pi in (p1, p2, p3):
            continue
        elif test_sommet_interieur_triangle(pi, p1, p2, p3):
            return False
    return True

def test_sommet_interieur_triangle(p, a, b, c):
    aire = aire_triangle(a[0], a[1], b[0], b[1], c[0], c[1])
    aire1 = aire_triangle(p[0], p[1], a[0], a[1], b[0], b[1])
    aire2 = aire_triangle(p[0], p[1], b[0], b[1], c[0], c[1])
    aire3 = aire_triangle(p[0], p[1], a[0], a[1], c[0], c[1])
    booleen_test_egalite_aire = abs(aire - (aire1 + aire2 + aire3)) < sys.float_info.epsilon
    return booleen_test_egalite_aire

def aire_triangle(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))) / 2.0

'''partie 2: trois coloriage'''

def trois_coloriage(triangles):
    liste_colories = []
    dictionnaire_adjacences = calcul_adjacence(triangles)
    n = len(dictionnaire_adjacences)
    dictionnaire_couleurs = {}
    
    # coloriage du premier triangle
    triangle = triangles[0]
    premier = triangle[0]
    deuxieme = triangle[1]
    troisieme = triangle[2]
    dictionnaire_couleurs[premier] = 1
    dictionnaire_couleurs[deuxieme] = 2
    dictionnaire_couleurs[troisieme] = 3
    liste_colories.append(premier)
    liste_colories.append(deuxieme)
    liste_colories.append(troisieme)
    liste_attente = []
    if(n!=3):
        coloration_rec(liste_attente,premier,deuxieme,troisieme,liste_colories,n,dictionnaire_adjacences,dictionnaire_couleurs)
    liste_rouge = [cle for cle, valeur in dictionnaire_couleurs.items() if valeur == 1]
    liste_bleu = [cle for cle, valeur in dictionnaire_couleurs.items() if valeur == 2]
    liste_vert = [cle for cle, valeur in dictionnaire_couleurs.items() if valeur == 3]
    return [liste_rouge,liste_bleu,liste_vert]

def calcul_adjacence(triangles):
    dictionnaire_adjacences = {}
    for triangle in triangles:
        compteur = 0
        for sommet in triangle: 
            if sommet not in dictionnaire_adjacences: 
                    dictionnaire_adjacences[sommet] = [triangle[(compteur + 1) % 3],triangle[(compteur + 2) % 3]]
            else:
                dictionnaire_adjacences[sommet] += [triangle[(compteur + 1) % 3],triangle[(compteur + 2) % 3]]
            compteur += 1
    
    for sommet in dictionnaire_adjacences.keys():
        dictionnaire_adjacences[sommet] = list(set(dictionnaire_adjacences[sommet]))

    return dictionnaire_adjacences
    
def coloration_rec(liste_attente,premier,deuxieme,troisieme,liste_colories,nb_sommets,dictionnaire_adjacences,dictionnaire_couleurs):

    while len(list(set(liste_colories)))!=nb_sommets:
        listea = test_coloration(dictionnaire_adjacences,deuxieme,troisieme,liste_colories)
        listeb = test_coloration(dictionnaire_adjacences,premier,troisieme,liste_colories)
        listec = test_coloration(dictionnaire_adjacences,premier,deuxieme,liste_colories)

        if listea[0] and listeb[0]:
            liste_attente.append((listeb[1],premier,troisieme))
        elif listea[0] and listec[0]:
            liste_attente.append((listec[1],premier,deuxieme))
        elif listeb[0] and listec[0]:
            liste_attente.append((listec[1],premier,deuxieme))
    
        if listea[0]:
            coloriage(listea[1],dictionnaire_couleurs[deuxieme],dictionnaire_couleurs[troisieme],dictionnaire_couleurs,liste_colories)
            liste_colories.append(listea[1])
            return coloration_rec(liste_attente,deuxieme,troisieme,listea[1],liste_colories,nb_sommets,dictionnaire_adjacences,dictionnaire_couleurs)
            
        if listeb[0]:
            coloriage(listeb[1],dictionnaire_couleurs[premier],dictionnaire_couleurs[troisieme],dictionnaire_couleurs,liste_colories)
            liste_colories.append(listeb[1])
            return coloration_rec(liste_attente,premier,troisieme,listeb[1],liste_colories,nb_sommets,dictionnaire_adjacences,dictionnaire_couleurs)

        if listec[0]:
            coloriage(listec[1],dictionnaire_couleurs[premier],dictionnaire_couleurs[deuxieme],dictionnaire_couleurs,liste_colories)
            liste_colories.append(listec[1])
            return coloration_rec(liste_attente,premier,deuxieme,listec[1],liste_colories,nb_sommets,dictionnaire_adjacences,dictionnaire_couleurs)
            
        else:
            l = liste_attente[0]
            coloriage(l[0],dictionnaire_couleurs[l[1]],dictionnaire_couleurs[l[2]],dictionnaire_couleurs,liste_colories)
            liste_colories.append(l[0])
            liste_attente_copie = liste_attente
            liste_attente_copie.remove(l)
            return coloration_rec(liste_attente_copie,l[0],l[1],l[2],liste_colories,nb_sommets,dictionnaire_adjacences,dictionnaire_couleurs) 

def test_coloration (dictionnaire_adjacences,sommet1,sommet2,liste_colories):
    liste = complementaire(intersection(dictionnaire_adjacences[sommet1],dictionnaire_adjacences[sommet2]),liste_colories) 
    if liste != []:
        return [True,liste[0]]
    else:
        return [False,[]]
               
def intersection(liste1, liste2):
    return list(set(liste1) & set(liste2))

def complementaire(liste1,liste2):
    return list(set(liste1) - set(liste2))

def coloriage(elt,couleur1,couleur2,dictionnaire_couleurs,liste_colories):
    if couleur1 + couleur2 == 3 :
        dictionnaire_couleurs[elt]= 3
    elif couleur1 + couleur2 == 5 :
        dictionnaire_couleurs[elt]= 1
    else: 
        dictionnaire_couleurs[elt]= 2
    liste_colories.append(elt)

'''partie 3: affichage'''

def affichage_global(polygone): 
    triangles = ear_clipping (polygone)
    affichage_polygone(polygone)
    affichage_triangulation(triangles)
    affichage_trois_coloriage(triangles)
    pyplot.show()    
     
def affichage_solution(polygone):
    affichage_polygone(polygone) 
    triangles = ear_clipping (polygone)
    affichage_couleur_minimale(triangles)
    pyplot.show()    

def affichage_polygone(polygone):
    # légère coloration de l'intérieur du polygone
    poly = Polygon(polygone)
    pol = geopandas.GeoSeries(poly)
    pol.plot(color='seashell')
    # tracé du contour du polygone
    liste_x = []
    liste_y = []
    for sommet in polygone:
        liste_x.append(sommet[0])
        liste_y.append(sommet[1])
        pyplot.plot(liste_x,liste_y, linewidth=2, c = 'black')

def affichage_triangulation(triangles):
    nb_triangles = len(triangles)
    i = 0
    for triangle in triangles:
        liste_x = []
        liste_y = []
        i+=1
        for sommet in triangle:
            liste_x.append(sommet[0])
            liste_y.append(sommet[1])
        if nb_triangles==i :
            sommet = triangle[0]
            liste_x.append(sommet[0])
            liste_y.append(sommet[1])
        pyplot.plot(liste_x,liste_y,color='dodgerblue',linestyle='dashed')

def affichage_trois_coloriage(triangles):
    liste_couleurs = trois_coloriage(triangles)
    liste_rouge_x = []
    liste_rouge_y = []
    liste_bleu_x = []
    liste_bleu_y = []
    liste_vert_x = []
    liste_vert_y = []

    for sommet in liste_couleurs[0]:
        liste_rouge_x.append(sommet[0])
        liste_rouge_y.append(sommet[1])
    for sommet in liste_couleurs[1]:
        liste_bleu_x.append(sommet[0])
        liste_bleu_y.append(sommet[1])
    for sommet in liste_couleurs[2]:
        liste_vert_x.append(sommet[0])
        liste_vert_y.append(sommet[1])

    pyplot.scatter(liste_rouge_x,liste_rouge_y, s=100, c = 'r')
    pyplot.scatter(liste_bleu_x,liste_bleu_y, s=100, c = 'b')
    pyplot.scatter( liste_vert_x, liste_vert_y, s=100, c = 'g')

def affichage_couleur_minimale(triangles):
    liste_couleurs = trois_coloriage(triangles)
    liste_rouge_x = []
    liste_rouge_y = []
    liste_bleu_x = []
    liste_bleu_y = []
    liste_vert_x = []
    liste_vert_y = []

    taille_liste_rouge = len(liste_couleurs[0])
    taille_liste_bleu = len(liste_couleurs[1])
    taille_liste_vert = len(liste_couleurs[2])
    min_couleurs= min([taille_liste_rouge,taille_liste_bleu,taille_liste_vert])
    
    if(min_couleurs==taille_liste_rouge):
        for sommet in liste_couleurs[0]:
            liste_rouge_x.append(sommet[0])
            liste_rouge_y.append(sommet[1])
    elif(min_couleurs==taille_liste_bleu):
        for sommet in liste_couleurs[1]:
            liste_bleu_x.append(sommet[0])
            liste_bleu_y.append(sommet[1])
    else:
        for sommet in liste_couleurs[2]:
            liste_vert_x.append(sommet[0])
            liste_vert_y.append(sommet[1])

    pyplot.scatter(liste_rouge_x,liste_rouge_y, s=165, c = 'r')
    pyplot.scatter(liste_bleu_x,liste_bleu_y, s=165, c = 'b')
    pyplot.scatter( liste_vert_x, liste_vert_y, s=165, c = 'g')

'''partie 4: exécution'''

polygone_illustration = [(44,22),(96,38),(169,6),(168,123),(80,86),(80,100),(63,70),(9,85),(26,63),(14,56),(64,49),(96,63),(130,47),(65,44),(9,52),(44,22)] 

polygone_un = [(54,1),(3,113),(30,293),(116,387),(126,387),(126,379),(113,345),(328,138),(300,109),(309,39),(340,15),(341,2),(55,2),(64,14),(231,14),
(195,68),(104,95),(99,80),(57,30),(51,42),(85,83),(116,158),(30,191),(31,202),(122,169),(167,275),(177,263),(138,173),(191,130),(248,193),(257,184),
(202,122),(256,79),(288,114),(290,99),(267,71),(296,47),(295,32),(254,64),(242,16),(235,26),(244,71),(132,160),(107,102),(202,74),(241,13),(318,14),
(300,29),(291,117),(308,138),(118,329),(38,254),(41,272),(109,335),(103,343),(109,360),(40,286),(14,112),(63,16),(54,1)]

polygone_deux = [(295,246),(257,203),(266,195),(285,216),(296,165),(307,154),(292,225),(313,247),(236,321),(359,459),(282,474),(282,484),(330,478),
(343,467),(355,471),(330,490),(223,506),(131,405),(165,372),(168,290),(176,290),(176,377),(153,402),(184,401),(192,412),(179,414),(244,471),(259,468),
(262,477),(242,481),(166,414),(157,415),(226,492),(268,487),(266,469),(197,407),(207,400),(182,376),(181,359),(213,326),(222,334),(191,367),(218,395),
(251,363),(259,371),(215,411),(276,467),(343,455),(227,329),(224,333),(179,283),(185,279),(220,318),(228,311),(191,270),(198,264),(235,305),(295,246)]

polygone_trois = [(263,350),(271,358),(333,299),(422,396),(356,453),(363,461),(476,368),(539,247),(575,124),(534,106),(498,164),(367,81),(318,126),
(326,134),(367,95),(432,135),(386,182),(323,137),(316,145),(353,187),(315,225),(360,272),(380,251),(407,247),(480,328),(485,319),(420,245),(495,179)
,(488,176),(455,204),(433,190),(401,187),(394,197),(450,210),(413,239),(392,242),(430,205),(418,200),(359,257),(331,227),(363,195),(388,195),(440,140)
,(500,175),(537,116),(561,127),(523,254),(466,361),(431,388),(344,289),(365,275),(349,268),(263,349)]

besancon = [(54,0),(3,112),(27,290),(222,506),(328,492),(476,370),(540,250),(576,126),(537,108),(500,168),(368,80),(316,128),(300,110),(308,38),
(340,13),(340,0),(55,0),(62,13),(231,14),(195,68),(104,94),(96,77),(57,31),(52,40),(84,82),(116,157),(27,190),(29,202),(120,169),(167,276),(115,328),
(36,254),(38,270),(107,335),(102,341),(108,361),(122,376),(111,344),(166,290),(164,373),(140,396),(156,413),(164,413),(240,480),(267,476),(267,485),
(280,483),(280,473),(345,463),(355,454),(270,360),(334,300),(422,397),(433,389),(344,290),(382,254),(408,249),(482,331),(487,321),(421,246),(500,177),
(491,175),(456,205),(434,189),(398,186),(439,143),(431,138),(387,184),(366,184),(326,140),(317,147),(354,189),(303,237),(291,224),(306,155),(314,147),
(306,139),(258,185),(265,194),(295,165),(280,230),(294,245),(220,318),(182,275),(188,268),(225,309),(232,302),(195,262),(256,203),(279,228),(281,214),
(200,122),(255,79),(288,114),(290,100),(265,72),(297,46),(289,36),(253,65),(241,15),(234,25),(244,71),(132,159),(137,170),(190,130),(248,194),(177,265),
(178,283),(213,324),(179,359),(179,374),(205,398),(167,401),(179,413),(200,411),(261,466),(272,464),(215,411),(261,369),(253,361),(218,396),(187,368),
(226,330),(253,359),(261,350),(236,321),(324,235),(351,264),(358,258),(332,228),(365,195),(450,210),(414,241),(393,243),(428,208),(415,206),(255,360),
(340,455),(242,471),(163,401),(151,402),(177,376),(175,265),(106,102),(201,74),(240,14),(317,14),(300,28),(290,117),(316,145),(368,95),(500,176),
(539,116),(563,128),(529,247),(467,362),(330,478),(225,492),(39,286),(15,111),(61,14),(54,0)]

# affichage_global(polygone_illustration)
affichage_global(besancon)

affichage_solution(besancon)