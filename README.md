# Geometric Component Analysis

This repository contains two notebooks:
1. [Principal Diameters of Disconnected Components - 3D](principal_diameters_3d.ipynb)
2. [Principal Diameters, Sphericity, and Roundness Measurement - 2D](principal_diameters_2d.ipynb)

## Description
The first one finds and plots the principal axes, and calculates the principal diameters of an object. The aim is to characterize fracture planes in a CT scanned soil sample using their three principal diameters and their relationships to each other. The notebook illustrates this approach on the following shapes:
1. Cube
2. Sphere
3. Cylinder
4. Slit
5. Rotated Slit
6. Ellipsoid
7. Dented Sphere

The second notebook uses the same principle to calculate the principal diameters in 2D. Then, it finds the sphericity and roundness of an object. This notebook extends the first one to analyze grains (disconnected 2D grains isolated from a [dataset](https://www.digitalrocksportal.org/projects/244) from [Digital Rocks Portal](https://www.digitalrocksportal.org/)) for estimating roundness and sphericity in the 2024 UT Geoscience Hackhathon. The grains are segmented using [Segment Every Grain](https://github.com/zsylvester/segmenteverygrain) model.
