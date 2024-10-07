from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
import datetime

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{time_stamp}.mp4'
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
captured_video = cv2.VideoWriter(filename, fourcc, 20.0, (width, height)) 

webcam = cv2.VideoCapture(0)

while True:
    img = ImageGrab.grab(bbox = (0, 0, width, height)) # captures screen
    img_np = np.array(img)
    img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    _, frame = webcam.read() # webcam capture
    frame_h, frame_w, _ = frame.shape
    img_final[0:frame_h, 0:frame_w, :] = frame[0:frame_h, 0:frame_w, :]  # overlay webcam on screen
    # cv2.imshow('webcam', frame)
    cv2.imshow('Capture', img_final)
    captured_video.write(img_final)
    if cv2.waitKey(10) == ord('q'):
        break
