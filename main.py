import sys
import time
import cv2
from datetime import datetime

from app.config_manager import ConfigManager
from app.source import VideoSource
from app.detector import YOLO26Detector
from app.annotator import FrameAnnotator
from app.output_manager import OutputManager
from app.utils import setup_logger

def show_model_menu(default_path):
    print("\n" + "="*40)
    print("        MODEL SELECTION MENU")
    print("="*40)
    print("1. YOLOv8n (yolov8n.pt) - Fast & Light")
    print("2. YOLOv8s (yolov8s.pt) - Better Accuracy")
    print("3. YOLOv11n (yolo11n.pt) - Latest YOLO")
    print("4. YOLO26n (yolo26n.pt) - Config Default")
    print("5. Custom Model Path")
    print("="*40)
    
    choice = input("Select a model [1-5] (default 1): ").strip()
    
    if choice == '1' or choice == '':
        return 'models/yolov8n.pt'
    elif choice == '2':
        return 'models/yolov8s.pt'
    elif choice == '3':
        return 'models/yolo11n.pt'
    elif choice == '4':
        return 'models/yolo26n.pt'
    elif choice == '5':
        custom = input("Enter custom model path: ").strip()
        return custom if custom else default_path
    else:
        return 'models/yolov8n.pt'

def show_device_menu(default_device):
    print("\n" + "="*40)
    print("        DEVICE SELECTION MENU")
    print("="*40)
    print("1. Auto (Default)")
    print("2. CPU")
    print("3. NVIDIA GPU (CUDA)")
    print("4. AMD GPU (DirectML)")
    print("="*40)
    
    choice = input("Select a device [1-4] (default 1): ").strip()
    
    if choice == '2':
        return 'cpu'
    elif choice == '3':
        return 'cuda'
    elif choice == '4':
        return 'dml'
    else:
        return default_device

def show_resolution_menu():
    print("\n" + "="*40)
    print("        RESOLUTION SELECTION MENU")
    print("="*40)
    print("1. 320 x 240   (Minimal)")
    print("2. 640 x 480   (Default/SD)")
    print("3. 1280 x 720  (HD)")
    print("4. 1920 x 1080 (FHD)")
    print("="*40)
    
    choice = input("Select resolution [1-4] (default 2): ").strip()
    
    if choice == '1':
        return (320, 240)
    elif choice == '3':
        return (1280, 720)
    elif choice == '4':
        return (1920, 1080)
    else:
        return (640, 480)

