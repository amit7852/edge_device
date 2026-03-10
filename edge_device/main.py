
from camera_capture import Camera
from detection_engine import DetectionEngine
from event_generator import EventGenerator
from uplink_client import send_event
from motion_sensor import motion_detected
import time

camera = Camera()
detector = DetectionEngine()
event_gen = EventGenerator()

while True:

    if motion_detected():

        frame = camera.get_frame()

        if frame is None:
            continue

        detections = detector.run_inference(frame)

        event = event_gen.generate_event(detections, frame)

        if event:
            send_event(event)

    time.sleep(1)
