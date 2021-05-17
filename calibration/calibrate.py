#!/usr/bin/python3

# Author: Maj Stenmark
# Preparation:
# Take images of a calibration grid of size (6,9) (total number of squares 7 x 10) and save in a folder.
# Script description:
# Calculates the camera matrix and distortion coefficients as described here:https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html and saves the parameters in a yaml file
# Input arguments:
# image_folder: the folder name with calibration images.
# out_data: the name of the yaml-file
# square_size: optional parameter for square size, the side of one of the black or white squares on the calibration grid. Default is 25 mm. 
# Output:
# yaml file with camera matrix and distortion coefficients.


import cv2
import numpy as np
import os
import glob
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--image_folder', required=True, action='store', default='.', help="folder")
    parser.add_argument('-o', '--out_data', required=True, action='store', default='.', help="data")
    parser.add_argument('-sz', '--square_size', required=False, action='store', default='25', help="square size")
    
    return parser.parse_args()


def calibrate(img_folder, out_data, square_size_s):
    square_size = float(square_size_s)
    CHECKERBOARD = (6,9)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = []

    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    #objp *= square_size
    prev_img_shape = None
    # Extracting path of individual image stored in a given directory
    images = glob.glob('./' + img_folder + '/*')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        cv2.imshow('gray',gray)
        cv2.waitKey(1)
        
        
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display
        them on the images of checker board
        """
        if ret == True:

            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('img',img)
        cv2.waitKey(1)
        
    
    cv2.destroyAllWindows()

    h,w = img.shape[:2]

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    camera_matrix= mtx.tolist()
    dist_coeff = dist.tolist()
    data = {"camera_matrix": camera_matrix, "dist_coeff": dist_coeff}
    fname = out_data


    import yaml
    with open(fname, "w") as f:
        yaml.dump(data, f)
    print('OK')

def main():
    args = get_args()
    calibrate(args.image_folder, args.out_data, args.square_size)

if __name__ == '__main__':
    main()
