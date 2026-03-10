import time
import cv2

class EventGenerator:

    def __init__(self):

        self.last_event_time = 0
        self.cooldown = 10

    def generate_event(self, detections, frame):

        person_count = 0

        for d in detections:

            if d["class_name"] == "person":
                person_count += 1

        if person_count == 0:
            return None

        now = time.time()

        if now - self.last_event_time < self.cooldown:
            return None

        self.last_event_time = now

        filename = f"event_{int(now)}.jpg"

        cv2.imwrite(filename, frame)

        event = {
            "camera_id":"cam_01",
            "timestamp": int(now),
            "type":"person_detected",
            "count":person_count,
            "image": filename
        }

        return event
