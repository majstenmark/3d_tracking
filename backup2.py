
import numpy as np

import matplotlib.pyplot as plt
from skspatial.objects import Points, Line
from skspatial.plotting import plot_3d, plot_2d
import mpl_toolkits.mplot3d.axes3d as p3
from collections import deque
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt


#!/usr/bin/python3

# Author: Maj Stenmark
# Preparation:
# Run the log_in_video.py to generate the log file
# Script description:
# Plots the position in 3D during an interval of given number of frames.
# Input arguments:
# log: log file with the position data.
# interval_size: no of frames to show. 
# Output: 
# Plots positions in 3D.

seq = [3428, 3497, 3565,3634, 3702, 3770, 3838, 3907, 3970, 4043, 4111, 4180, 4248, 4316, 4384, 4454, 4521, 4589, 4658, 4727, 4795, 4862, 4931, 5000, 5067, 5135, 5204, 5272, 5340, 5409, 5477, 5546, 5614, 5681, 5750, 5819, 5886, 4862, 4931, 5000, 5067, 5135, 5204, 5272, 5340, 5409, 5477, 5546, 5614, 5681, 5750, 5819, 5886, 5955, 6023, 6091]
seq2 = [10167,10370,10570,10772,10972,11172,11375,11576,11776,11978,12178,12381,12581,12783,12985,13187,13386,13588,13789,13991,14191,14392,14594,14796,14996,15197,15399,15599,15802,16000,16203,16405,16605,16807,17007,17208,17409,17611,17812,18012]


#intervals = [[3428, 6091],
#        [7013, 9676],
#        [10167, 18013],
#        [19208, 27073]]
intervals = [seq2]



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', required=True, action='store', default='.', help="log file")
    #parser.add_argument('-sz', '--interval_size', required=True, action='store', default='250', help="number of frames in interval")
    return parser.parse_args()

def readlog2(log):
    cent_pos = []
    frames = []
    no_markers = []
    # Define the codec and create VideoWriter object
    with open(log, 'r+') as logfile: 
        lines = logfile.readlines()
        for line in lines:
            no, x, y, z, nom = map(float, line.split())
            pos = [x, y, z]
            cent_pos.append(pos)
            frames.append(no)
            no_markers.append(int(nom)//4)
            
    return cent_pos, frames, no_markers


def getside(frameno, intervals):
    for seq in intervals:
        for i in range(len(seq) -1):
            a = seq[i]
            b = seq[i+1]
            if a <= frameno <= b:
                return i%4
    return -1

args = get_args()
logfile = args.log
#interval_size = int(args.interval_size)
positions, frames, no_markers = readlog2(logfile)
cnt = 0
for i, n in enumerate(no_markers):
    side = getside(frames[i], intervals)
    if side > -1 and n == 1:
        cnt += 1
print(f'Number of data points with 1 marker(s) {cnt}')

xlim = [0, 0]
ylim = [0, 0]
zlim = [0, 0]

for index, pos in enumerate(positions):
    tvec = pos

    for coord, lim in zip(tvec, [xlim, ylim, zlim]):
        lim[0] = min(lim[0], coord)
        lim[1] = max(lim[1], coord)


# Attaching 3D axis to the figure
fig = plt.figure()
ax3d = plt.axes(projection='3d')


# Setting the axes properties



ax3d.set_title('3D Plot')
colors = ['r', 'orange', 'g', 'b']




sides = []
for i in range(4):
    sides.append([[], [], []])
#print(len(positions))


for i, pos in enumerate(positions):
    frameno = frames[i]
    no = no_markers[i]
    if no ==1:
        side = getside(frameno, intervals)
        if side > -1:
            sides[side][0].append(pos[0])
            sides[side][1].append(pos[1])
            sides[side][2].append(pos[2])
            
for i in range(4):
    x, y, z = sides[i]
    ax3d.scatter3D(x, y, z,color = colors[i],  alpha=0.4)




'''
ax3d.set_xlim(xlim[0], xlim[1])
ax3d.set_ylim(ylim[0], ylim[1])
ax3d.set_zlim(zlim[0], zlim[1])
'''
ax3d.set_xlabel('X')
ax3d.set_ylabel('Y')
ax3d.set_zlabel('Z')


plt.show()

def fitdata(points):

    line_fit = Line.best_fit(points)
    
    errs = []

    for pt in points:
        d = line_fit.distance_point(pt)
        errs.append(d)

    return errs

def printerrors(title, errs2d, errs3d):
    means2d = []
    means3d = []
    scale = 1.1 #the image is scaled 
    scalefactor = 1/scale


    mx2d = 0
    mx3d = 0
    mx2d = max(errs2d)
    mean2d = sum(errs2d)/len(errs2d)
        
    
    mx3d = max(errs3d)
    mean3d = sum(errs3d)/len(errs3d)
    
        # We can set the number of bins with the `bins` kwarg

    
    
    print('{}: Values 2D mean distance {:.4f} mm'.format(title, scalefactor * mean2d))
    print('Max 2D {}'.format(mx2d))
    
    print('{}: Values 3D mean distance {:.4f} mm'.format(title, scalefactor * mean3d))
    print('Max 3D {}'.format(mx3d))

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    n_bins = 20

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(errs2d, bins=n_bins)
    axs[1].hist(errs3d, bins=n_bins)
    plt.show()

def to_points(pos):
    x, y, z = pos
    reorder = sorted(range(len(x)), key = lambda ii: x[ii])
    coords = [[x[ii], y[ii], z[ii]] for ii in reorder]
    coord2d = [[x[ii], y[ii]] for ii in reorder]
    return coords, coord2d

errs3d_tot = []
errs2d_tot = []
for i in range(4):
    pos = sides[i]
    coords3d, coords2d = to_points(pos)
    err3d = fitdata(coords3d)
    err2d = fitdata(coords2d)
    errs3d_tot.extend(err3d)
    errs2d_tot.extend(err2d)
printerrors("Yumi stereo", errs3d_tot, errs2d_tot)