import time
import audio
import head_pose
import matplotlib.pyplot as plt
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PLOT_LENGTH = 200

# Placeholders 
GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.6
XDATA = list(range(200))
YDATA = [0] * 200

# Global flag to check if window is open
is_running = True

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return 1 * previous + 0.1 * current

def process():
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT, CHEAT_THRESH

    try:
        if GLOBAL_CHEAT == 0:
            if head_pose.X_AXIS_CHEAT == 0:
                if head_pose.Y_AXIS_CHEAT == 0:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
                else:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
            else:
                if head_pose.Y_AXIS_CHEAT == 0:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.4, PERCENTAGE_CHEAT)
                else:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.25, PERCENTAGE_CHEAT)
        else:
            if head_pose.X_AXIS_CHEAT == 0:
                if head_pose.Y_AXIS_CHEAT == 0:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
                else:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
            else:
                if head_pose.Y_AXIS_CHEAT == 0:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.6, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)
                else:
                    if audio.AUDIO_CHEAT == 0:
                        PERCENTAGE_CHEAT = avg(0.5, PERCENTAGE_CHEAT)
                    else:
                        PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)

        if PERCENTAGE_CHEAT > CHEAT_THRESH:
            GLOBAL_CHEAT = 1
            print("CHEATING")
        else:
            GLOBAL_CHEAT = 0
        print("Cheat percent: ", PERCENTAGE_CHEAT, GLOBAL_CHEAT)
    
    except Exception as e:
        logging.error(f"Error in process: {e}")
        print("An error occurred during processing. Please check the logs.")

def on_close(event):
    global is_running
    is_running = False
    # Set flag to False when the window is closed

def run_detection():
    global XDATA, YDATA, is_running

    try:
        fig, axes = plt.subplots()

        axes.set_xlim(0, 200)
        axes.set_ylim(0, 1)
        line, = axes.plot(XDATA, YDATA, 'r-')
        plt.title("Suspicious Behaviour Detection")
        plt.xlabel("Time")
        plt.ylabel("Cheat Probability")

        # Connect the close event to the callback
        fig.canvas.mpl_connect('close_event', on_close)

        while is_running:
            YDATA.pop(0)
            YDATA.append(PERCENTAGE_CHEAT)
            line.set_xdata(XDATA)
            line.set_ydata(YDATA)
            plt.draw()
            plt.pause(1e-17)
            process()
            time.sleep(1 / 5)

        plt.close(fig)
    
    except Exception as e:
        logging.error(f"Error in run_detection: {e}")
        print("An error occurred while running the detection. Please check the logs.")

if __name__ == "__main__":
    try:
        run_detection()
    except KeyboardInterrupt:
        logging.info("Detection interrupted by user.")
        print("Terminated detection.")