def main():
    # 1. Load Config
    config_mgr = ConfigManager()
    
    # 2. Setup Logger
    log_level = config_mgr.get('logging', 'level', 'INFO')
    log_file = config_mgr.get('logging', 'log_file', 'logs/app.log')
    logger = setup_logger(log_level, log_file)
    logger.info("Starting Realtime Object Detection Application...")

    # 3. Load Model
    model_path = config_mgr.get('model', 'path', 'models/yolo26n.pt')
    device = config_mgr.get('model', 'device', 'auto')
    
    if "--model" not in sys.argv:
        # Prompt user if no model is explicitly provided via command line
        model_path = show_model_menu(model_path)
    
    if "--device" not in sys.argv:
        # Prompt user if no device is explicitly provided
        device = show_device_menu(device)
        
    resolution = show_resolution_menu()
    
    detector = YOLO26Detector(
        model_path=model_path,
        conf=config_mgr.get('model', 'conf_threshold', 0.5),
        iou=config_mgr.get('model', 'iou_threshold', 0.45),
        imgsz=config_mgr.get('model', 'imgsz', 640),
        device=device,
        classes=config_mgr.get('filter', 'classes'),
        half=config_mgr.get('model', 'half', False)
    )
    detector.load_model()

    # 4. Open Source
    source = VideoSource(
        source_input=config_mgr.get('source', 'input', 0),
        fps_limit=config_mgr.get('source', 'fps_limit', 0),
        resolution=resolution
    )
    if not source.open():
        logger.error("Could not open video source. Exiting.")
        sys.exit(1)

    # 5. Output Manager
    output_mgr = OutputManager(config_mgr.get('output', default={}))
    
    # Init video writer if needed
    fps = source.get_fps()
    resolution = source.get_resolution()
    output_mgr.init_video_writer(fps, resolution)
    
    # 6. Annotator
    annotator = FrameAnnotator(
        class_names=detector.get_class_names(),
        thickness=config_mgr.get('output', 'bbox_thickness', 2),
        font_scale=config_mgr.get('output', 'font_scale', 0.6)
    )

    show_window = config_mgr.get('output', 'show_window', True)
    window_name = str(config_mgr.get('output', 'window_name', 'Object Detection'))
    show_bbox = True
    show_info = True
    is_paused = False

    logger.info("Entering main loop. Press 'Q' or 'ESC' to exit.")

    frame_id = 0
    total_objects = 0
    start_session_time = time.time()

    # Initialize so they are always defined (used in key handler outside the if-not-paused block)
    frame = None
    annotated_frame = None

    # Variables for FPS calculation
    fps_calc_start = time.time()
    frames_in_interval = 0
    current_fps = 0.0

    try:
        while True:
            if not is_paused:
                ret, frame = source.read()
                if not ret:
                    logger.info("End of video stream or cannot fetch frame.")
                    break
                assert frame is not None  # narrowed: ret=True guarantees frame exists

                frame_id += 1
                timestamp_str = datetime.now().isoformat()
                
                # FPS Calculation
                frames_in_interval += 1
                now = time.time()
                if now - fps_calc_start >= 1.0:
                    current_fps = frames_in_interval / (now - fps_calc_start)
                    frames_in_interval = 0
                    fps_calc_start = now

                # Inference
                detections = detector.detect(frame)
                
                # Exclusion filter
                exclude_classes = config_mgr.get('filter', 'exclude_classes', [])
                if exclude_classes:
                    detections = [d for d in detections if d.class_id not in exclude_classes]

                total_objects += len(detections)

                # Annotation
                annotated_frame = frame.copy()
                if show_bbox:
                    annotated_frame = annotator.annotate(annotated_frame, detections)
                
                if show_info:
                    annotated_frame = annotator.draw_info_overlay(
                        annotated_frame, 
                        current_fps, 
                        len(detections),
                        bool(config_mgr.get('output', 'show_timestamp', False))
                    )

                # Outputs
                output_mgr.write_frame(annotated_frame)
                output_mgr.save_image_frame(annotated_frame, frame_id)
                output_mgr.log_detections(frame_id, timestamp_str, current_fps, detections)

                # Display
                if show_window:
                    cv2.imshow(window_name, annotated_frame)

            # Handle keyboard input
            if show_window:
                key = cv2.waitKey(1) & 0xFF
                if key in [ord('q'), ord('Q'), 27]: # Q or ESC
                    break
                elif key in [ord('s'), ord('S')]: # Screenshot
                    screenshot_img = annotated_frame if not is_paused else frame
                    if screenshot_img is not None:
                        output_mgr.save_screenshot(screenshot_img)
                elif key == 32: # SPACE
                    is_paused = not is_paused
                    state = "Paused" if is_paused else "Resumed"
                    logger.info(f"Playback {state}")
                elif key in [ord('b'), ord('B')]:
                    show_bbox = not show_bbox
                elif key in [ord('i'), ord('I')]:
                    show_info = not show_info

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt (Ctrl+C) detected in terminal. Exiting safely...")
    finally:
        # Cleanup
        source.release()
        output_mgr.finalize()
        if show_window:
            cv2.destroyAllWindows()

        session_duration = time.time() - start_session_time
        avg_fps = frame_id / session_duration if session_duration > 0 else 0
        
        logger.info("Session Summary:")
        logger.info(f"- Total Frames: {frame_id}")
        logger.info(f"- Total Objects Detected: {total_objects}")
        logger.info(f"- Average FPS: {avg_fps:.2f}")
        logger.info("Application exited successfully.")

if __name__ == "__main__":
    main()
