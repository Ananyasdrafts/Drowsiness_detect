from threading import Thread
import winsound

class AlarmManager:
    def __init__(self):
        self.alarm_status = False
        self.alarm_status2 = False
        self.saying = False

    def alarm(self, msg, frequency=1000, duration=500):
        while self.alarm_status:
            winsound.Beep(frequency, duration)

        if self.alarm_status2:
            self.saying = True
            winsound.Beep(frequency + 500, duration)
            self.saying = False

    def start_alarm(self, msg, alarm_type=1):
        if alarm_type == 1:
            t = Thread(target=self.alarm, args=(msg, 1000))
        elif alarm_type == 2:
            t = Thread(target=self.alarm, args=(msg, 1500))
        t.daemon = True
        t.start()
