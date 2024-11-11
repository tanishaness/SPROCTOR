import cv2
import numpy as np
import logging
import time
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from .student_tracker import MultiStudentTracker
from .face_recog import FaceRecognition

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DetectionSystem:
    def __init__(self):
        self.face_recognition = FaceRecognition()
        self.student_tracker = MultiStudentTracker()
        self.active_tracking = False
        
        # Detection parameters
        self.PLOT_LENGTH = 200
        self.CHEAT_THRESH = 0.6
        self.is_running = True
        
        # Initialize tracking data for each student
        self.student_data = {}  # Dictionary to store per-student metrics
        
    def avg(self, current: float, previous: float) -> float:
        """Calculate weighted average of cheat probability"""
        if previous > 1:
            return 0.65
        if current == 0:
            if previous < 0.01:
                return 0.01
            return previous / 1.01
        if previous == 0:
            return current
        return 1 * previous + 0.1 * current

    def calculate_cheat_probability(self, student_metrics: Dict) -> float:
        """
        Calculate cheat probability based on multiple metrics
        """
        pose_data = student_metrics.get('pose_data', {})
        audio_cheat = student_metrics.get('audio_cheat', 0)
        previous_cheat = student_metrics.get('previous_cheat', 0)
        
        x_axis_cheat = int(not pose_data.get('looking_straight', True))
        y_axis_cheat = int(pose_data.get('movement_detected', False))
        
        # Complex decision tree for cheat probability
        base_probability = 0
        
        if x_axis_cheat == 0:
            if y_axis_cheat == 0:
                if audio_cheat == 0:
                    base_probability = 0
                else:
                    base_probability = 0.2
            else:
                if audio_cheat == 0:
                    base_probability = 0.2
                else:
                    base_probability = 0.4
        else:
            if y_axis_cheat == 0:
                if audio_cheat == 0:
                    base_probability = 0.1
                else:
                    base_probability = 0.4
            else:
                if audio_cheat == 0:
                    base_probability = 0.15
                else:
                    base_probability = 0.25
                    
        return self.avg(base_probability, previous_cheat)

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[Dict]]:
        """
        Process a single frame with face recognition and student tracking
        """
        if frame is None:
            return None, []
            
        try:
            # Perform face recognition
            recognized_frame = self.face_recognition.recognize_faces(frame)
            
            # Perform student tracking
            tracked_frame, new_student_data = self.student_tracker.detect_and_track_students(recognized_frame)
            
            # Update student metrics
            timestamp = time.time()
            for student in new_student_data:
                student_id = student['bbox']  # Use bbox as temporary ID
                
                if student_id not in self.student_data:
                    # Initialize new student data
                    self.student_data[student_id] = {
                        'cheat_history': [0] * self.PLOT_LENGTH,
                        'previous_cheat': 0,
                        'global_cheat': 0,
                        'audio_cheat': 0  # Placeholder for audio detection
                    }
                
                # Calculate cheat probability
                cheat_prob = self.calculate_cheat_probability({
                    'pose_data': student['pose_data'],
                    'audio_cheat': self.student_data[student_id]['audio_cheat'],
                    'previous_cheat': self.student_data[student_id]['previous_cheat']
                })
                
                # Update student metrics
                self.student_data[student_id]['previous_cheat'] = cheat_prob
                self.student_data[student_id]['cheat_history'].pop(0)
                self.student_data[student_id]['cheat_history'].append(cheat_prob)
                
                # Update global cheat flag
                if cheat_prob > self.CHEAT_THRESH:
                    self.student_data[student_id]['global_cheat'] = 1
                    logging.info(f"Cheating detected for student at {student['bbox']}")
                else:
                    self.student_data[student_id]['global_cheat'] = 0
                
                # Add metrics to student data
                student['cheat_probability'] = cheat_prob
                student['global_cheat'] = self.student_data[student_id]['global_cheat']
                student['timestamp'] = timestamp
            
            return tracked_frame, new_student_data
            
        except Exception as e:
            logging.error(f"Error in process_frame: {e}")
            return frame, []

    def start_tracking(self):
        """Enable student tracking"""
        self.active_tracking = True
        self.is_running = True

    def stop_tracking(self):
        """Disable student tracking"""
        self.active_tracking = False
        self.is_running = False
        
    def get_student_plot_data(self, student_id):
        """Get plotting data for a specific student"""
        if student_id in self.student_data:
            return (
                list(range(self.PLOT_LENGTH)),
                self.student_data[student_id]['cheat_history']
            )
        return None, None

    def cleanup(self):
        """Cleanup resources"""
        self.stop_tracking()
        plt.close('all')