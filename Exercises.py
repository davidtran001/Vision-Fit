import cv2
import mediapipe as mp
import numpy as np
import PoseEstimationModule as pm

def bicepCurl(frame, detector):
    # Left Arm
    angle = detector.findAngle(frame, 11, 13, 15, True)
    # Right Arm
    # angle = detector.findAngle(frame, 12, 14, 16, True)
    per = np.interp(angle,(60,160),(0,100))
    bar = np.interp(angle, (60,150), (30,400))
    return angle, per, bar

def dumbellRow(frame, detector):
    # Left Arm
    angle = detector.findAngle(frame, 11, 13, 15, True)
    # Right Arm
    # angle = detector.findAngle(frame, 12, 14, 16, True)
    per = np.interp(angle,(70,140),(0,100))
    print(per)
    bar = np.interp(angle, (60,150), (30,400))
    return angle, per, bar

def dumbellRow(frame, detector):
    # Left Arm
    angle = detector.findAngle(frame, 11, 13, 15, True)
    # Right Arm
    # angle = detector.findAngle(frame, 12, 14, 16, True)
    per = np.interp(angle,(70,140),(0,100))
    print(per)
    bar = np.interp(angle, (60,150), (30,400))
    return angle, per, bar


