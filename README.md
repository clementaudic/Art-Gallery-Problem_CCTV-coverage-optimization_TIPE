# The Art Gallery Problem expanded to a city

## Presentation
The goal is to ensure **complete surveillance of a city's downtown**, by strategically placing security cameras. For that, we will use the [Art Gallery Problem](https://en.wikipedia.org/wiki/Art_gallery_problem) principles.

<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/besancon.png" alt="hexagon" width="800"/>
1) Let's take the city of Besançon, France as an example. <br>
2) Complete surveillance is only needed in frequently used streets. Let's use [Strava's Global heatmap](https://www.strava.com/heatmap) to identify them. <br>
3) We represent these streets by a polygon with holes.

## Table of Contents
1. [Triangulation](#triangulation)
2. [3-Coloring](#3-coloring)
3. [Display](#display)
   
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
The ear-clipping algorithm must still process the vertices of the polygon in the same order.
‘‘‘python
def is_clockwise(polygon):
    signed_polygon_area = 0
    polygon_size = len(polygon)
    for i in range(polygon_size):
        current_vertex = polygon[i]
        next_vertex = polygon[(i + 1) % polygon_size]
        signed_polygon_area += (next_vertex[0] - current_vertex[0]) * ((next_vertex[1] + current_vertex[1])/2)
    return signed_polygon_area
‘‘‘
## 3-Coloring
## Display
    
