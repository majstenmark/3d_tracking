import numpy as np
import cv2
import cv2.aruco as aruco
import sksurgerycore.transforms.matrix as matrix
import sksurgerycalibration.algorithms.pivot as pivot
from transforms3d.affines import compose
from transforms3d.euler import (euler2mat, mat2euler, euler2quat, quat2euler,
                     euler2axangle, axangle2euler, EulerFuncs)
from mpl_toolkits.mplot3d import proj3d
from scipy.spatial.transform import Rotation as R
from transforms3d.affines import compose
import math
import warnings
from cad_model import model, model_corners
import camera_data

cv_file = cv2.FileStorage()
cv_file.open('maj_stereoMap.xml', cv2.FileStorage_READ)

camera_left = cv_file.getNode('camera_left').mat()
camera_right = cv_file.getNode('camera_right').mat()
dist_left = cv_file.getNode('dist_left').mat()
dist_right = cv_file.getNode('dist_right').mat()
trans = cv_file.getNode('trans').mat()
projL = cv_file.getNode('projL').mat()
projR = cv_file.getNode('projR').mat()


def drawcenter(img, imgpts):
    corner = tuple(map(int, imgpts[0].ravel()))
    img = cv2.line(img, corner, tuple(map(int, imgpts[1].ravel())), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(map(int, imgpts[2].ravel())), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(map(int, imgpts[3].ravel())), (0,0,255), 5)
    return img


def process(file, out_video):

    markerlength = 10

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)#Aruco marker size 4x4 (+ border)
    parameters =  aruco.DetectorParameters_create()
    axis = np.float32([[0, 0, 0],[3,0,0], [0,3,0], [0,0,3]]).reshape(-1,3)

    # Define the codec and create VideoWriter object
    cap = cv2.VideoCapture(file)
    # Define the codec and create VideoWriter object
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    print(f'W = {width} and H = {height}')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'FPS {fps}')
    frametot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)+ 0.5)
    codec = 'mp4v'
    size = (width, height)
    last_frameno = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    #start = 257300 - 10
    #cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    if out_video != '':
        out = cv2.VideoWriter(out_video, cv2.VideoWriter_fourcc(*codec), fps, (width, height))
    
    seen = 0
    rvec = np.array([0., 0., 0.])
    tvec = np.array([0., 0., 0.])
    touse= True
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        marked = frame.copy()#aruco.drawDetectedMarkers(color_image.copy(), corners)#, ids)#Fails without the '.copy()', the 'drawDetectedMarkers' draw contours of the tags in the image
        
        marked = aruco.drawDetectedMarkers(marked, corners, ids, (0,255,0))

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        points3d = []
        crns = []
        frameno = cap.get(cv2.CAP_PROP_POS_FRAMES)
        
        cv2.putText(marked,f'{frameno}/{frametot}',(8,25), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        #out.write(marked)
        cv2.imshow('frame',marked)
        out.write(marked)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if ids is None:
            continue
        
        
    print('Seen {} of total {} frames'.format(seen, frametot))      #Seen 76589 of total 270944 frames
    #Seen 23331 of total 206454 frames
    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()


def main():

    FILE = '/Users/maj/repos/3d_tracking/videos/yumi_square/yumi_square_left_sync.mp4'
    out_video = '/Users/maj/repos/3d_tracking/videos/yumi_square/yumi_square_left_sync_marked.mp4'
    process(FILE, out_video)

if __name__ == '__main__':
    main()
  