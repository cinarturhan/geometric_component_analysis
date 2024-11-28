import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import skimage
from skimage.measure import regionprops, label
from mpl_toolkits.mplot3d import Axes3D
import scipy
# %matplotlib widget
# %matplotlib inline

def find_and_plot_principal_diameters_2D(binary_image, max_radius = 500):
    """
    Calculate and plot the principal diameters of a binary object.

    Parameters:
    - binary_image: 2D binary image with a single object.
    """

    props = regionprops(label(binary_image))[0]
    center = np.array(props.centroid) 
    inertia_matrix = props.inertia_tensor

    eigenvalues, eigenvectors = np.linalg.eig(inertia_matrix)
    sorted_indices = np.argsort(-eigenvalues)  # Sorted by largest eigenvalues
    eigenvectors = eigenvectors[:, sorted_indices]

    directions = [eigenvectors[:, 0], -eigenvectors[:, 0],  # Principal direction 1
                  eigenvectors[:, 1], -eigenvectors[:, 1]]  # Principal direction 2


    extracted_coords = []
    extracted_lengths = []

    max_radius = max_radius
    for direction in directions:
        for radius in range(1, max_radius + 1):
            coord = center + radius * direction
            x, y = map(int, coord)
            if 0 <= x < binary_image.shape[0] and 0 <= y < binary_image.shape[1]:
                if binary_image[x, y] == 0:  
                    extracted_coords.append(coord)
                    extracted_lengths.append(radius)
                    break

    # Plotting
    fig, ax = plt.subplots()
    # Hiding the figure numbers (otherwise, they iterate all the time)
    fig.canvas.toolbar_visible = False
    fig.canvas.header_visible = False
    fig.canvas.footer_visible = False
    ax.imshow(binary_image, cmap='gray')

    # Plotting arrows
    colors = ['red', 'red', 'blue', 'blue']
    for i, (coord, length, direction) in enumerate(zip(extracted_coords, extracted_lengths, directions)):
        ax.arrow(
            center[1], center[0],  # Arrow origin
            direction[1] * length, direction[0] * length,  # Arrow direction and length
            color=colors[i], head_width=5, head_length=5
        )
    arrow_names = ['Arrow1', 'Arrow2', 'Arrow3', 'Arrow4']

    # for arrow, coords, length in zip(arrow_names, extracted_coords, extracted_lengths):
    #     print(f"Arrow: {arrow}, Coordinates: {coords}, Length: {length}")
    
    # Principal diameters
    diameter_1 = extracted_lengths[0] + extracted_lengths[1]
    diameter_2 = extracted_lengths[2] + extracted_lengths[3]

    print(f"Principal Diameter 1: {diameter_1}")
    print(f"Principal Diameter 2: {diameter_2}")
    
    ax.set_title('Principal Diameters')
    return diameter_1, diameter_2, fig, ax 

