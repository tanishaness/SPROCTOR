from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

@dataclass
class Detection:
    """Class for storing detection results"""
    frame: Optional[np.ndarray] = None
    faces: List[Dict] = None
    timestamp: datetime = None
    is_cheating: bool = False
    confidence: float = 0.0
    detected_processes: List[Dict] = None
    
    def __post_init__(self):
        if self.faces is None:
            self.faces = []
        if self.detected_processes is None:
            self.detected_processes = []
            
    def add_face(self, face: Dict):
        """Add a face detection result"""
        self.faces.append(face)
        
    def get_face_count(self) -> int:
        """Return number of faces detected"""
        return len(self.faces)
        
    def get_process_count(self) -> int:
        """Return number of detected unauthorized processes"""
        return len(self.detected_processes)