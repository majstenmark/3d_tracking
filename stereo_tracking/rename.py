import os

path = '/Users/maj/repos/ComputerVision_cloned_niconielsen32/stereoVisionCalibration/images/stereoLeft/'
for i in range(3, 46):
    src = path + 'stereoLeft' + str(i) + '.png'
    dst = path + 'imageL' + str(i) + '.png'
    os.rename(src, dst)