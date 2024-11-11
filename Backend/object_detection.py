import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import json
import logging
from datetime import datetime

class SPROCTORObjectDetector:
    """Object detection module for SPROCTOR exam monitoring system"""
    
    SUSPICIOUS_OBJECTS = {
        'cell phone': 0.7,
        'book': 0.6,
        'laptop': 0.8,
        'tablet': 0.7,
        'person': 0.8,  # For detecting additional persons in frame
    }
    
    def __init__(self, model_url="https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"):
        self.logger = self._setup_logger()
        self.model = self._load_model(model_url)
        self.class_names = self._load_class_names()
        
    def _setup_logger(self):
        logger = logging.getLogger('SPROCTOR_ObjectDetection')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('sproctor_detection.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _load_model(self, model_url):
        try:
            model = hub.load(model_url)
            self.logger.info("Model loaded successfully")
            return model
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise
            
    def _load_class_names(self, filename="class_names.json"):
        try:
            with open(filename) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading class names: {str(e)}")
            raise
            
    def process_frame(self, frame):
        """
        Process a single frame and return suspicious object detections
        Returns: (processed_frame, suspicious_objects_detected)
        """
        # Prepare image
        h, w = frame.shape[:2]
        scale_factor = 320 / max(h, w)
        frame_resized = cv2.resize(frame, (int(w * scale_factor), int(h * scale_factor)))
        input_tensor = tf.convert_to_tensor(frame_resized)[tf.newaxis, ...]
        
        # Detect objects
        detections = self.model(input_tensor)
        
        # Extract detection data
        boxes = detections["detection_boxes"].numpy()[0]
        class_ids = detections["detection_classes"].numpy()[0].astype(int)
        scores = detections["detection_scores"].numpy()[0]
        
        # Process detections and draw boxes
        suspicious_objects = []
        processed_frame = frame.copy()
        
        for i, score in enumerate(scores):
            class_name = self.class_names.get(str(class_ids[i]), "Unknown")
            
            # Check if detected object is suspicious and meets threshold
            if class_name.lower() in self.SUSPICIOUS_OBJECTS and score >= self.SUSPICIOUS_OBJECTS[class_name.lower()]:
                box = boxes[i]
                ymin, xmin, ymax, xmax = [int(val * dim) for val, dim in zip(box, [h, w, h, w])]
                
                # Draw red box for suspicious objects
                cv2.rectangle(processed_frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
                label = f"SUSPICIOUS: {class_name} ({score:.2f})"
                cv2.putText(processed_frame, label, (xmin, ymin - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                suspicious_objects.append({
                    'type': class_name,
                    'confidence': float(score),
                    'timestamp': datetime.now().isoformat(),
                    'bbox': [xmin, ymin, xmax, ymax]
                })
                
                self.logger.warning(f"Suspicious object detected: {class_name} with confidence {score:.2f}")
        
        return processed_frame, suspicious_objects
    
    def calculate_suspicion_score(self, suspicious_objects):
        """
        Calculate a suspicion score based on detected objects
        Returns: float between 0 and 1
        """
        if not suspicious_objects:
            return 0.0
            
        total_score = 0
        for obj in suspicious_objects:
            base_weight = self.SUSPICIOUS_OBJECTS.get(obj['type'].lower(), 0.5)
            confidence_factor = obj['confidence']
            total_score += base_weight * confidence_factor
            
        # Normalize score between 0 and 1
        return min(1.0, total_score / len(suspicious_objects))
    
    def analyze_exam_session(self, video_path):
        """
        Analyze a recorded exam session video
        Returns: dict with analysis results
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.logger.error(f"Error opening video file: {video_path}")
            return None
            
        session_data = {
            'suspicious_events': [],
            'overall_suspicion_score': 0.0,
            'timestamp': datetime.now().isoformat()
        }
        
        frame_count = 0
        suspicious_frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, suspicious_objects = self.process_frame(frame)
            
            if suspicious_objects:
                suspicious_frame_count += 1
                session_data['suspicious_events'].extend(suspicious_objects)
            
            frame_count += 1
            
        cap.release()
        
        # Calculate overall session statistics
        if frame_count > 0:
            session_data['overall_suspicion_score'] = suspicious_frame_count / frame_count
            session_data['total_frames'] = frame_count
            session_data['suspicious_frames'] = suspicious_frame_count
            
        self.logger.info(f"Session analysis completed. Overall suspicion score: {session_data['overall_suspicion_score']:.2f}")
        
        return session_data

def main():
    detector = SPROCTORObjectDetector()
    
    # Example usage for live video feed
    cap = cv2.VideoCapture(0)  # Use camera index or video file path
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        processed_frame, suspicious_objects = detector.process_frame(frame)
        suspicion_score = detector.calculate_suspicion_score(suspicious_objects)
        
        # Display suspicion score on frame
        cv2.putText(processed_frame, f"Suspicion Score: {suspicion_score:.2f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('SPROCTOR Monitor', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()