def find_and_plot_principal_diameters(binary_volume, max_radius=500, xlim=None, ylim=None, zlim=None):
    volume = binary_volume


    props = regionprops(label(binary_volume))[0]
    center = np.array(props.centroid) 
    inertia_matrix = props.inertia_tensor

    eigenvalues, eigenvectors = np.linalg.eig(inertia_matrix)
    sorted_indices = np.argsort(-eigenvalues)  # Sorted by largest eigenvalues
    eigenvectors = eigenvectors[:, sorted_indices]

    axis_1 = eigenvectors[:,0]  
    axis_2 = eigenvectors[:,1]   
    axis_3 = eigenvectors[:,2]   

    axis_4 = -eigenvectors[:,0] 
    axis_5 = -eigenvectors[:,1] 
    axis_6 = -eigenvectors[:,2]   


    arrow_data = {
        'Arrow1': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow2': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow3': {'coords': [], 'binary_data': [], 'radius': []},

        'Arrow4': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow5': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow6': {'coords': [], 'binary_data': [], 'radius': []}
    }


    arrow_1 = Arrow3D(None, center, axis_1, length=1, color='r')
    arrow_2 = Arrow3D(None, center, axis_2, length=1, color='g')
    arrow_3 = Arrow3D(None, center, axis_3, length=1, color='b')

    arrow_4 = Arrow3D(None, center, axis_4, length=1, color='r')
    arrow_5 = Arrow3D(None, center, axis_5, length=1, color='g')
    arrow_6 = Arrow3D(None, center, axis_6, length=1, color='b')

    # Increase radius incrementally
    for radius in range(1, max_radius + 1):
        # arrow coordinates for each radius
        for arrow, arrow_obj in zip(['Arrow1', 'Arrow2', 'Arrow3', 'Arrow4', 'Arrow5', 'Arrow6'], 
                                    [arrow_1, arrow_2, arrow_3, arrow_4, arrow_5, arrow_6]):
            # coordinates for the current radius
            coord = center + radius * arrow_obj.direction

            x, y, z = map(int, coord)  # coordinates to integers
            if 0 <= x < volume.shape[0] and 0 <= y < volume.shape[1] and 0 <= z < volume.shape[2]:
                binary_data = volume[x, y, z]
            else:
                binary_data = -1  # out-of-bounds coordinates

            arrow_data[arrow]['coords'].append(coord)
            arrow_data[arrow]['binary_data'].append(binary_data)
            arrow_data[arrow]['radius'].append(radius)


    extracted_coords = []
    extracted_lengths = []
    arrow_names = []

    for arrow, data in arrow_data.items():
        zero_index = np.where(np.array(arrow_data[arrow]['binary_data'])==0)[0]  # Find indices with zero binary data
        if zero_index.size > 0:  # If zero index exists
            first_zero_index = zero_index[0]  # Get the index of the first zero binary result
            extracted_coords.append(arrow_data[arrow]['coords'][first_zero_index])  # Extract corresponding coordinates
            extracted_lengths.append(arrow_data[arrow]['radius'][first_zero_index])  # Extract corresponding length
            arrow_names.append(arrow)  # Store arrow name

    ## print the extracted coordinates and lengths
    # for arrow, coords, length in zip(arrow_names, extracted_coords, extracted_lengths):
    #     print(f"{arrow}, Coordinates: {coords}, Length: {length}")

    dimater_array = {
        'Principal Diameter 1 (red)': extracted_lengths[0]+extracted_lengths[3],
        'Principal Diameter 2 (green)': extracted_lengths[1]+extracted_lengths[4],
        'Principal Diameter 3 (blue)': extracted_lengths[2]+extracted_lengths[5],
    }
    print('\n')
    for diameter_name, diameter_length in dimater_array.items():
        print(f"{diameter_name}, Length: {diameter_length}")

    verts, faces, _, _ = skimage.measure.marching_cubes(volume, level=0)

    # Plotting
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_subplot(111, projection='3d')
    # ax.view_init(elev=30, azim=30, roll=0)
    
    # Plot the surface
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r',alpha=0.1)


    custom_coords = {
        'Arrow1': extracted_coords[0], 
        'Arrow2': extracted_coords[1],  
        'Arrow3': extracted_coords[2],
        'Arrow4': extracted_coords[3],
        'Arrow5': extracted_coords[4],
        'Arrow6': extracted_coords[5]
    }

    custom_lengths = {
        'Arrow1': extracted_lengths[0], 
        'Arrow2': extracted_lengths[1],
        'Arrow3': extracted_lengths[2],
        'Arrow4': extracted_lengths[3],
        'Arrow5': extracted_lengths[4],
        'Arrow6': extracted_lengths[5]
    }

    col = ['red','orange','blue','red','orange','blue']


    for i, info in enumerate(custom_coords.items()):
        arrow, coords = info
        direction = coords - center
        direction /= np.linalg.norm(direction)
        ax.quiver(
            center[0], center[1], center[2], direction[0], direction[1], direction[2],
            color=col[i], length=custom_lengths[arrow], arrow_length_ratio=0.1
        )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if zlim is not None:
        ax.set_zlim(zlim)

    ax.set_box_aspect([np.ptp(verts[:, 0]), np.ptp(verts[:, 1]), np.ptp(verts[:, 2])])

    plt.show()


    # Arrow class
