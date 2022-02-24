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

def save_images(file, save_folder, prefix):


    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)#Aruco marker size 4x4 (+ border)
    parameters =  aruco.DetectorParameters_create()

    cap = cv.VideoCapture(file)
    frames = []
    # Define the codec and create VideoWriter object
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        marked = frame.copy()#aruco.drawDetectedMarkers(color_image.copy(), corners)#, ids)#Fails without the '.copy()', the 'drawDetectedMarkers' draw contours of the tags in the image
            
        marked = aruco.drawDetectedMarkers(marked, corners, ids, (0,255,0))

        frameno = cap.get(cv.CAP_PROP_POS_FRAMES)
        cv.imshow('frame',marked)
        key = cv.waitKey(1)
            
        if key == ord('q'):
            break

        if ids is not None:
            cv.imwrite(save_folder + '/' + prefix + str(int(frameno)) + '.png', frame)
            frames.append(int(frameno))
           
          
        # Release everything if job is finished
    cap.release()
    cv.destroyAllWindows()
    return frames

def extract_aruco():
    leftvideo = "/Users/maj/Movies/Version2/left_ver2_cut.mp4"
    rightvideo = "/Users/maj/Movies/Version2/right_ver2_cut.mp4"

    save_folder = '/Users/maj/repos/ComputerVision_cloned_niconielsen32/stereoVisionCalibration/images/aruco'
    frames = []

    for path, prefix in zip([leftvideo, rightvideo], ['imageL', 'imageR']):
        framelist = save_images(path, save_folder, prefix)
        frames.append(framelist)
    
    leftframes = set(frames[0])
    both = []
    for rf in frames[1]:
        if rf in leftframes:
            both.append(rf)
    print(both)

    



def main():
    
    extract_aruco()
    
   

if __name__ == '__main__':
    main()
