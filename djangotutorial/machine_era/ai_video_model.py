import cv2
import os
import numpy as np
from collections import Counter
from ultralytics import YOLO

MAX_FRAMES_TO_ANALYZE = 30 
FRAME_SKIP = 10 

_yolo_model = None

def get_yolo_model():
    """Завантажує модель YOLOv8-nano або повертає її з кешу."""
    global _yolo_model
    if _yolo_model is None:
        print("--- [AI INIT] Loading YOLOv8n model (Object Detection)... ---")
        # Завантажуємо попередньо навчену на COCO модель YOLOv8 nano
        _yolo_model = YOLO('yolov8n.pt') 
        print("--- [AI INIT] YOLOv8n model loaded. ---")
    return _yolo_model


def analyze_video(video_path):
    if not os.path.exists(video_path):
        return "CRITICAL.ERROR: File not found."
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "CRITICAL.ERROR: Could not open video file."

    # 1. Завантаження моделі YOLO
    try:
        yolo_model = get_yolo_model()
    except Exception as e:
        cap.release()
        return f"CRITICAL.ERROR: YOLO Model init failed: {e}"
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Список для збору ВСІХ виявлених класів
    detected_classes = []
    frames_processed = 0
    
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        
        if i % FRAME_SKIP == 0 and frames_processed < MAX_FRAMES_TO_ANALYZE:
            frames_processed += 1
            
            # 2. Обробка кадру за допомогою YOLO
            # Запускаємо передбачення. source=frame. conf=0.5 (мінімальна впевненість 50%)
            results = yolo_model(frame, verbose=False, conf=0.5, classes=None, imgsz=640)
            
            # 3. Збір результатів
            for result in results:
                # result.boxes.cls - тензор виявлених класів
                for cls_tensor in result.boxes.cls:
                    class_id = int(cls_tensor.item())
                    # result.names - словник імен класів (від 0 до 79)
                    class_name = result.names[class_id] 
                    detected_classes.append(class_name)
        
        if frames_processed >= MAX_FRAMES_TO_ANALYZE:
            break
        
    cap.release()
    
    # 4. Узагальнення результатів
    if not detected_classes:
        return f"SUCCESS: Analyzed {frames_processed} key frames. No dominant objects detected (Conf < 50%). Total Frames: {frame_count}. FPS: {fps:.2f}."

    # Знаходимо ТОП-3 найпоширеніших об'єкти
    counts = Counter(detected_classes)
    most_common = counts.most_common(3)
    
    dominant_object = most_common[0][0]
    top_3_summary = ', '.join([f'{name} ({count})' for name, count in most_common])
    
    return (
        f"SUCCESS: Analyzed {frames_processed} key frames. "
        f"Dominant Object: '{dominant_object}'. "
        f"Top 3 Detections: {top_3_summary}."
    )