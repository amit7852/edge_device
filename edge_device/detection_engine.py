from ultralytics import YOLO

class DetectionEngine:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def run_inference(self, frame):

        results = self.model(frame)

        detections = []

        for r in results:

            for box in r.boxes:

                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if conf < 0.5:
                    continue

                name = self.model.names[cls]

                x1,y1,x2,y2 = box.xyxy[0]

                detections.append({
                    "class_name": name,
                    "confidence": conf,
                    "bbox":[int(x1),int(y1),int(x2),int(y2)]
                })

        return detections
