import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize the figure
plt.figure()

# Set up the axes
plt.axis("off")  # Turn off the axis for a cleaner look

# Create an empty grid for the heatmap
heatmap_data = np.zeros((10, 10))  # 10x10 grid

# Show the plot window
plt.ion()  # Turn on interactive mode
plt.show()

# Loop to simulate data for the heatmap
for i in range(100):
    # Randomly generate data (for example purposes)
    data = np.random.rand(10, 10)  # Random values between 0 and 1 for a 10x10 grid
    heatmap_data += data  # Accumulate data for the heatmap

    # Clear the axes and plot the heatmap
    plt.clf()  # Clear the current figure
    heatmap = plt.imshow(
        heatmap_data, cmap="hot", interpolation="nearest", vmin=0, vmax=100
    )  # Create heatmap
    plt.colorbar(heatmap)  # Add a colorbar to indicate scale
    plt.title("Dynamic Heatmap of Random Values")

    # Update the plot
    plt.draw()
    plt.pause(0.5)  # Pause to see the update

# Keep the plot window open at the end
plt.ioff()  # Turn off interactive mode
plt.show()
