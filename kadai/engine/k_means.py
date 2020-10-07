from PIL import Image
import math
import random

class kMeansEngine():
    def __init__(self, image):
        self.image = image
        self.colors = get_colors(image)

    def generate(self):
        return self.colors

class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates    

class Cluster:
    def __init__(self, center, points):
        self.center = center
        self.points = points

class KMeans:
    def __init__(self, n_clusters, min_diff = 10):
        self.n_clusters = n_clusters
        self.min_diff = min_diff


    def calculate_center(self, points):
        n_dim = len(points[0].coordinates)
        vals = [0.0 for i in range(n_dim)]

        for p in points:
            for i in range(n_dim):
                vals[i] += p.coordinates[i]
        
        coords = [(v/len(points)) for v in vals]
        return Point(coords)

    def assign_points(self, clusters, points):
        plists = [[] for i in range(self.n_clusters)]

        for p in points:
            smallest_distance = float('inf')

            for i in range(self.n_clusters):
                distance = euclidan(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            
            plists[idx].append(p)

        return plists

    
    def fit(self, points):
        clusters = [Cluster(center=p, points=[p]) for p in random.sample(points, self.n_clusters)]

        while True:
            plists = self.assign_points(clusters, points)
            diff=0

            for i in range(self.n_clusters):
                if not plists[i]:
                    continue

                old = clusters[i]
                center = self.calculate_center(plists[i])
                new = Cluster(center, plists[i])
                clusters[i] = new
                diff = max(diff, euclidan(old.center, new.center))

            if diff < self.min_diff:
                break

        return clusters

def get_points(image_path):
    img = Image.open(image_path)
    w,h = img.size

    points = []
    for count, color in img.getcolors(w*h):
        for _ in range(count):
            points.append(Point(color))

    return points

def euclidan(p, q):
    n_dim = len(p.coordinates)
    return math.sqrt(sum([
        (p.coordinates[i] - q.coordinates[i]) ** 2 for i in range(n_dim)
    ]))

def get_colors(filename, n_colors=7):
    points = get_points(filename)
    clusters = KMeans(n_clusters=n_colors).fit(points)
    clusters.sort(key=lambda c: len(c.points), reverse = True)
    rgbs = list(map(tuple, [map(int, c.center.coordinates) for c in clusters]))
    return rgbs

"""
kadai - Simple wallpaper manager for tiling window managers.
Copyright (C) 2020  slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Find the full license in the root of this project
"""