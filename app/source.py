import cv2
import time
import numpy as np
from app.utils import get_logger

logger = get_logger()

class VideoSource:
    def __init__(self, source_input, fps_limit=0, resolution=None):
        # Convert "0" to integer 0 for webcam
        if isinstance(source_input, str) and source_input.isdigit():
            self.source = int(source_input)
        else:
            self.source = source_input
            
        self.fps_limit = fps_limit
        self.resolution = resolution
        self.cap = None
        self._last_frame_time = 0.0

    def open(self) -> bool:
        logger.info(f"Opening video source: {self.source}")
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            logger.error(f"Failed to open source {self.source}")
            return False
            
        if self.resolution:
            width, height = self.resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if actual_w != width or actual_h != height:
                self.software_resize = (width, height)
                logger.info(f"Requested resolution: {width}x{height}, Camera returned: {actual_w}x{actual_h}. Applying software resize.")
            else:
                self.software_resize = None
                logger.info(f"Requested resolution: {width}x{height}, Actual: {actual_w}x{actual_h}")
            
        return True

    def read(self) -> tuple[bool, np.ndarray | None]:
        if self.cap is None or not self.cap.isOpened():
            return False, None

        if self.fps_limit > 0:
            time_between_frames = 1.0 / self.fps_limit
            current_time = time.time()
            elapsed = current_time - self._last_frame_time
            if elapsed < time_between_frames:
                # Need to wait before reading next frame, to respect fps limit
                time.sleep(time_between_frames - elapsed)
        
        ret, frame = self.cap.read()
        self._last_frame_time = time.time()
        
        if ret and getattr(self, 'software_resize', None):
            frame = cv2.resize(frame, self.software_resize)
            
        return ret, frame

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
            logger.info("Video source released")

    def get_fps(self) -> float:
        if self.cap is not None and self.cap.isOpened():
            return self.cap.get(cv2.CAP_PROP_FPS)
        return 0.0

    def get_resolution(self) -> tuple[int, int]:
        if self.cap is not None and self.cap.isOpened():
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return width, height
        return 0, 0
