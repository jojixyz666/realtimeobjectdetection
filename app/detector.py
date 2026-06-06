import os
from ultralytics import YOLO
from app.utils import get_logger
import sys

logger = get_logger()

class Detection:
    def __init__(self, class_id, class_name, conf, x1, y1, x2, y2):
        self.class_id = int(class_id)
        self.class_name = class_name
        self.conf = float(conf)
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        self.center_x = self.x1 + self.width // 2
        self.center_y = self.y1 + self.height // 2

    def to_dict(self):
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "confidence": round(self.conf, 3),
            "bbox": {
                "x1": self.x1,
                "y1": self.y1,
                "x2": self.x2,
                "y2": self.y2,
                "width": self.width,
                "height": self.height,
                "center_x": self.center_x,
                "center_y": self.center_y
            }
        }

class YOLO26Detector:
    def __init__(self, model_path, conf=0.5, iou=0.45, imgsz=640, device="auto", classes=None, half=False):
        self.model_path = model_path
        self.conf = conf
        self.iou = iou
        self.imgsz = imgsz
        self.device = device
        self.classes = classes
        self.half = half
        self.model = None
        self.class_names = {}

    def load_model(self) -> None:
        logger.info(f"Loading YOLO model from {self.model_path} on device={self.device}...")
        try:
            # We use ultralytics YOLO class. If yolo26n.pt doesn't exist, it will try to download or fail.
            # To handle the case where yolo26n.pt is a mockup name, we'll catch exceptions and fallback if possible.
            try:
                self.model = YOLO(self.model_path)
            except Exception as e:
                logger.warning(f"Failed to load {self.model_path}: {e}")
                logger.info("Attempting to fallback to models/yolo11n.pt...")
                self.model_path = "models/yolo11n.pt"
                self.model = YOLO(self.model_path)
                
            self.class_names = self.model.names
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model completely. ERR-001: {e}")
            sys.exit(1)

    def detect(self, frame) -> list[Detection]:
        if self.model is None:
            return []

        # Run inference
        kwargs = {
            "source": frame,
            "conf": self.conf,
            "iou": self.iou,
            "imgsz": self.imgsz,
            "verbose": False,
            "device": None if self.device == "auto" else self.device,
            "half": self.half,
        }
        if self.classes:
            kwargs["classes"] = self.classes

        results = self.model(**kwargs)
        
        detections = []
        if not results:
            return detections
            
        result = results[0]
        boxes = result.boxes
        
        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                
                det = Detection(
                    class_id=cls_id,
                    class_name=self.class_names.get(cls_id, "Unknown"),
                    conf=conf,
                    x1=xyxy[0], y1=xyxy[1], x2=xyxy[2], y2=xyxy[3]
                )
                detections.append(det)

        return detections

    def get_class_names(self) -> dict:
        return self.class_names
