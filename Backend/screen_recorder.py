from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
import datetime

def initialize_video_writer(filename, fourcc, frame_rate, frame_size):
    return cv2.VideoWriter(filename, fourcc, frame_rate, frame_size)

def capture_screen(width, height):
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

def overlay_webcam_on_screen(screen_frame, webcam_frame):
    frame_h, frame_w, _ = webcam_frame.shape
    screen_frame[0:frame_h, 0:frame_w, :] = webcam_frame[0:frame_h, 0:frame_w, :]
    return screen_frame

def main():
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    filename = f'{time_stamp}.mp4'
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    frame_rate = 20.0
    frame_size = (width, height)

    captured_video = initialize_video_writer(filename, fourcc, frame_rate, frame_size)
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            screen_frame = capture_screen(width, height)
            ret, webcam_frame = webcam.read()

            if not ret:
                print("Error: Failed to capture webcam frame.")
                break

            final_frame = overlay_webcam_on_screen(screen_frame, webcam_frame)
            cv2.imshow('Capture', final_frame)
            captured_video.write(final_frame)

            if cv2.waitKey(10) == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        webcam.release()
        captured_video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()