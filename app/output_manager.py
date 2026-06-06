import os
import cv2
import json
import numpy as np
from datetime import datetime
from app.utils import get_logger

logger = get_logger()

class OutputManager:
    def __init__(self, config_dict):
        self.save_video = config_dict.get('save_video', False)
        self.save_images = config_dict.get('save_images', False)
        self.save_json = config_dict.get('save_json', False)
        self.output_dir = config_dict.get('output_dir', './output')
        self.video_codec = config_dict.get('video_codec', 'mp4v')
        
        self.video_writer = None
        self.json_data = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "frames": []
        }
        
        if self.save_video or self.save_images or self.save_json:
            os.makedirs(self.output_dir, exist_ok=True)

    def init_video_writer(self, fps: float, resolution: tuple[int, int]) -> None:
        if not self.save_video:
            return
            
        if fps == 0:
            fps = 30.0 # fallback
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(self.output_dir, f"output_{timestamp}.mp4")
        fourcc = cv2.VideoWriter.fourcc(*self.video_codec)
        self.video_writer = cv2.VideoWriter(video_path, fourcc, fps, resolution)
        logger.info(f"Video writer initialized: {video_path} @ {fps}fps")

    def write_frame(self, frame: np.ndarray) -> None:
        if self.video_writer is not None:
            self.video_writer.write(frame)

    def save_screenshot(self, frame: np.ndarray) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        img_path = os.path.join(self.output_dir, f"screenshot_{timestamp}.jpg")
        cv2.imwrite(img_path, frame)
        logger.info(f"Screenshot saved: {img_path}")
        return img_path

    def save_image_frame(self, frame: np.ndarray, frame_id: int) -> None:
        if self.save_images:
            img_path = os.path.join(self.output_dir, f"frame_{frame_id:06d}.jpg")
            cv2.imwrite(img_path, frame)

    def log_detections(self, frame_id: int, timestamp: str, fps: float, detections: list) -> None:
        if not self.save_json:
            return
            
        frame_data = {
            "frame_id": frame_id,
            "timestamp": timestamp,
            "fps": round(fps, 2),
            "detections": [d.to_dict() for d in detections]
        }
        self.json_data["frames"].append(frame_data)

    def finalize(self) -> None:
        if self.video_writer is not None:
            self.video_writer.release()
            logger.info("Video writer released.")
            
        if self.save_json:
            json_path = os.path.join(self.output_dir, f"log_{self.json_data['session_id']}.json")
            try:
                with open(json_path, 'w') as f:
                    json.dump(self.json_data, f, indent=2)
                logger.info(f"JSON log saved: {json_path}")
            except Exception as e:
                logger.error(f"Failed to save JSON log: {e}")
