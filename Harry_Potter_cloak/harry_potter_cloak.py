import cv2
import numpy as np
import time

def get_limits(color):

    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV) 

    lowerlimit = hsvC[0][0][0] - 5,100,100
    upperlimit = hsvC[0][0][0] + 15,255,255

    lowerlimit = np.array(lowerlimit, dtype=np.uint8)
    upperlimit = np.array(upperlimit, dtype=np.uint8)

    return lowerlimit,upperlimit

def capture_background(cap):
    print("For the magic to begin, clear the stage! Please step out of the frame for a moment.")
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)

    backgrounds = []

    for i in range(30):
        ret,frame=cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print(f'Error capturing frame {i+1}')
        time.sleep(0.1)
    if backgrounds:
        return np.median(backgrounds,axis=0).astype(np.uint8)
    else:
        raise ValueError('Failed to capture background.')

def main():

    yellow = [0,255,255]
    lowerlimit,upperlimit = get_limits(yellow)
    
    cap = cv2.VideoCapture(0)

    background = capture_background(cap)

    while True:

        ret,frame = cap.read()

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImage, lowerlimit, upperlimit)
        inverted_mask = cv2.bitwise_not(mask)

        visible_frame = cv2.bitwise_and(frame, frame, mask=inverted_mask)
        visible_background = cv2.bitwise_and(background,background,mask=mask)

        cloak_effect = cv2.add(visible_frame,visible_background)
        cv2.imshow('frame',cloak_effect)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.release()

    cv2.destroyAllWindows()

main()
