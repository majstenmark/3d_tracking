import numpy as np
import cv2 as cv
import cv2.aruco as aruco
import math
import warnings
from cad_model import model, model_corners
import glob
import calibration_data
import tracking_die
from collections import defaultdict as dd
from scipy.spatial.transform import Rotation 


cv_file = cv.FileStorage()
cv_file.open('maj_stereoMap.xml', cv.FileStorage_READ)

camera_left = cv_file.getNode('camera_left').mat()
camera_right = cv_file.getNode('camera_right').mat()
dist_left = cv_file.getNode('dist_left').mat()
dist_right = cv_file.getNode('dist_right').mat()
trans = cv_file.getNode('trans').mat()
projL = cv_file.getNode('projL').mat()
projR = cv_file.getNode('projR').mat()

def drawcenter(img, imgpts):
    corner = tuple(map(int, imgpts[0].ravel()))
    img = cv.line(img, corner, tuple(map(int, imgpts[1].ravel())), (255,0,0), 5)
    img = cv.line(img, corner, tuple(map(int, imgpts[2].ravel())), (0,255,0), 5)
    img = cv.line(img, corner, tuple(map(int, imgpts[3].ravel())), (0,0,255), 5) ## NOTE THAT THIS IS BGR AND Z IS RED
    return img

def tolist(v):
    x, y, z = v[0][0], v[1][0], v[2][0]    
    return [x, y, z]

