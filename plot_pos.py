import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

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


import numpy as np

import matplotlib.pyplot as plt
from skspatial.objects import Points, Line
from skspatial.plotting import plot_3d, plot_2d
from collections import deque
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', required=True, action='store', default='.', help="log file")
    parser.add_argument('-sz', '--interval_size', required=True, action='store', default='250', help="number of frames in interval")
    return parser.parse_args()

def readlog(log, CENTID):
    cent_pos = {}
    frames = []
    # Define the codec and create VideoWriter object
    with open(log, 'r+') as logfile: 
        
        for line in logfile.readlines():
            line = line.replace('[', '')
            line = line.replace(']', '')
            
            data = line.split()
            frameno = int(float(data[0]))
            
            id = int(data[1])
            if id == CENTID:
                frames.append(frameno)
                rvec = np.array(list(map(float, data[2:5])))
                tvec = np.array(list(map(float, data[5:8])))
                cent_pos[frameno] = (rvec, tvec)
            '''
            elif id < 10:
                corners = []
                for i in range(4):
                    px, py = float(data[2 + 2 * i]), float(data[2 + 2 * i + 1])
                    corners.append((px, py))
            '''
            
    return cent_pos, frames

args = get_args()
logfile = args.log
interval_size = int(args.interval_size)
positions, framenos = readlog(logfile, 10)

L = len(framenos)
data = np.empty((3, L))

xlim = [0, 0]
ylim = [0, 0]
zlim = [0, 0]

for index, frameno in enumerate(framenos):
    _, tvec = positions[frameno]
    #x, y, z = tvec
    data[:, index] = tvec

    for coord, lim in zip(tvec, [xlim, ylim, zlim]):
        lim[0] = min(lim[0], coord)
        lim[1] = max(lim[1], coord)

fromindex = {}
start = 0
for i, frameno in enumerate(framenos):
    while framenos[start] <= frameno - interval_size:
        start += 1
    fromindex[i] = start

def update_lines(num, data, line):
    num = int(num)
    start = fromindex[num]
    line.set_data(data[0:2, start:num])
    line.set_3d_properties(data[2, start:num])
    return line,

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

# Setting the axes properties

ax.set_xlim(xlim[0], xlim[1])
ax.set_ylim(ylim[0], ylim[1])
ax.set_zlim(zlim[0], zlim[1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, frames=np.linspace(0, len(framenos)-1, len(framenos)), fargs=(data, line),
                                   interval=50, blit=False)

plt.show()