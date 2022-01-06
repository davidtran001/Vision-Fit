import cv2
import mediapipe as mp
#from PoseEstimationModule import rescale_frame
import PoseEstimationModule as pm
import Exercises as ex
import numpy as np

cap = cv2.VideoCapture('../../TestVideos/dumbellrow.mp4')
detector = pm.poseDetector()
rep_count = 0
dir = 0

while True:
    success, frame = cap.read()
    frame = pm.rescale_frame(frame, 50)
    frame = detector.findPose(frame, draw=False)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) > 0:
        #angle, per, bar = ex.bicepCurl(frame, detector)
        angle, per, bar = ex.dumbellRow(frame, detector)
        # check for the dumbbell curls
        if per == 100:
            if dir == 0:
                rep_count += 0.5
                dir = 1
        elif per == 0:
            if dir == 1:
                rep_count += 0.5
                dir = 0

        # Display ROM bar
        #if bar == 30:
            #cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,255,0), cv2.FILLED)
        #else:
            #cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,0,255), cv2.FILLED)
        cv2.putText(frame, f'{str(int(rep_count))} reps', (1,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    print('hi')