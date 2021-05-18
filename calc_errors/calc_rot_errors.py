import sys
sys.path.insert(1, '/Users/maj/repos/tracker/')
from transforms3d.euler import (euler2mat, mat2euler, euler2quat, quat2euler,
                     euler2axangle, axangle2euler, EulerFuncs)

from skspatial.objects import Points, Line
from skspatial.plotting import plot_3d
from calc_errors import log2sides, readcuts, readlog, side2XYZ
import numpy as np
from averageQuaternions import averageQuaternions
from scipy.spatial.transform import Rotation as R
import pyquaternion
import math
import cv2
import matplotlib.pyplot as plt
from DrawArrows import drawArrow

def side2Quat(side):
    Q = []
    for rvec, _ in side:

        rot = R.from_rotvec(rvec)
        q = rot.as_quat() #scalar last
        q1 = [q[3], q[0], q[1], q[2]]
        Q.append(q1)
    return np.array(Q)
'''
def side2Rot(side):
    yaws = []
    rxs = []
    rys = []    
    for rvec, _ in side:

        rx, ry, rz = rvec[0], rvec[1], rvec[2]
        yaw = rz
        new_x = math.sin(yaw)
        new_y = math.cos(yaw)
        yaws.append(yaw)
        rxs.append(new_x)
        rys.append(new_y)
        
    return yaw, rxs, rys
''' 
def fromside(side):
    X, Y, Z = [], [], []
    RX, RY, RZ = [], [], []
    
    height = 720 
    for rvec, tvec in side:
        rx, ry, rz = rvec[0], rvec[1], rvec[2]
        x, y, z = tvec[0], height -tvec[1], tvec[2]
        X.append(x)
        Y.append(y)
        Z.append(z)
        RX.append(rx)
        RY.append(ry)
        RZ.append(rz)
    return X, Y, Z, RX, RY, RZ


def plotsides(sides, avQuats):
    INF = 10**12
    xmin, ymin, zmin, xmax, ymax, zmax = INF, INF, INF, 0, 0, 0
    colors = ['r', 'b', 'g', 'orange']
    sidecoords = []

    fig = plt.figure(f'Rotation')
    ax = fig.add_subplot(111, projection='3d')

    
    for i, side in enumerate(sides[1:2]):
        
        X, Y, Z, RX, RY, RZ = fromside(side)

        xmin = min(xmin, min(X))
        ymin = min(ymin, min(Y))
        zmin = min(zmin, min(Z))
        xmax = max(xmax, max(X))
        ymax = max(ymax, max(Y))
        zmax = max(zmax, max(Z))
        q = avQuats[i]
        rx, ry, rz = quat2euler(q)
        avx = sum(X) / len(X)
        avy = sum(Y) / len(Y)
        avz = sum(Z) / len(Z)
        
        #drawArrow(ax, avx, avy, avz, rx, ry, rz, 20)

        #ax.scatter(X, Y, Z, color = colors[i])
        for i in range(len(X)):
            x, y, z = X[i], Y[i], Z[i]
            rx, ry, rz = RX[i], RY[i], RZ[i]
            drawArrow(ax, x, y, z, rx, ry, rz, 20)

        #ax.arrow(x, y, z, rx, ry, color=colors[i])
   
    #errors2d = []
    #errors3d = []
    
    '''
    for i, (points, points2d) in enumerate(sidecoords):

        res = fitdata(points, colors[i], xmin, xmax, ymin, ymax, zmin, zmax)
        errors3d.append(res)
        
        res2d = fitdata(points2d, colors[i], xmin, xmax, ymin, ymax, zmin, zmax)
        errors2d.append(res2d)
    ''' 
        
    #p.set_xlim([-50, 200])
    #p.set_ylim([-50, 50])
    #p.set_zlim([0, 500])
    ax.autoscale(enable= True)
    ax.set_xlim([xmin -10, xmax+10])
    ax.set_ylim([ymin -10, ymax + 10])
    ax.set_zlim([zmin - 10 , zmax + 10])

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    #return errors2d, errors3d
    return [], []
    


def plot_rot_errors(title, qerr, meanqerr, pincerdist):
    n_bins = 20
    _, axs= plt.subplots(nrows = 1, ncols = 4)
 
    for i, side_qerr in enumerate(qerr):
        meanerr = meanqerr[i]
        # We can set the number of bins with the `bins` kwarg
        axs[i].hist(side_qerr, bins=n_bins)
    
def print_rot_errors(title, qerr, meanqerr, pincerdist):
    mean = sum(meanqerr)/len(meanqerr)
    mx = max(meanqerr)
    rad = deg2rad(mean)
    mrad = deg2rad(mx)
    one = deg2rad(1)
    deviation = 2 * pincerdist * math.sin(one/2)
    mdeviation = 2 * pincerdist * math.sin(mrad/2)
    
    print(f'{title}: Average angle {mean} and deviation at 195 mm: {deviation} mm')
    print(f'{title}: Max angle {mx} and deviation at 195 mm: {mdeviation} mm')
    
    
        
    
def quatdist(q1, q2):
    pq1 = pyquaternion.Quaternion(q1)
    pq2 = pyquaternion.Quaternion(q2)
    conj_pq1 = pq1.inverse
    q12 = conj_pq1 * pq2
    L = math.hypot(q12[1], q12[2], q12[3])
    angle = 2 * math.atan2(L, q12[0])

    return min(angle, 2 * math.pi - angle)

    

def rad2deg(r): return r * 180.0 / math.pi
def deg2rad(r): return r / 180.0 * math.pi

#returns degrees
def get_rot_errors(sides):
    avQs = []
    qerr = []
    meanErrs = []
    for i, side in enumerate(sides):
        #print(side)
        Q = side2Quat(side)

        #print(Q)
        avQ = averageQuaternions(Q)
        avQs.append(avQ)
        errs = [rad2deg(quatdist(q, avQ)) for q in Q]
        meanErr = sum(errs)/len(errs)
        qerr.append(errs)
        meanErrs.append(meanErr)        
        

    return avQs, qerr, meanErrs

def main():
    intervals = readcuts('cuts.txt')
    logs = [('log_min1.txt', 10), ('log_min2.txt', 10)]
    titles = ['PNP min1', 'PNP min2'] 
    #intervals = readcuts('cuts.txt')
    for title, (logfile, centerid) in zip(titles, logs):
    
        _, cent_pos, _ = readlog(logfile, centerid)
        sides = log2sides(intervals, cent_pos)
        avQuats, qerr, meanErr = get_rot_errors(sides) #average per side
        
        
        print_rot_errors(title, qerr, meanErr, 200)
        plt.show()

if __name__ == '__main__':
    main()