import numpy as np
import matplotlib.pyplot as plt
from geojson import Point, Feature, FeatureCollection, dump
from geojson import Polygon, MultiPolygon

from shapely.geometry.polygon import LinearRing, Polygon

scale = 10
radius_Center_Double = 166 / scale
radius_Center_Triple = 111 / scale

radius_Bull_Double = 12.7 / 2 / scale

radius_Bull_Simple = 31.8 / 2 / scale

dble_semi_width = 4 / scale
tple_semi_width = 4 / scale

n = 20

def arc(ray, theta):
    arc_x = ray * np.cos(theta)
    arc_y = ray * np.sin(theta)
    arc = list(zip(arc_x, arc_y))
    return(arc)

def rev(input):
    return(list(reversed(input)))

features = []

theta = np.linspace(-np.pi , np.pi, n*20)
single_bull = arc(radius_Bull_Simple, theta)
double_bull = arc(radius_Bull_Double, theta) 
p_single_bull = Polygon(rev(single_bull), (rev(double_bull), ))
p_double_bull = Polygon(rev(double_bull))

features.append(Feature(geometry=p_double_bull, properties={"id": "25.2"}))
features.append(Feature(geometry=p_single_bull, properties={"id": "25.0"}))


for i in range (0, 20):
    
    theta = np.linspace(-np.pi/20 + 2*i*np.pi/20 , np.pi/20 + 2*i*np.pi/20, n)

    bull_arc = arc(radius_Bull_Simple, theta)

    arc_double_low = arc(radius_Center_Double - dble_semi_width, theta) 
    arc_double_high = arc(radius_Center_Double + dble_semi_width, theta) 
    
    arc_triple_low = arc(radius_Center_Triple - tple_semi_width, theta) 
    arc_triple_high = arc(radius_Center_Triple + tple_semi_width, theta) 

    p_double = Polygon(arc_double_low + rev(arc_double_high))
    p_triple = Polygon(arc_triple_low + rev(arc_triple_high))
    p_1 = Polygon(bull_arc + rev(arc_triple_low))
    p_2 = Polygon(arc_triple_high + rev(arc_double_low))
    
    features.append(Feature(geometry=p_double, properties={"id": f"{i}.2"}))
    features.append(Feature(geometry=p_triple, properties={"id": f"{i}.3"}))
    features.append(Feature(geometry=p_1, properties={"id": f"{i}.0.0"}))
    features.append(Feature(geometry=p_2, properties={"id": f"{i}.0.1"}))



feature_collection = FeatureCollection(features)

with open('ressources/darts.geojson', 'w') as f:
   dump(feature_collection, f)
