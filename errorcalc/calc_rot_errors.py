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
        q1 = [q[3], q[0], q[1], q[2]] #scalar first!
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
    
    print(f'{title}: Mean angle {mean} and deviation {deviation} mm')
    print(f'{title}: Max angle {mx} and deviation {mdeviation} mm')

def sigma2(err):
    su2 = 0.0
    su = 0.0
    n = 0
    for e in err:
        su2 += e**2
        su += e
        n += 1
    mean = su/n
    return su2/n - mean **2, su/n, len(err) -1


def calc_F_stat(errors3d, title):
    s1_3d, mean1_3d,dof1_3d = sigma2(errors3d)
    #print(f'Variance {title} {s1_3d}')
    print(f'Deviation {title} {s1_3d**0.5}')


def proj2plane(q):

    r = R.from_quat([q[1], q[2], q[3], q[0]]).as_matrix() #scalar last
    transform = np.zeros((4, 4))
    transform[3, 3] = 1.0
    #print(r)
    
    axis = np.array([0, 0, 1.0, 1])
    transform[0:3, 0:3] = r
    #print(transform)
    
    prim = np.matmul(transform, axis)
    #print(f'Prim {prim}')
    vec = [prim[0], prim[1], prim[2]]
    #print('Vector', vec)
    normal = np.array([0, 0, 1.0])
    l = np.dot(vec, normal)
    proj = vec - l * normal
    #print(f'Proj {proj}')
    dx, dy = proj[0], proj[1]
    theta = math.atan2(dy, dx)
    return theta/math.pi * 180
    #print(theta)

def plot_errors(err):
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    n_bins = 20

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(err, bins=n_bins)
    plt.show()

def calc_2d(meanquat, Q):
    def mindist(a, b):
        diff = abs(a - b)
        return min(diff, 360 - diff)
    #calc proj angle 2d
    mean2d = proj2plane(meanquat)
    errs = []
    for q in Q:
        proj = proj2plane(q)
        err = mindist(mean2d, proj)
        errs.append(err)
    print(f'Projected angle {mean2d}')

    #plot_errors(errs)
    return errs




def test_proj():
    deg = -90
    rad = deg/180 * math.pi 
    s = math.cos(rad/2)
    w = math.sin(rad/2)
    q = [w, s, 0, 0]
    proj2plane(q)
        
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
    errors_2d = []
    meanErrs = []
    for i, side in enumerate(sides):
        #print(side)
        Q = side2Quat(side)

        #print(Q)
        avQ = averageQuaternions(Q)
        avQs.append(avQ)
        errs = [rad2deg(quatdist(q, avQ)) for q in Q]
        meanErr = sum(errs)/len(errs)
        qerr.extend(errs)
        meanErrs.append(meanErr)        
        err_2d = calc_2d(avQ, Q)
        errors_2d.extend(err_2d)

    mean2derr = sum(errors_2d)/len(errors_2d)
    mxang = max(errors_2d)
    print(f'Average 2D angle error {mean2derr} and max {mxang}')
    calc_F_stat(errors_2d, '2D')
    return avQs, qerr, meanErrs

def main():


    intervals = readcuts('cuts2_hres.txt')
    
    #logs = [('./logs/MAH00337_old.txt', 10), ('./logs/MAH00337min2_old.txt', 10)]
    #logs = [('log_conv_calc1_min1_hres.txt', 10), ('log_conv_calc1_min2_hres.txt', 10)]
    logs = [('log_conv_calc1_min1_scaled.txt', 10), ('log_conv_calc1_min2_scaled.txt', 10)]
    
    #logs = [('./log/MAH00337min2_recalibrated.txt', 10)]#, ('./log/MAH00337min2.txt', 10)] #, ('MAH00337_log_dodeca.txt', 12), ('MAH00337_log_dodeca_pnp.txt', 12)]
    titles = ['PNP min1', 'PNP min2'] #, 'Dodeca orig min2', 'Dodeca with Pnp min2']
    #intervals = readcuts('cuts.txt')
    for title, (logfile, centerid) in zip(titles, logs[0:1]):
    
    
        #_, cent_pos, _ = readlog('MAH00337_log_dodeca.txt', 12)
        #_, cent_pos, _ = readlog('MAH00337.txt', 10)
        
        _, cent_pos, _ , pos_cnt= readlog(logfile, centerid)
        #_, cent_pos, _ = readlog('MAH00337.txt', 10)
        sides, sides2, sides3  = log2sides(intervals, cent_pos, pos_cnt)
        avQuats, qerr, meanErr = get_rot_errors(sides) #average per side
        calc_F_stat(qerr, '3D')
        #title, qerr, meanqerr, fig
        #plotsides(sides,avQuats)
        
        
        print_rot_errors(title, qerr, meanErr, 200)
        plt.show()

if __name__ == '__main__':
    main()