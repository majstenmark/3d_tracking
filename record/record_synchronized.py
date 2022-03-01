import numpy as np
import cv2 as cv
import os, sys
import socket
from datetime import datetime

capL = cv.VideoCapture(1)
capR = cv.VideoCapture(0) #change this to 2!
PATH = os.getcwd()
width = int(capL.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(capL.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)

widthR = int(capR.get(cv.CAP_PROP_FRAME_WIDTH) + 0.5)
heightR = int(capR.get(cv.CAP_PROP_FRAME_HEIGHT) + 0.5)
codec = 'mjpg'
fps = 25

s = socket.socket()
port = 1025
#address = ('192.168.125.1', port) #CHANGE THIS
address = ('127.0.0.1', port)
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

leftout = PATH + f'/left_{timestamp}.mp4'
outL = cv.VideoWriter(leftout, cv.VideoWriter_fourcc(*codec), fps, (width, height))
rightout = PATH + f'/right_{timestamp}.mp4'
outR = cv.VideoWriter(rightout, cv.VideoWriter_fourcc(*codec), fps, (widthR, heightR))

try:
  s.connect(address) 
except:
    while True:
        if (s.connect(address) != True ):
            break
        print("trying to connect")

'''
def createfolder(suffix):
    imgpath = PATH + '/images'
    if not os.path.isdir(imgpath):
        os.mkdir(imgpath)
    path = os.path.join(PATH, f'images/stereo{suffix}')
    if not os.path.isdir(path):    
        os.mkdir(path)
   
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
'''

def getrobpos():
    s.send(bytes("1", 'utf-8'))
    data = s.recv(4096)
    if len(data)>0:
        res=str(data)
        print(res[2:len(res)-1])
        return res
    return 'No msg'

def save(cap, t, suffix):
    succes1, img = cap.read()
    if succes1:
        #path = PATH + f'/images/stereo{suffix}/image{suffix}' + str(t) + '.png'

        #cv.imwrite(path, img)
        if suffix == 'L':
            outL.write(img)
            cv.imshow(f"frame {suffix}", img)
        
        else:
            outR.write(img)        



def tostring(robpos, t):
    return f'{t} {robpos}'
    #return f'{t} {robpos[0]} {robpos[1]} {robpos[2]} {robpos[3]} {robpos[4]} {robpos[5]} {robpos[6]}\n'

def main():
    t = 0
    #createfolder('L')
    #createfolder('R')
    
    with open(f'roblog_{timestamp}.txt', 'w+') as robfile:
        while True:
            robpos = getrobpos()

            save(capL, t, 'L') #CHANGE THIS
            save(capR, t, 'R') #CHANGE THIS
            robfile.write(tostring(robpos, t))
            
            k = cv.waitKey(1)
            if k == ord('q'):
                break

    capL.release()
    capR.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()