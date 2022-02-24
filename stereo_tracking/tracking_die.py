import numpy as np
import math
from cad_model import model, model_corners
from transforms3d.quaternions import axangle2quat, mat2quat, quat2mat
from transforms3d.affines import compose, decompose
from pytransform3d.plot_utils import make_3d_axis
from pytransform3d.transform_manager import TransformManager
import pytransform3d.rotations as Rotations

from averageQuaternions import averageQuaternions

def getmid(corners):
    mid = np.array([0., 0., 0.])
    for c in corners:
        ar = np.array(c)
        mid += ar
    return mid/4

def getnormal(corners):
    p1 = np.array(corners[0])
    #order important, the vector should point up!
    p2 = np.array(corners[3]) 
    p3 = np.array(corners[1])
    v1 = p2 - p1
    v2 = p3 - p1
    n = np.cross(v1, v2)
    magn = np.linalg.norm(n)
    return n/magn

def getplanevec(corners):
    p1 = np.array(corners[0])
    #order important, the vector should point up!
    p2 = np.array(corners[3]) 
    p3 = np.array(corners[1])
    v1 = p2 - p1
    v2 = p3 - p1
    return v1, v2

def create_mat_die(corners):
    mid_trans = getmid(corners)
    print('Mid point =', mid_trans)
    vx, vy = getplanevec(corners)
    R = Rotations.matrix_from_two_vectors(vx, vy)
        
    T = compose(mid_trans, R, [1., 1., 1., ])
    return T

def create_mat(corners):
    mid_trans = getmid(corners)
    print('Mid point =', mid_trans)
    vx, vy = getplanevec(corners)
    R = Rotations.matrix_from_two_vectors(vx, vy)
    
    
    T = compose(mid_trans, R, [1., 1., 1., ])
    return T


def tranform2origin(corners):
    
    T = create_mat_die(corners)
    Tinv = np.linalg.inv(T)
    return Tinv


def getorig(idx, points3d):
    P = create_mat(points3d)

    Tinv = transformations[idx]
    print('##############')
    print('Tinv', Tinv)
    print('P', P)
    return np.matmul(P, Tinv)


def getaverage(pos):
    mid = np.array([0., 0., 0.])
    Q = []
    for mat in pos:
        trans, rot, _, _ = decompose(mat)
        mid += trans
        #q = mat2quat(rot)
        q = rot
        Q.append(q)
    mid = mid/len(pos)
    #Q = np.array(Q)
    #q = averageQuaternions(Q)
    return mid, Q[0]




transformations = {}
for idx, corners in model_corners.items():
    print('ID = ', idx)
    
    transformations[idx] = tranform2origin(corners)
    

def getpos(corners_real3d):
    pos = []
    for idx, points3d in corners_real3d.items():
       

        alt = getorig(idx, points3d)
        pos.append(alt)
    return getaverage(pos)