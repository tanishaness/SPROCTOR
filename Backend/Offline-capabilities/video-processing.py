import cv2

def process_video_offline(video_source, frame_interval=30):
    cap = cv2.VideoCapture(video_source)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame
        if frame_count % frame_interval == 0:
            # Apply cheat detection algorithms here
            detect_cheating(frame)

        frame_count += 1
        cv2.imshow('Exam Monitoring', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Sample function to simulate cheat detection
def detect_cheating(frame):
    # Perform facial recognition or gesture analysis here
    print("Analyzing frame for cheating behavior...")
