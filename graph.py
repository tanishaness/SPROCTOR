import matplotlib.pyplot as plt
import time

xdata = []
ydata = []

plt.show()

axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(0, 1)
line, = axes.plot(xdata, ydata, 'r-')

def update_graph(x_cheat, y_cheat):
    xdata.append(len(xdata))
    ydata.append(y_cheat)  # Use Y_AXIS_CHEAT for the y-value

    # Keep the graph length fixed at 100 points
    if len(xdata) > 100:
        xdata.pop(0)
        ydata.pop(0)

    line.set_xdata(xdata)
    line.set_ydata(ydata)
    plt.draw()
    plt.pause(1e-17)

# Add this if you don't want the window to disappear at the end
plt.show()

# In your pose function, call update_graph when cheating behavior is detected
def pose():
    global X_AXIS_CHEAT, Y_AXIS_CHEAT

    # ... (your existing code)

    if Y_AXIS_CHEAT == 1:
        update_graph(X_AXIS_CHEAT, Y_AXIS_CHEAT)

    # ... (rest of your pose function)

if __name__ == "__main__":
    t1 = th.Thread(target=pose)

    t1.start()

    t1.join()
