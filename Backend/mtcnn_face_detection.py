import cv2
from mtcnn import MTCNN

# Initialize the MTCNN face detector
detector = MTCNN()

# Initialize the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert frame to RGB (MTCNN requires RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    faces = detector.detect_faces(rgb_frame)

    # Loop over each face detected
    for face in faces:
        # Get the bounding box and keypoints
        x, y, width, height = face['box']
        keypoints = face['keypoints']

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Draw keypoints
        cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
        cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
        cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
        cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
        cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)

    # Display the resulting frame
    cv2.imshow('MTCNN Real-Time Face Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
