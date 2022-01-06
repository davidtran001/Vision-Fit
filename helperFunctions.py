import time
import cv2

def timer(startTime):
    currTime = time.time()
    return int(currTime-startTime)

def workoutPlan(exercise1, exercise2):
    return [exercise1, exercise2]

def centerText(w, h, text, font, size, thickness):
    # get boundary of this text
    textsize = cv2.getTextSize(text, font, size, thickness)[0]
    # get coords based on boundary
    textX = (w - textsize[0]) // 2
    textY = (h + textsize[1]) // 2
    return textX, textY
