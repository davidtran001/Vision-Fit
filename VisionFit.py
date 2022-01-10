import cv2
import mediapipe as mp
#from PoseEstimationModule import rescale_frame
import PoseEstimationModule as pm
import helperFunctions as hf
import Exercises as ex
import numpy as np
import time
from playsound import playsound

start_menu = True
cap = cv2.VideoCapture('../../TestVideos/chinup.mov')
#cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
rep_count = 0
dir = 0

menu_timer = time.time()
startTime = time.time()
tempTime = time.time()
#plan = hf.workoutPlan('dumbellRow', 'bicepCurl')
set_count = 1
rest_flag = False
title_flag = True

workout = ex.workout()
#test
while True:
    success, frame = cap.read()
    #frame = pm.rescale_frame(frame, 50)
    frame = detector.findPose(frame, draw=True)
    lmList = detector.findPosition(frame, draw=False)

    if start_menu:
        pTime = menu_timer
        menu_timer = hf.timer(startTime)
        print(menu_timer)
        if int(menu_timer) > int(pTime):
            title_flag = not title_flag
            #print(title_flag)
        
        if title_flag:
            sx, sy = hf.centerText(frame.shape[1], frame.shape[0], 'STRENGTH BUDDY', cv2.FONT_HERSHEY_COMPLEX_SMALL, 2.5, 2)
            cv2.putText(frame, 'STRENGTH BUDDY', (sx,sy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2.5, (150,255,0), 2)
        else:
            sx, sy = hf.centerText(frame.shape[1], frame.shape[0], 'raise your hands to begin your workout!', cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.15, 2)
            cv2.putText(frame, 'raise your hands to begin your workout!', (sx,sy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.15, (150,255,0), 2)

        #if len(lmList) > 0:
            #print('frame shape: ',frame.shape[0]/2, lmList[20][2], lmList[19][2])
        if len(lmList) > 0 and lmList[20][2] < frame.shape[0]/3 and lmList[19][2] < frame.shape[0]/3:
            start_menu = False
            print('frame shape: ',frame.shape[0]/2, lmList[20][2], lmList[19][2])
    else:
        if rest_flag: # if the user is resting
            # start rest timer
            pTime = tempTime
            tempTime = hf.timer(startTime)
            rTime = 5-tempTime
            # display rest timer
            # select color of text
            if rTime > 3: 
                rest_colorB, rest_colorG, rest_colorR = 150,255,0 # seafoam green
            else:
                rest_colorB, rest_colorG, rest_colorR = 0,0,255 # red
                # if int(tempTime) > pTime:
                #     playsound('countdown.mp3')

            sx, sy = hf.centerText(frame.shape[1], frame.shape[0], str(rTime), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, 2)
            cv2.putText(frame, str(rTime), (sx,sy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (rest_colorB, rest_colorG, rest_colorR), 2)

            if rTime == 0:
                rest_flag = False

        else:   
            if len(lmList) > 0:  # if there is person detected
                #print(lmList)
                if not rest_flag: # if the user is not resting
                    #angle, per, bar, currentExercise = workout.workoutPlan(frame, detector, set_count)
                    #print(detector.lmList[9][2])
                    angle, per, bar, currentExercise = workout.chinUp(frame, detector, rep_count, dir)

                    if set_count == 4:
                        set_count = 1

                    # increase rep_count for each full ROM rep 
                    print(per)
                    if per == 100:
                        if dir == 0:
                            rep_count += 0.5
                            dir = 1
                    elif per == 0:
                        if dir == 1:
                            rep_count += 0.5
                            dir = 0
                #print(rep_count)
                # Keep track of set count
                if rep_count == 5:
                    rep_count = 0
                    set_count += 1
                    startTime = time.time()
                    rest_flag = True

                # Display set number
                if set_count <= 3:
                    cv2.putText(frame, f'set# {str(int(set_count))}', (frame.shape[1]-120,frame.shape[0]-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2)
                else:
                    cv2.putText(frame, f'REST!', (frame.shape[1]-200,frame.shape[0]-1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2)
                

                # Display ROM bar
                if bar == 30:
                    cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,255,0), cv2.FILLED)
                else:
                    cv2.rectangle(frame, (500, int(bar)), (1175, 400), (0,0,255), cv2.FILLED)
                
                # Display rep count and current exercise 
            cv2.putText(frame, f'{str(int(rep_count))} reps', (10,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2)
        cv2.putText(frame, currentExercise, (frame.shape[1]-250,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255,255,255), 2)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)