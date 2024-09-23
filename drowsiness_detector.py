import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils

class DrowsinessDetector:
    def __init__(self, eye_thresh=0.3, yawn_thresh=20, consec_frames=30):
        self.EYE_AR_THRESH = eye_thresh
        self.YAWN_THRESH = yawn_thresh
        self.EYE_AR_CONSEC_FRAMES = consec_frames
        self.COUNTER = 0
        self.alarm_status = False
        self.alarm_status2 = False
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def final_ear(self, shape):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        return (ear, leftEye, rightEye)

    def lip_distance(self, shape):
        top_lip = shape[50:53]
        top_lip = np.concatenate((top_lip, shape[61:64]))
        low_lip = shape[56:59]
        low_lip = np.concatenate((low_lip, shape[65:68]))

        top_mean = np.mean(top_lip, axis=0)
        low_mean = np.mean(low_lip, axis=0)

        distance = abs(top_mean[1] - low_mean[1])
        return distance

    def analyze_frame(self, gray, rect):
        shape = self.predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        ear, leftEye, rightEye = self.final_ear(shape)
        distance = self.lip_distance(shape)

        return ear, distance, leftEye, rightEye, shape
