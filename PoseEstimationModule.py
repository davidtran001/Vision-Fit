import cv2
import mediapipe as mp
import time
import math


def rescale_frame(frame, percent=100):
        width = int(frame.shape[1] * percent/ 100)
        height = int(frame.shape[0] * percent/ 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

class poseDetector():
    def __init__(self, mode=False, model_complexity=1, smooth=True, enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(static_image_mode=self.mode, model_complexity=self.model_complexity, smooth_landmarks=self.smooth, enable_segmentation=self.enable_segmentation, smooth_segmentation=self.smooth_segmentation, 
                                    min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Retrieve the position of each point 
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        
        # Calculate angle between each point
        length1 = math.sqrt((x2-x1)**2+(y2-y1)**2)
        length2 = math.sqrt((x3-x2)**2+(y3-y2)**2)
        length3 = math.sqrt((x3-x1)**2+(y3-y1)**2)
        # Cosine Law
        ratio = (length1**2 + length2**2 - length3**2) / (2*length1*length2)
        angle = math.degrees(math.acos(ratio)) 
        if angle < 0: angle += 360
        if draw:
            cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 2)
            cv2.line(img, (x2,y2), (x3,y3), (255,255,255), 2)
            cv2.putText(img, str(int(angle)), (x2-20, y2+50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
        return angle
        
    
def main():
    cap = cv2.VideoCapture('../PoseEstimationVideos/shadowboxing.mp4')
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img, draw=True)
        lmList = detector.findPosition(img, draw=True)
        if len(lmList) != 0:
            # print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()