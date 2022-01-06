import cv2
import mediapipe as mp
#from PoseEstimationModule import rescale_frame
import PoseEstimationModule as pm
import helperFunctions as hf
import Exercises as ex
import numpy as np
import time

start_menu = True
#cap = cv2.VideoCapture('../../TestVideos/bicepcurl2.mp4')
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
rep_count = 0
dir = 0

startRestTime = time.time()
plan = hf.workoutPlan('dumbellRow', 'bicepCurl')
set_count = 1
rest_flag = False

workout = ex.workout()

while True:
    success, frame = cap.read()
    #frame = pm.rescale_frame(frame, 50)
    frame = detector.findPose(frame, draw=False)
    lmList = detector.findPosition(frame, draw=False)

    if start_menu:
        sx, sy = hf.centerText(frame.shape[1], frame.shape[0], 'gainz buddy', cv2.FONT_HERSHEY_PLAIN, 2, 2)
        cv2.putText(frame, 'gainz buddy', (sx,sy), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
        
    else:
        if rest_flag: # if the user is resting
            # start rest timer
            rtime = 5-hf.timer(startRestTime)
            print(rtime)
            if rtime == 0:
                rest_flag = False
            
        if len(lmList) > 0:  # if there is person detected
            if not rest_flag: # if the user is not resting
                angle, per, bar, currentExercise = workout.workoutPlan(frame, detector, set_count)
                if set_count == 4:
                    set_count = 1

                # increase rep_count for each full ROM rep 
                if per == 100:
                    if dir == 0:
                        rep_count += 0.5
                        dir = 1
                elif per == 0:
                    if dir == 1:
                        rep_count += 0.5
                        dir = 0

            # Keep track of set count
            if rep_count == 3:
                rep_count = 0
                set_count += 1
                startRestTime = time.time()
                rest_flag = True
            # Display set number
            if set_count <= 3:
                cv2.putText(frame, f'set# {str(int(set_count))}', (frame.shape[1]-200,frame.shape[0]-1), cv2.FONT_HERSHEY_PLAIN    , 2, (255,255,255), 2)
            else:
                cv2.putText(frame, f'REST!', (frame.shape[1]-200,frame.shape[0]-1), cv2.FONT_HERSHEY_PLAIN    , 2, (255,255,255), 2)
            

            # Display ROM bar
            if bar == 30:
                cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,255,0), cv2.FILLED)
            else:
                cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,0,255), cv2.FILLED)
            
            # Display rep count and current exercise 
            cv2.putText(frame, f'{str(int(rep_count))} reps', (1,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
            cv2.putText(frame, currentExercise, (frame.shape[1]-250,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)