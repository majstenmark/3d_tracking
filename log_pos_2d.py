#!/usr/bin/python3

# Author: Maj Stenmark
# Preparation:
# Film video where the tracking device is used.
# Script description:
# Creates a log file with single marker positions (tvec and rvec) and calculates the center position if more than 'minSeen' markers are visible. It saves a video where the markers are drawn.
# Input arguments:
# video: video to analyse
# out_video: video where the markers and center is drawn.
# camera_data: yaml file with camera calibration parameters
# outfile: log file with the markers and center positions.
# min: minimum number of visible markers to use for center estimation
# Output: 
# log file with data from the marker positions and center position. Video where the markers are drawn. The center has ID 10.

import numpy as np
import cv2
import cv2.aruco as aruco
import math
import warnings
from cad_model import model, model_corners
import glob
import argparse
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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video file")
    parser.add_argument('-o', '--out_video', required=True, action='store', default='.', help="video file")
    
    parser.add_argument('-cd', '--camera_data', required=True, action='store', default='.', help="camera data")
    parser.add_argument('-l', '--log', required=True, action='store', default='.', help="log file")
    parser.add_argument('-m', '--min', required=False, action='store', default='1', help="Out file")
    
    return parser.parse_args()


def process(file, out_video, camera_matrix, dist_coeff, log):

    markerlength = 9.0

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)#Aruco marker size 4x4 (+ border)
    parameters =  aruco.DetectorParameters_create()

    cap = cv2.VideoCapture(file)
    # Define the codec and create VideoWriter object
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frametot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)+ 0.5)
    
    codec = 'mjpg'
    font = cv2.FONT_HERSHEY_SIMPLEX
    guess = False
    size = (width, height)
    with open(log, 'w+') as logfile: 
        rvec = np.array([0., 0., 0.])
        tvec = np.array([0., 0., 0.])
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                ##print("Can't receive frame (stream end?). Exiting ...")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            marked = frame.copy()#aruco.drawDetectedMarkers(color_image.copy(), corners)#, ids)#Fails without the '.copy()', the 'drawDetectedMarkers' draw contours of the tags in the image
            
            marked = aruco.drawDetectedMarkers(marked, corners, ids, (0,255,0))

            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            
            crns = []
            frameno = cap.get(cv2.CAP_PROP_POS_FRAMES)

            n = 0

            if ids is None:
                
                cv2.imshow('frame',marked)
                key = cv2.waitKey(1)
                guess = False
                rvec = np.array([0., 0., 0.])
                tvec = np.array([0., 0., 0.])

                if key == ord('q'):
                    break
            else:
                for index, id in enumerate(ids): 
                    if id[0] in model_corners:
                        n += 1
                        
                        for corner_list in corners[index]:
                            for corner in corner_list:
                                crns.append(corner)

                            logfile.write('{} {} {} {} {} {}\n'.format(frameno, id[0], corner_list[0], corner_list[1], corner_list[2], corner_list[3]))
                
          

            cv2.putText(marked,f'{int(frameno)}/{frametot}',(8,25), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow('frame',marked)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            if key == ord('p'):
                key = cv2.waitKey(0) #wait until any key is pressed

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()
        print(f'Total no frames in {file} is {frametot}')

def main():
    #args = get_args()
    
    video = '/Users/maj/repos/3d_tracking/videos/yumi_square/yumi_square_left_sync.mp4'
    log = '/Users/maj/repos/3d_tracking/videos/yumi_square/poslog_left_20220309.txt'
    #mn = int(args.min)  
    process(video,None, camera_left, dist_left, log)


if __name__ == '__main__':
    main()
