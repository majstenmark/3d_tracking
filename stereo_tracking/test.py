import cv2

cap = cv2.VideoCapture(0)

num = 0

while cap.isOpened():

    succes1, img = cap.read()
    if succes1:

    
        cv2.imshow('Img 1',img)

        k = cv2.waitKey(5)

        if k == 27:
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            cv2.imwrite('images/stereoLeft/imageL' + str(num) + '.png', img)
            print("images saved!")
            num += 1
    else:
        print("No device")
        break
 

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
