import cv2
import mediapipe as mp
import numpy as np
import PoseEstimationModule as pm

class workout(): 
    def __init__(self):
        self.exercise_num = 0

    def workoutPlan(self, frame, detector, set_count):
        if set_count == 4:
            self.exercise_num += 1

        if self.exercise_num == 0:
            return self.dumbellRow(frame, detector)
        elif self.exercise_num == 1:
            return self.bicepCurl(frame, detector)

    def bicepCurl(self, frame, detector):
        exerciseName = 'Bicep Curl'
        # Left Arm
        angle = detector.findAngle(frame, 11, 13, 15, True)
        # Right Arm
        # angle = detector.findAngle(frame, 12, 14, 16, True)
        per = np.interp(angle,(60,150),(0,100))
        bar = np.interp(angle, (60,150), (30,400))
        return angle, per, bar, exerciseName

    def dumbellRow(self, frame, detector):
        exerciseName = 'Dumbell Row'
        # Left Arm
        angle = detector.findAngle(frame, 11, 13, 15, True)
        # Right Arm
        # angle = detector.findAngle(frame, 12, 14, 16, True)
        per = np.interp(angle,(75,140),(0,100))
        bar = np.interp(angle, (60,150), (30,400))
        return angle, per, bar, exerciseName
    
    def chinUp(self, frame, detector, rep_count, dir):
        angle = 0
        exerciseName = 'Chin Up'
        chin_pos = detector.lmList[9][2]
        per = np.interp(chin_pos,(100,240),(0,100))
        bar = np.interp(chin_pos, (100,240), (30,400))
        
        #print(per)
        return  angle, per, bar, exerciseName