def stereo_test(L, R, projL, projR):
    f = -1
    alpha = 66
    frame_left = cv.imread(L)
    frame_right = cv.imread(R)
    
    frame_right, frame_left = calibration_data.undistortRectify(frame_right, frame_left)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)#Aruco marker size 4x4 (+ border)
    parameters =  aruco.DetectorParameters_create()

   
    grayL = cv.cvtColor(frame_left, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(frame_right, cv.COLOR_BGR2GRAY)
    cornersL, idsL, rejectedImgPointsL = aruco.detectMarkers(grayL, aruco_dict, parameters=parameters)
    markedL = frame_left.copy()#aruco.drawDetectedMarkers(color_image.copy(), corners)#, ids)#Fails without the '.copy()', the 'drawDetectedMarkers' draw contours of the tags in the image
            
    markedL = aruco.drawDetectedMarkers(markedL, cornersL, idsL, (0,255,0))

    cornersR, idsR, rejectedImgPointsR = aruco.detectMarkers(grayR, aruco_dict, parameters=parameters)
    markedR = frame_right.copy()#aruco.drawDetectedMarkers(color_image.copy(), corners)#, ids)#Fails without the '.copy()', the 
    markedR = aruco.drawDetectedMarkers(markedR, cornersR, idsR, (0,255,0))
    axis = np.float32([[0, 0, 0],[3,0,0], [0,3,0], [0,0,3]]).reshape(-1,3)
    K, Rot, t,_,_,_,_ = cv.decomposeProjectionMatrix(projL)
    
    if len(cornersL) == 0 or len(cornersR) == 0:
        print('Not found')
        return
    
    points3dL = []
    points3dR = []
    cornL = []
    cornR = []
    inleft = set()
    for id in idsL:
        inleft.add(id[0])

    
    inboth = set()
    for id in idsR:
        if id[0] in inleft:
            inboth.add(id[0])
  
    ids = []
    for index, id in enumerate(idsL): 
        if id[0] in model_corners and id[0] in inboth:
            #for corner in model_corners[id[0]]:
            #    points3dL.append(corner) 
            for corner_list in cornersL[index]:
                for corner in corner_list:
                    cornL.append(corner)
    for index, id in enumerate(idsR): 
        
        if id[0] in model_corners and id[0] in inboth:
            
            #for corner in model_corners[id[0]]:
            #    points3dR.append(corner)
            for corner_list in cornersR[index]:
                for corner in corner_list:
                    cornR.append(corner)
                    ids.append(id[0])
   
    real3d = dd(list)
    print('##################')
    #a corner is a list of points. Something does not work
    for i in range(len(cornR)):
        idx = ids[i]
        leftpoints = cornL[i]
        rightpoints = cornR[i]
    
        
        position = cv.triangulatePoints(projL, projR, leftpoints, rightpoints)
        
        pos = position[0:3]/position[3]
        li = tolist(pos)
        print('Corner positions', li)
        real3d[idx].append(li)
        rvec = np.array([0., 0., 0.])
        tvec = np.array([li[0], li[1], li[2]])
        print('Triang position')
        print(tvec)
        
        #proj, jac = cv.projectPoints(axis, rvec, tvec, K, dist_left)
        #markedL = drawcenter(markedL, proj)
    
    diecenter, dierot = tracking_die.getpos(real3d)
    
    markermat = tracking_die.create_mat(real3d[ids[0]])

    markerrot = markermat[0:3, 0:3]
    markerpos = markermat[0:3, 3]
    tvecmarker = markerpos
    rotmatmarker = Rotation.from_matrix(markerrot)
    rvecmarker = rotmatmarker.as_rotvec()
   


    
    print('Diecenter', diecenter)
    rotmat = Rotation.from_matrix(dierot)
    rvec = np.zeros((1, 3), np.float32)
    rvec = rotmat.as_rotvec()
    tvec = diecenter 
    proj, jac = cv.projectPoints(axis, rvec, tvec, K, dist_left)
    markedL = drawcenter(markedL, proj)
    


    proj2, jac2 = cv.projectPoints(axis, rvecmarker, tvecmarker, K, dist_left)
    markedL = drawcenter(markedL, proj2)
    

    cv.imshow("frame right", markedR) 
    cv.imshow("frame left", markedL)


            # Hit "q" to close the window
    if cv.waitKey(0) & 0xFF == ord('q'): 
        exit()



def main():

   
    
    
   
    
    save_folder = '/Users/maj/repos/ComputerVision_cloned_niconielsen32/stereoVisionCalibration/images/aruco'
    #
    no = [1626, 1631, 1740, 1743, 1744, 1745, 1746, 1747, 1749, 1750, 1922, 1931, 1937, 1938, 1944, 1945, 1947, 1948, 1949, 1950, 1952, 1954, 1955, 1956, 1957, 1959, 1960, 1962, 1963, 1964, 1968, 1969, 1971, 1974, 1994, 2092, 2093, 2102, 2106, 2119, 2141, 2144, 2145, 2148, 2150, 2153, 2157, 2198, 2199, 2200, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2213, 2214, 2253, 2257, 2288, 2289, 2290, 2291, 2292, 2306, 2307, 2308, 2309, 2310, 2337, 2338, 2339, 2340, 2342, 2343, 2344, 2345, 2346, 2347, 2348, 2349, 2350, 2351, 2372, 2373, 2378, 2379, 2382, 2383, 2482, 2485, 2542, 2543, 2544, 2547, 2548, 2549, 2557, 2559, 2566, 2676, 2689, 2690, 2697, 2699, 2709, 2774, 2786, 2787, 2800, 2802, 2803, 2805, 2806, 2807, 2808, 2809, 2811, 2816, 2819, 2820, 2824, 2825, 2877, 2883, 2885, 2886, 2887, 2888, 2889, 2890, 2891, 2892, 2893, 2894, 2895, 2896, 2897, 2898, 2899, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2907, 2908, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2917, 2919, 2920, 2943, 2946, 2947, 2948, 2962, 3079, 3100, 3102, 3103, 3104, 3105, 3106, 3108, 3109, 3113, 3116, 3117, 3118, 3119, 3149, 3150, 3151, 3152, 3153, 3154, 3155, 3156, 3157, 3159, 3160, 3168, 3174, 3175, 3178, 3179, 3180, 3181, 3182, 3183, 3184, 3185, 3186, 3187, 3188, 3189, 3195, 3197, 3200, 3201, 3202, 3204, 3205, 3206, 3207, 3208, 3212, 3213, 3214, 3215, 3216, 3217, 3218, 3219, 3227, 3230, 3231, 3232, 3233, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3241, 3242, 3245, 3247, 3255, 3256, 3257, 3448, 3475, 3477, 3480, 3483, 3493, 3496, 3521, 3538, 3539, 3540, 3542, 3545, 3546, 3547, 3549, 3550, 3553, 3557, 3563, 3564, 3565, 3566, 3568, 3570, 3574, 3575, 3597, 3620, 3629, 3632, 3633, 3635, 3637, 3642, 3643, 3644, 3646, 3647, 3657, 3660, 3679, 3691, 3692, 3701, 3702, 3703, 3704, 3709, 3710, 3711, 3712, 3714, 3717, 3718, 3721, 3722, 3724, 3725, 3726, 3727, 3728, 3730, 3733, 3734, 3735, 3740, 3746, 3751, 3755, 3756, 3757, 3760, 3761, 3762, 3763, 3764, 3765, 3766, 3767, 3768, 3769, 3770, 3771, 3774, 3775]
    for n in no:
        n = str(n)
        L = save_folder + '/imageL' + n + '.png'
        R = save_folder + '/imageR' + n + '.png'
        #identify(L, R, camera_left, dist_left, camera_right, dist_right)
        stereo_test(L, R, projL, projR)


if __name__ == '__main__':
    main()
