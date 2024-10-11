import pyaudio
import struct
import numpy as np
import time

# Constants
CHUNK = 64 * 2             # Samples per frame
FORMAT = pyaudio.paInt16   # Audio format (16-bit integer)
CHANNELS = 1               # Single channel for microphone
RATE = 44100               # Samples per second

# Create pyaudio class instance
p = pyaudio.PyAudio()

# Stream object to get data from microphone
try:
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=False,  # Set to False since we're only capturing input
        frames_per_buffer=CHUNK
    )
    
    print("Recording audio... Press Ctrl+C to stop.")

    while True:
        # Read data from the stream
        data = stream.read(CHUNK)
        
        # Unpack the data into an array of integers
        data_int = struct.unpack(str(2 * CHUNK) + 'h', data)
        
        # Calculate the average amplitude
        avg_amplitude = sum(data_int) / len(data_int)
        
        # Print the average amplitude
        print(f"Average Amplitude: {avg_amplitude:.2f}")

except KeyboardInterrupt:
    print("Recording stopped by user.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Stream closed and resources released.")
