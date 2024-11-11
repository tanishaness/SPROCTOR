import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Tuple

class MultiStudentTracker:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.7
        )
        self.suspicious_behaviors = {
            'looking_away': 0,
            'rapid_movement': 0,
            'out_of_frame': 0
        }
        
    def detect_and_track_students(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict]]:
        """
        Detect and track multiple students in the frame
        Returns annotated frame and list of student tracking data
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        student_data = []
        
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Track head pose and movement
                pose_data = self.analyze_head_pose(frame[y:y+height, x:x+width])
                
                # Calculate suspicion metrics
                suspicion_score = self.calculate_suspicion_score(pose_data)
                
                student_info = {
                    'bbox': (x, y, width, height),
                    'pose_data': pose_data,
                    'suspicion_score': suspicion_score,
                    'timestamp': cv2.getTickCount() / cv2.getTickFrequency()
                }
                student_data.append(student_info)
                
                # Draw bounding box and suspicion score
                color = self.get_alert_color(suspicion_score)
                cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                cv2.putText(frame, f"Score: {suspicion_score:.2f}", 
                           (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, color, 2)
                
        return frame, student_data
    
    def analyze_head_pose(self, face_region: np.ndarray) -> Dict:
        """
        Analyze head pose and movement patterns
        """
        return {
            'looking_straight': True,
            'movement_detected': False
        }
    
    def calculate_suspicion_score(self, pose_data: Dict) -> float:
        """
        Calculate suspicion score based on pose analysis
        """
        score = 0.0
        if not pose_data['looking_straight']:
            score += 0.3
        if pose_data['movement_detected']:
            score += 0.2
        return min(score, 1.0)
    
    def get_alert_color(self, score: float) -> Tuple[int, int, int]:
        """
        Return color based on suspicion score
        """
        if score < 0.3:
            return (0, 255, 0)  # Green
        elif score < 0.7:
            return (0, 255, 255)  # Yellow
        return (0, 0, 255)  # Red