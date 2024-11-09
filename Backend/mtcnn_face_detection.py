import cv2
import numpy as np
from mtcnn import MTCNN
import logging
import os
from typing import Dict, List, Tuple, Optional

# Import project-specific modules
from detection import Detection
from processes import Process
from proctor_core import ProctorCore

class FaceDetector:
    """MTCNN-based face detection class for the SPROCTOR system."""
    
    def __init__(self, confidence_threshold: float = 0.9):
        """
        Initialize the MTCNN face detector.
        
        Args:
            confidence_threshold (float): Minimum confidence threshold for face detection
        """
        self.detector = MTCNN(min_face_size=20, scale_factor=0.709)
        self.confidence_threshold = confidence_threshold
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the face detector."""
        logger = logging.getLogger('SPROCTOR.FaceDetector')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def detect_faces(self, frame: np.ndarray) -> Tuple[List[Dict], np.ndarray]:
        """
        Detect faces in a frame and return detection results.
        
        Args:
            frame (np.ndarray): Input frame in BGR format
            
        Returns:
            Tuple containing list of face detections and annotated frame
        """
        try:
            # Convert BGR to RGB for MTCNN
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            faces = self.detector.detect_faces(rgb_frame)
            
            # Filter faces based on confidence
            valid_faces = [
                face for face in faces 
                if face['confidence'] >= self.confidence_threshold
            ]
            
            # Annotate frame
            annotated_frame = self._annotate_frame(frame.copy(), valid_faces)
            
            self.logger.debug(f"Detected {len(valid_faces)} faces")
            return valid_faces, annotated_frame
            
        except Exception as e:
            self.logger.error(f"Error in face detection: {str(e)}")
            return [], frame
    
    def _annotate_frame(self, frame: np.ndarray, faces: List[Dict]) -> np.ndarray:
        """
        Draw detection results on frame.
        
        Args:
            frame (np.ndarray): Input frame
            faces (List[Dict]): List of detected faces
            
        Returns:
            np.ndarray: Annotated frame
        """
        for face in faces:
            # Get detection data
            box = face['box']
            keypoints = face['keypoints']
            confidence = face['confidence']
            
            # Draw bounding box
            x, y, width, height = box
            cv2.rectangle(
                frame, 
                (x, y), 
                (x + width, y + height),
                (0, 255, 0), 
                2
            )
            
            # Draw confidence
            cv2.putText(
                frame,
                f"Conf: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            
            # Draw facial keypoints
            for point in keypoints.values():
                cv2.circle(frame, point, 2, (0, 155, 255), 2)
                
        return frame

class MTCNNDetectionProcess(Process):
    """Process class for running MTCNN face detection."""
    
    def __init__(self, core: ProctorCore):
        """
        Initialize the MTCNN detection process.
        
        Args:
            core (ProctorCore): Reference to the main proctor core
        """
        super().__init__()
        self.core = core
        self.face_detector = FaceDetector()
        self.logger = logging.getLogger('SPROCTOR.MTCNNProcess')
        
    def process_frame(self, frame: np.ndarray) -> Detection:
        """
        Process a single frame and return detection results.
        
        Args:
            frame (np.ndarray): Input frame
            
        Returns:
            Detection: Detection results including face locations and confidence
        """
        faces, annotated_frame = self.face_detector.detect_faces(frame)
        
        # Create detection object
        detection = Detection()
        detection.frame = annotated_frame
        detection.faces = faces
        detection.timestamp = self.core.get_timestamp()
        
        return detection
    
    def run(self):
        """Main process loop."""
        self.logger.info("Starting MTCNN detection process")
        
        try:
            cap = cv2.VideoCapture(0)
            
            while not self.stop_flag.is_set():
                ret, frame = cap.read()
                if not ret:
                    self.logger.error("Failed to grab frame")
                    continue
                    
                # Process frame
                detection = self.process_frame(frame)
                
                # Send detection to core
                self.core.process_detection(detection)
                
                # Check for quit command
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in MTCNN process: {str(e)}")
            
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.logger.info("MTCNN detection process stopped")

if __name__ == "__main__":
    # Simple test code
    detector = FaceDetector()
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        faces, annotated_frame = detector.detect_faces(frame)
        cv2.imshow('MTCNN Face Detection', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()