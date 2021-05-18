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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video file")
    parser.add_argument('-o', '--out_video', required=True, action='store', default='.', help="video file")
    
    parser.add_argument('-cd', '--camera_data', required=True, action='store', default='.', help="camera data")
    parser.add_argument('-l', '--log', required=True, action='store', default='.', help="log file")
    parser.add_argument('-m', '--min', required=False, action='store', default='1', help="Out file")
    
    return parser.parse_args()


def drawcenter(img, imgpts):
    corner = tuple(map(int, imgpts[0].ravel()))
    img = cv2.line(img, corner, tuple(map(int, imgpts[1].ravel())), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(map(int, imgpts[2].ravel())), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(map(int, imgpts[3].ravel())), (0,0,255), 5)
    return img

def process(file, out_video, camera_data_file, log, minSeen = 1):

    markerlength = 9.0
    camera_matrix, dist_coeffs = camera_data.get_data(camera_data_file)
    axis = np.float32([[0, 0, 0],[3,0,0], [0,3,0], [0,0,3]]).reshape(-1,3)

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
    if out_video != '':
        out = cv2.VideoWriter('./' + out_video, cv2.VideoWriter_fourcc(*codec), fps, (width, height))
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
            points3d = []
            crns = []
            frameno = cap.get(cv2.CAP_PROP_POS_FRAMES)

            n = 0

            if ids is None:
                
                cv2.imshow('frame',marked)
                key = cv2.waitKey(1)
                guess = False
                rvec = np.array([0., 0., 0.])
                tvec = np.array([0., 0., 0.])

                if out_video != '': out.write(marked)
                if key == ord('q'):
                    break
            else:
                for index, id in enumerate(ids): 
                    if id[0] in model_corners:
                        n += 1
                        for corner in model_corners[id[0]]:
                            points3d.append(corner)
                        for corner_list in corners[index]:
                            for corner in corner_list:
                                crns.append(corner)

                            logfile.write('{} {} {} {} {} {}\n'.format(frameno, id[0], corner_list[0], corner_list[1], corner_list[2], corner_list[3]))
                
                
            if n >= minSeen:
                pts3d = np.array(points3d)
                corners = np.array(crns).reshape(4 * n , 2)
                assert(max(pts3d.shape) == 4 * n)
                assert(max(corners.shape) == 4* n)
                
                ret = cv2.solvePnP(pts3d, corners, camera_matrix, dist_coeffs, rvec, tvec, useExtrinsicGuess = guess)
                proj, jac = cv2.projectPoints(axis, rvec, tvec, camera_matrix, dist_coeffs)
                #positions.append((rvec, tvec))
                logfile.write('{} {} {} {} {} {} {} {}\n'.format(frameno, 10, rvec[0], rvec[1], rvec[2], tvec[0], tvec[1], tvec[2]))
                marked = drawcenter(marked, proj)
                guess = True
                
                
                key = cv2.waitKey(1)

                if key == ord('q'):
                    break
                if key == ord('p'):
                    key = cv2.waitKey(0) #wait until any key is pressed
            elif n>0:
                pts3d = np.array(points3d)
                corners = np.array(crns).reshape(4 * n , 2)
                assert(max(pts3d.shape) == 4 * n)
                assert(max(corners.shape) == 4* n)
                
                ret = cv2.solvePnP(pts3d, corners, camera_matrix, dist_coeffs, rvec, tvec, useExtrinsicGuess = guess)
                proj, jac = cv2.projectPoints(axis, rvec, tvec, camera_matrix, dist_coeffs)
                #positions.append((rvec, tvec))
                marked = drawcenter(marked, proj)
                guess = True
                
                
           
            else:
                guess = False
                rvec = np.array([0., 0., 0.])
                tvec = np.array([0., 0., 0.])

            cv2.putText(marked,f'{int(frameno)}/{frametot}',(8,25), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow('frame',marked)
            if out_video != '': out.write(marked)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break
            if key == ord('p'):
                key = cv2.waitKey(0) #wait until any key is pressed

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()

def main():
    args = get_args()
    
    camera_data = args.camera_data
    out_video = args.out_video
    log = args.log
    mn = int(args.min)  
    process(args.video,out_video, camera_data, log, mn)


if __name__ == '__main__':
    main()