class Arrow3D:
    def __init__(self, ax, start, direction, length=1, mutation_scale=20, arrowstyle='-|>', color='black'):
        self.ax = ax
        self.start = start
        self.direction = direction
        self.length = length
        self.mutation_scale = mutation_scale
        self.arrowstyle = arrowstyle
        self.color = color

    def draw(self):
        arrow_prop_dict = dict(mutation_scale=self.mutation_scale, arrowstyle=self.arrowstyle, color=self.color)
        end = self.start + self.length * self.direction
        self.ax.quiver(self.start[0], self.start[1], self.start[2], self.direction[0], self.direction[1],
                       self.direction[2], length=self.length, **arrow_prop_dict)
        self.ax.text(end[0], end[1], end[2], f'  {self.length}', color=self.color, fontsize=8)

# Function to plot arrows in the principal directions (radius version):
def find_and_plot_principal_radiuses(binary_volume):
    volume = binary_volume


    props = regionprops(label(binary_volume))[0]
    center = np.array(props.centroid) 
    inertia_matrix = props.inertia_tensor

    eigenvalues, eigenvectors = np.linalg.eig(inertia_matrix)
    axis_1 = eigenvectors[:,0]  
    axis_2 = eigenvectors[:,1] 
    axis_3 = eigenvectors[:,2] 


    arrow_data = {
        'Arrow1': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow2': {'coords': [], 'binary_data': [], 'radius': []},
        'Arrow3': {'coords': [], 'binary_data': [], 'radius': []}
    }

    arrow_1 = Arrow3D(None, center, axis_1, length=1, color='r')
    arrow_2 = Arrow3D(None, center, axis_2, length=1, color='g')
    arrow_3 = Arrow3D(None, center, axis_3, length=1, color='b')


    max_radius = 100  # Set maximum radius
    for radius in range(1, max_radius + 1):

        for arrow, arrow_obj in zip(['Arrow1', 'Arrow2', 'Arrow3'], [arrow_1, arrow_2, arrow_3]):

            coord = center + radius * arrow_obj.direction


            x, y, z = map(int, coord)  # coordinates to integers
            if 0 <= x < volume.shape[0] and 0 <= y < volume.shape[1] and 0 <= z < volume.shape[2]:
                binary_data = volume[x, y, z]
            else:
                binary_data = -1  # out-of-bounds coordinates


            arrow_data[arrow]['coords'].append(coord)
            arrow_data[arrow]['binary_data'].append(binary_data)
            arrow_data[arrow]['radius'].append(radius)


    # for arrow, data in arrow_data.items():
    #     print(f"Arrow: {arrow}")
    #     for coord, binary, radius in zip(data['coords'], data['binary_data'], data['radius']):
    #         print(f"Coordinate: {coord}, Binary Data: {binary}, Radius: {radius}")

    extracted_coords = []
    extracted_lengths = []
    arrow_names = []

    for arrow, data in arrow_data.items():
        zero_index = np.where(np.array(arrow_data[arrow]['binary_data'])==0)[0]  
        if zero_index.size > 0:  # If zero index exists
            first_zero_index = zero_index[0]  # Get the index of the first zero binary result
            extracted_coords.append(arrow_data[arrow]['coords'][first_zero_index])  
            extracted_lengths.append(arrow_data[arrow]['radius'][first_zero_index]) 
            arrow_names.append(arrow) 

    # # Display the extracted coordinates and lengths
    # for arrow, coords, length in zip(arrow_names, extracted_coords, extracted_lengths):
    #     print(f"Arrow: {arrow}, Coordinates: {coords}, Length: {length}")


    verts, faces, _, _ = skimage.measure.marching_cubes(volume, level=0)

    # Plotting
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r',alpha=0.1)


    custom_coords = {
        'Arrow1': extracted_coords[0],  
        'Arrow2': extracted_coords[1],  
        'Arrow3': extracted_coords[2]  
    }
    custom_lengths = {
        'Arrow1': extracted_lengths[0], 
        'Arrow2': extracted_lengths[1],  
        'Arrow3': extracted_lengths[2]
    } 

    col = ['red','orange','blue']

    # Plotting the custom arrows for each principal axis at specified coordinates and lengths
    for i, info in enumerate(custom_coords.items()):
        arrow, coords = info
        direction = coords - center
        direction /= np.linalg.norm(direction)
        ax.quiver(
            center[0], center[1], center[2], direction[0], direction[1], direction[2],
            color=col[i], length=custom_lengths[arrow], arrow_length_ratio=0.1
        )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_box_aspect([np.ptp(verts[:, 0]), np.ptp(verts[:, 1]), np.ptp(verts[:, 2])])

    plt.show()

