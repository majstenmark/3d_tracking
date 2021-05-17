#!/usr/bin/python3

# Author: Maj Stenmark
# Preparation:
# Take a video of a calibration grid (of size 6,9) from different angles with the camera that you want to calibrate. 
# Script description:
# From a video of a calibration grid, this script saves every 5th image into the img folder.
# Input arguments:
# video: video of a calibration grid from different angles
# image_folder: the folder name where the images should be saved.
# Output:
# images named 'calibxxxx.jpg' in the image_folder.


import numpy as np
import cv2
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video")
    parser.add_argument('-f', '--image_folder', required=True, action='store', default='.', help="folder")
    return parser.parse_args()

def get_frame(frame_no, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    return cap.read()

def create_imgs(video, out_folder):
    folder = './' + out_folder
    cap = cv2.VideoCapture(video)
    tot  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Tot ', tot)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for k in range(1, tot, 5):
        _, frame = get_frame(k, cap)
        lname = folder + '/calib{}.jpg'.format(k)
        cv2.imshow('Testing', frame)
        
        key = cv2.waitKey(1)
        cv2.imwrite(lname, frame)
        print(lname)

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()
def main():
    args = get_args()
    create_imgs(args.video, args.image_folder)

if __name__ == '__main__':
    main()
