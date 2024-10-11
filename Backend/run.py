import head_pose
import detection
import threading as th

def run_threads():
    try:
        # Create threads for each target function
        head_pose_thread = th.Thread(target=head_pose.pose)
        # audio_thread = th.Thread(target=audio.sound)  # Uncomment if audio module is needed
        detection_thread = th.Thread(target=detection.run_detection)

        # Start the threads
        head_pose_thread.start()
        # audio_thread.start()  # Uncomment to start audio thread
        detection_thread.start()

        # Wait for the threads to complete
        head_pose_thread.join()
        # audio_thread.join()  # Uncomment to wait for audio thread
        detection_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("All threads have been joined.")

if __name__ == "__main__":
    run_threads()
