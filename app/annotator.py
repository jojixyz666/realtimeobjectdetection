import cv2
import numpy as np
from datetime import datetime

class FrameAnnotator:
    def __init__(self, class_names, colors=None, thickness=2, font_scale=0.6):
        self.class_names = class_names
        self.thickness = thickness
        self.font_scale = font_scale
        
        # Generate random colors for classes if not provided
        if colors is None:
            np.random.seed(42)
            self.colors = np.random.randint(0, 255, size=(len(class_names) if class_names else 80, 3), dtype="uint8").tolist()
        else:
            self.colors = colors

    def annotate(self, frame: np.ndarray, detections: list) -> np.ndarray:
        annotated_frame = frame.copy()
        for det in detections:
            color = self.colors[det.class_id % len(self.colors)]
            
            # Draw bbox
            cv2.rectangle(
                annotated_frame, 
                (det.x1, det.y1), 
                (det.x2, det.y2), 
                color, 
                self.thickness
            )
            
            # Draw label
            label = f"{det.class_name} {det.conf:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.thickness)
            
            # Background for label
            cv2.rectangle(
                annotated_frame, 
                (det.x1, det.y1 - h - 5), 
                (det.x1 + w, det.y1), 
                color, 
                -1
            )
            # Text
            cv2.putText(
                annotated_frame, 
                label, 
                (det.x1, det.y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                self.font_scale, 
                (255, 255, 255), 
                self.thickness
            )
        return annotated_frame

    def draw_info_overlay(self, frame: np.ndarray, fps: float, obj_count: int, show_timestamp: bool) -> np.ndarray:
        overlay = frame.copy()
        
        info_text = f"FPS: {fps:.1f} | Objects: {obj_count}"
        if show_timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
            info_text += f" | {timestamp}"
            
        cv2.putText(
            overlay, 
            info_text, 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.8, 
            (0, 255, 0), 
            2
        )
        return overlay
