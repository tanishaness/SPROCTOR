import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Tuple
import logging
import os

# Local imports
from .detection import run_detection
from .head_pose import pose
from .object_detection import detect_objects
from .audio import process_audio
from .screen_recorder import capture_screen
from proctor_api import proctor_api

app.register_blueprint(proctor_api, url_prefix='/api')

class ProctorCore:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_pose = mp.solutions.pose
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.7)
        self.pose_detection = self.mp_pose.Pose(min_detection_confidence=0.7)
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure logging for the proctoring system"""
        logger = logging.getLogger('ProctorCore')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def start_monitoring(self):
        """Initialize and start all monitoring components"""
        try:
            # Start detection systems
            detection_result = run_detection()
            pose_result = pose()
            screen_capture = capture_screen()
            
            # Process and combine results
            combined_results = self._process_results(
                detection_result,
                pose_result,
                screen_capture
            )
            
            return combined_results
            
        except Exception as e:
            self.logger.error(f"Error in monitoring: {str(e)}")
            raise
    
    def _process_results(self, detection_data, pose_data, screen_data) -> Dict:
        """Process and combine results from different detection systems"""
        results = {
            'timestamp': np.datetime64('now'),
            'detection': detection_data,
            'pose': pose_data,
            'screen': screen_data,
            'suspicious_level': 0.0
        }
        
        # Calculate suspicious level based on combined factors
        suspicious_factors = [
            detection_data.get('suspicious_score', 0),
            pose_data.get('deviation_score', 0),
            screen_data.get('activity_score', 0)
        ]
        
        results['suspicious_level'] = np.mean([x for x in suspicious_factors if x is not None])
        
        return results
    
    def save_results(self, results: Dict, output_path: str = None):
        """Save monitoring results to specified location"""
        if output_path is None:
            output_path = os.path.join(
                os.path.dirname(__file__), 
                'Dataset', 
                f'proctor_results_{np.datetime64("now")}.json'
            )
            
        try:
            import json
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=4, default=str)
            self.logger.info(f"Results saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
    
    def analyze_behavior(self, results: Dict) -> Dict:
        """Analyze monitored behavior and generate insights"""
        analysis = {
            'timestamp': np.datetime64('now'),
            'overall_score': results.get('suspicious_level', 0),
            'warnings': [],
            'recommendations': []
        }
        
        # Generate warnings based on thresholds
        if results.get('pose', {}).get('deviation_score', 0) > 0.7:
            analysis['warnings'].append('Significant head movement detected')
            
        if results.get('detection', {}).get('suspicious_score', 0) > 0.7:
            analysis['warnings'].append('Suspicious objects detected')
            
        if results.get('screen', {}).get('activity_score', 0) > 0.7:
            analysis['warnings'].append('Unusual screen activity detected')
        
        return analysis
    
    def cleanup(self):
        """Cleanup resources and close connections"""
        try:
            cv2.destroyAllWindows()
            self.logger.info("Cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")