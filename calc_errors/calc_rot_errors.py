import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from calc_errors import log2sides, readcuts, readlog, side2XYZ
import numpy as np
from averageQuaternions import averageQuaternions
from scipy.spatial.transform import Rotation as R
import pyquaternion
import math
import cv2

def side2Quat(side):
    Q = []
    for rvec, _ in side:

        rot = R.from_rotvec(rvec)
        q = rot.as_quat() #scalar last
        q1 = [q[3], q[0], q[1], q[2]]
        Q.append(q1)
    return np.array(Q)

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
        
if __name__ == '__main__':
    main()