from imutils.video import VideoStream
import time
import imutils
import cv2

class VideoStreamer:
    def __init__(self, webcam_index=0):
        self.webcam_index = webcam_index
        self.vs = None

    def start(self):
        print("-> Starting Video Stream")
        self.vs = VideoStream(src=self.webcam_index).start()
        time.sleep(1.0)

    def read_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=450)
        return frame

    def stop(self):
        self.vs.stop()
