# The Art Gallery Problem expanded to a city

The goal is to ensure **complete surveillance of a city**, by strategically placing security cameras. For that, we will use the [Art Gallery Problem](https://en.wikipedia.org/wiki/Art_gallery_problem) principles.

<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/images/city.jpeg" width="800"/>
1) Let's take the city of Besançon, France, as an example. <br>
2) Complete surveillance is only needed in frequently used streets. Let's use Strava's Global heatmap to identify them. <br>
3) We represent these streets by a polygon with holes.

## Table of Contents
1. [Triangulation](#triangulation)
2. [3-Coloring](#3-coloring)
3. [Final result](#final-result)
   
## Triangulation

We first triangulate the polygon by applying the **ear-clipping algorithm**, which divides it into non-overlapping triangles.
<br><br>
<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/images/triangulation.png" width="600"/>

## 3-Coloring

Next, we apply a 3-coloring algorithm to the triangulated polygon.

***Why 3 colors?*** Because the Art Gallery Theorem states that "To guard a simple polygon with n vertices, **⌊n/3⌋ guards are always sufficient** and sometimes necessary".
<br><br>
<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/images/3coloring.png" width="600"/>

## Final result

Finally, we keep the least represented color. The placement of these 53 security cameras will ensure the complete surveillance of the city.
<br><br>
<img src="https://github.com/clementaudic/Art-Gallery-Problem_CCTV-coverage-optimization_TIPE/blob/main/images/final.png" width="600"/>
    
