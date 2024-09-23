import cv2
from drowsiness_detector import DrowsinessDetector
from alarm_manager import AlarmManager
from video_streamer import VideoStreamer
from email_notifier import EmailNotifier

class MainApplication:
    def __init__(self):
        self.detector = DrowsinessDetector()
        self.alarm_manager = AlarmManager()
        self.streamer = VideoStreamer()
        self.notifier = EmailNotifier("sender@example.com", "receiver@example.com")
        self.COUNTER = 0

    def run(self):
        self.streamer.start()

        while True:
            frame = self.streamer.read_frame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = self.detector.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                ear, distance, leftEye, rightEye, shape = self.detector.analyze_frame(gray, rect)

                if ear < self.detector.EYE_AR_THRESH:
                    self.COUNTER += 1

                    if self.COUNTER >= self.detector.EYE_AR_CONSEC_FRAMES:
                        if not self.alarm_manager.alarm_status:
                            self.alarm_manager.alarm_status = True
                            self.alarm_manager.start_alarm('Drowsiness detected!', alarm_type=1)
                        self.notifier.send_alert("Drowsiness Alert", "The user is drowsy!")
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                else:
                    self.COUNTER = 0
                    self.alarm_manager.alarm_status = False

                if distance > self.detector.YAWN_THRESH:
                    if not self.alarm_manager.alarm_status2:
                        self.alarm_manager.alarm_status2 = True
                        self.alarm_manager.start_alarm('Yawning detected!', alarm_type=2)
                    self.notifier.send_alert("Yawn Alert", "The user is yawning!")
                    cv2.putText(frame, "Yawn Alert", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.streamer.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = MainApplication()
    app.run()
