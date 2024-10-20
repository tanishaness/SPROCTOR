import psutil

def adjust_processing_based_on_resources():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    if cpu_usage > 80 or memory_usage > 75:
        print("High resource usage detected, lowering frame rate...")
        return 60  # Process fewer frames (lower frame rate)
    else:
        return 30  # Normal frame rate

# Use this function to adjust the video processing loop
def process_video_dynamically(video_source):
    frame_interval = adjust_processing_based_on_resources()
    process_video_offline(video_source, frame_interval)
