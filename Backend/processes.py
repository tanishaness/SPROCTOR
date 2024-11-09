import threading
from abc import ABC, abstractmethod
import logging
from typing import Optional, List, Dict
import numpy as np
import wmi
import time
from detection import Detection

class Process(ABC):
    """Abstract base class for all detection processes"""
    
    def __init__(self):
        self.stop_flag = threading.Event()
        self.thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(f'SPROCTOR.{self.__class__.__name__}')
        
    @abstractmethod
    def process_frame(self, frame: np.ndarray) -> Detection:
        """Process a single frame"""
        pass
        
    @abstractmethod
    def run(self):
        """Main process loop"""
        pass
        
    def start(self):
        """Start the process thread"""
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info(f"Started {self.__class__.__name__}")
        
    def stop(self):
        """Stop the process thread"""
        self.stop_flag.set()
        if self.thread:
            self.thread.join()
        self.logger.info(f"Stopped {self.__class__.__name__}")

class ProcessMonitor:
    """Class for monitoring system processes"""
    
    NOT_ALLOWED_APPS = [
        "Discord",
        "Whatsapp",
        "Telegram",
        "Zoom",
        "Skype"
    ]
    
    def __init__(self):
        self.logger = logging.getLogger('SPROCTOR.ProcessMonitor')
        self.wmi = wmi.WMI()
        self.detected_processes: Dict[str, int] = {}
        
    def scan_processes(self) -> List[Dict[str, str]]:
        """
        Scan for not allowed processes
        Returns list of detected processes with their details
        """
        start_time = time.time()
        detected = []
        
        try:
            processes = self.wmi.Win32_Process()
            
            for process in processes:
                for app in self.NOT_ALLOWED_APPS:
                    if app.lower() in process.Name.lower():
                        process_info = {
                            'name': process.Name,
                            'pid': process.ProcessId,
                            'path': process.ExecutablePath or 'Unknown'
                        }
                        detected.append(process_info)
                        self.detected_processes[process.Name] = process.ProcessId
                        self.logger.warning(f"Detected unauthorized application: {process.Name}")
            
            execution_time = time.time() - start_time
            self.logger.info(f"Process scan completed in {execution_time:.2f} seconds")
            return detected
            
        except Exception as e:
            self.logger.error(f"Error scanning processes: {str(e)}")
            return []
            
    def is_cheating(self) -> bool:
        """Check if any unauthorized applications are running"""
        return len(self.detected_processes) > 0
        
    def get_detected_apps(self) -> List[str]:
        """Get list of currently detected unauthorized applications"""
        return list(self.detected_processes.keys())

class ProcessMonitoringProcess(Process):
    """Process class for monitoring system processes"""
    
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.monitor = ProcessMonitor()
        self.scan_interval = 5  # seconds
        
    def process_frame(self, frame: np.ndarray) -> Detection:
        """Process a single frame (not used in process monitoring)"""
        return Detection()
        
    def run(self):
        """Main monitoring loop"""
        self.logger.info("Starting process monitoring")
        
        while not self.stop_flag.is_set():
            try:
                # Scan for unauthorized processes
                detected = self.monitor.scan_processes()
                
                if detected:
                    # Create detection event
                    detection = Detection()
                    detection.timestamp = self.core.get_timestamp()
                    detection.is_cheating = True
                    detection.confidence = 0.9
                    detection.detected_processes = detected
                    
                    # Send detection to core
                    self.core.process_detection(detection)
                    
                # Wait for next scan
                time.sleep(self.scan_interval)
                
            except Exception as e:
                self.logger.error(f"Error in process monitoring: {str(e)}")
                time.sleep(1)
                
        self.logger.info("Process monitoring stopped")

def main():
    """Test function for process monitoring"""
    logging.basicConfig(level=logging.INFO)
    
    monitor = ProcessMonitor()
    print("\nScanning for unauthorized applications...")
    detected = monitor.scan_processes()
    
    if detected:
        print("\nDetected unauthorized applications:")
        print("Name                          PID")
        print("-" * 40)
        for process in detected:
            print(f"{process['name']:<30} {process['pid']}")
    else:
        print("\nNo unauthorized applications detected")

if __name__ == "__main__":
    main()