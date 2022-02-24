import cv2

cap = cv2.VideoCapture("/Users/maj/Movies/Version2/left_ver2_cut.mp4")
cap2 = cv2.VideoCapture("/Users/maj/Movies/Version2/right_ver2_cut.mp4")

num = 0
paused = False
next_frame = 1
current_frame = 0

while cap.isOpened():

    if not paused:
        succes1, img = cap.read()
        succes2, img2 = cap2.read()
        next_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_frame = next_frame - 1
        

    k = cv2.waitKey(1)


    if k == ord('q'):
        break
    elif k == ord('p'):
        paused = not paused
        print(paused)
    elif k== ord('b'):
        if current_frame >= 1:
            previous_frame = current_frame -1
            print(previous_frame)
            cap.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
            cap2.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
            
            succes1, img = cap.read()
            succes2, img2 = cap2.read()
            current_frame -= 1


    elif k== ord('n'):
        next_frame = current_frame + 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame)
        print(next_frame)
        succes1, img = cap.read()
        succes2, img2 = cap2.read()
        current_frame += 1
    
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('/Users/maj/repos/ComputerVision_cloned_niconielsen32/stereoVisionCalibration/images/stereoLeft/imageL' + str(num) + '.png', img)
        cv2.imwrite('/Users/maj/repos/ComputerVision_cloned_niconielsen32/stereoVisionCalibration/images/stereoRight/imageR' + str(num) + '.png', img2)
        print("images saved!")
        num += 1

    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()
