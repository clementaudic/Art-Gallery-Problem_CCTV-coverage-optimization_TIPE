# Art-Gallery-Problem_CCTV-coverage-optimization_TIPE

## Table of Contents
1. [Presentation](#presentation)
2. [Triangulation](#triangulation)
3. [3-Coloring](#3-coloring)
4. [Display](#display)

## Presentation
The city council of Besançon wants to create a network of security cameras. The aim is to minimize the cost of such a network, while ensuring optimum coverage. How many cameras will the city need to purchase to ensure optimum surveillance of public spaces?



## Triangulation

Ear clipping algorithm
```python

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
```
## 3-Coloring
## Display
    
