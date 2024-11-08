import threading as th
import logging
import os
from typing import Dict, List
import queue
from .proctor_core import ProctorCore

class ProctorManager:
    def __init__(self):
        self.result_queue = queue.Queue()
        self.proctor = ProctorCore()
        self.is_running = False
        self.threads: List[th.Thread] = []
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('ProctorManager')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _monitoring_worker(self):
        """Worker function for continuous monitoring"""
        while self.is_running:
            try:
                results = self.proctor.start_monitoring()
                self.result_queue.put(results)
            except Exception as e:
                self.logger.error(f"Error in monitoring worker: {str(e)}")
                break
    
    def _analysis_worker(self):
        """Worker function for analyzing results"""
        while self.is_running:
            try:
                results = self.result_queue.get(timeout=1)
                if results:
                    analysis = self.proctor.analyze_behavior(results)
                    self.proctor.save_results(analysis)
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in analysis worker: {str(e)}")
                break
    
    def start(self):
        """Start the proctoring system"""
        try:
            self.is_running = True
            
            # Create worker threads
            monitoring_thread = th.Thread(target=self._monitoring_worker)
            analysis_thread = th.Thread(target=self._analysis_worker)
            
            # Start threads
            self.threads = [monitoring_thread, analysis_thread]
            for thread in self.threads:
                thread.start()
            
            self.logger.info("Proctoring system started successfully")
            
        except Exception as e:
            self.logger.error(f"Error starting proctoring system: {str(e)}")
            self.stop()
    
    def stop(self):
        """Stop the proctoring system"""
        self.is_running = False
        
        # Wait for threads to complete
        for thread in self.threads:
            thread.join()
        
        # Cleanup resources
        self.proctor.cleanup()
        self.logger.info("Proctoring system stopped")

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize and start the proctoring system
        manager = ProctorManager()
        manager.start()
        
        # Keep running until interrupted
        while True:
            pass
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        if 'manager' in locals():
            manager.stop()
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()

