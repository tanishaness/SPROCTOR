import sounddevice as sd
import numpy as np
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Placeholders and global variables
SOUND_AMPLITUDE = 0
AUDIO_CHEAT = 0

# Sound variables
CALLBACKS_PER_SECOND = 38               # Callbacks per sec (system dependent)
SUS_FINDING_FREQUENCY = 2               # Calculates SUS *n* times every sec
SOUND_AMPLITUDE_THRESHOLD = 20          # Default amplitude threshold

# Packing *n* frames to calculate SUS
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)
AMPLITUDE_LIST = [0] * FRAMES_COUNT
SUS_COUNT = 0
count = 0

# Configure command-line argument parsing
parser = argparse.ArgumentParser(description="Configure sound detection sensitivity.")
parser.add_argument('--threshold', type=int, help="Set the amplitude threshold for sound detection.")
args = parser.parse_args()

# Prompt user for threshold if not provided via command-line
if args.threshold is not None:
    SOUND_AMPLITUDE_THRESHOLD = args.threshold
else:
    try:
        user_input = input("Enter amplitude threshold for sound detection (default is 20): ")
        if user_input.strip():
            SOUND_AMPLITUDE_THRESHOLD = int(user_input)
        else:
            logging.info("Using default amplitude threshold of 20.")
    except ValueError:
        logging.error("Invalid input. Using default amplitude threshold of 20.")
        SOUND_AMPLITUDE_THRESHOLD = 20

def print_sound(indata, outdata, frames, time, status):
    avg_amp = 0
    global SOUND_AMPLITUDE, SUS_COUNT, count, SOUND_AMPLITUDE_THRESHOLD, AUDIO_CHEAT
    
    try:
        vnorm = int(np.linalg.norm(indata) * 10)
        AMPLITUDE_LIST.append(vnorm)
        count += 1
        AMPLITUDE_LIST.pop(0)
        
        if count == FRAMES_COUNT:
            avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT
            SOUND_AMPLITUDE = avg_amp
            
            if SUS_COUNT >= 2:
                AUDIO_CHEAT = 1
                SUS_COUNT = 0
            
            if avg_amp > SOUND_AMPLITUDE_THRESHOLD:
                SUS_COUNT += 1
            else:
                SUS_COUNT = 0
                AUDIO_CHEAT = 0
            
            count = 0
    except Exception as e:
        logging.error(f"Error in print_sound: {e}")
        print("An error occurred while processing audio input. Please check the logs.")

def sound():
    try:
        with sd.Stream(callback=print_sound):
            sd.sleep(-1)
    except Exception as e:
        logging.error(f"Error in sound function: {e}")
        print("An error occurred while starting the audio stream. Please check the logs.")

def sound_analysis():
    global AMPLITUDE_LIST, FRAMES_COUNT, SOUND_AMPLITUDE
    while True:
        try:
            AMPLITUDE_LIST.append(SOUND_AMPLITUDE)
            AMPLITUDE_LIST.pop(0)

            avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT

            if avg_amp > 10:
                print("Sus...")
        except Exception as e:
            logging.error(f"Error in sound_analysis: {e}")
            print("An error occurred during sound analysis. Please check the logs.")

if __name__ == "__main__":
    try:
        sound()
    except KeyboardInterrupt:
        logging.info("Sound analysis interrupted by user.")
        print("Terminated sound analysis.")
