import pyaudio
import os
import struct
import numpy as np
# import matplotlib.pyplot as plt
# import time
# from tkinter import TclError

# use this backend to display in separate Tk window
# %matplotlib tk

# constants
CHUNK = 64 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
# fig, ax = plt.subplots(1, figsize=(15, 7))

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)
# data = stream.read(CHUNK)
# data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
# for i in data_int:
#     print(i)


while True:
    data = stream.read(CHUNK)
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    print(sum(data_int)/len(data_int))
