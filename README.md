# Art-Gallery-Problem_CCTV-coverage-optimization_TIPE

## Table of Contents
1. [Presentation](#presentation)
2. [Triangulation](#triangulation)
3. [3-Coloring](#3-coloring)
4. [Display](#display)

## Presentation
The aim is to establish a network of security cameras to safeguard entirely the center of a city. 

<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/besancon.png" alt="hexagon" width="800"/>

1: In this example, we want to safeguard Besançon downtown, which is bounded by the horseshoe-shaped Doubs River.
2: In order to pinpoint the streets to monitor, and in particular to distinguish them from private courtyards and parking lots, I make use of [Strava's Global heatmap](https://www.strava.com/heatmap). [3] Finally, I have represented the city by a polygon using Geogebra.

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
    
