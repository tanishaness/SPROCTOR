import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import time

# Connect to the database
db = mysql.connector.connect(
    host="localhost",  # Your database host
    user="root",  # Your database username
    password="ananyavastare2345",  # Your database password
    database="SPROCTOR",  # Your database name
)

cursor = db.cursor()

# Query to retrieve look_up, look_down, look_left, and look_right values from HeadMovements
cursor.execute("SELECT look_up, look_down, look_left, look_right FROM HeadMovements")
head_movement_values = cursor.fetchall()  # Retrieve all values

# Close the cursor and database connection
cursor.close()
db.close()

# Prepare heatmap data
heatmap_data = np.zeros((10, 10, 4))  # Create a 10x10 grid for RGBA channels

# Populate heatmap data based on head movement values
for index, (look_up, look_down, look_left, look_right) in enumerate(
    head_movement_values
):
    row = index // 10  # Determine row index
    col = index % 10  # Determine column index
    if row < 10 and col < 10:  # Check bounds
        # Assign values to different channels
        heatmap_data[row, col] = [look_up, look_down, look_left, look_right]

# Normalize the heatmap data to the range [0, 1]
heatmap_data_normalized = heatmap_data / np.max(heatmap_data)

# Create the combined heatmap by averaging the channels
combined_heatmap = np.mean(
    heatmap_data_normalized, axis=2
)  # Average across the channels

# Initialize the figure
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()  # Create a subplot

# Create the heatmap
heatmap = ax.imshow(
    combined_heatmap,
    cmap="YlOrRd",  # Choose a color map
    interpolation="nearest",
    vmin=0,
    vmax=1,  # Set the range for color normalization
)
plt.colorbar(heatmap)  # Add a colorbar to indicate scale
plt.title("Combined Heatmap of Look Directions")

# Add labels for each direction without overlap
for i, direction in enumerate(["Look Up", "Look Down", "Look Left", "Look Right"]):
    ax.text(
        0.5,
        -0.15 - (i * 0.05),  # Adjust this value to position the labels appropriately
        direction,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=10,
        color="black",
        fontweight="bold",
    )

# Loop to update heatmap every second
for _ in range(10):  # Run the loop 10 times
    # Lightly modify the heatmap data for demonstration (this simulates transition)
    heatmap_data_normalized += np.random.uniform(0, 0.1, heatmap_data_normalized.shape)
    heatmap_data_normalized = np.clip(
        heatmap_data_normalized, 0, 1
    )  # Keep values within [0, 1]

    # Create a new combined heatmap by averaging the updated data
    combined_heatmap = np.mean(
        heatmap_data_normalized, axis=2
    )  # Average across the channels

    # Update the heatmap
    heatmap.set_array(combined_heatmap)  # Update heatmap data
    plt.draw()  # Redraw the heatmap
    plt.pause(1)  # Pause for 1 second

# Save the figure
plt.savefig(
    f"heatmap_combined_{time.strftime('%Y%m%d_%H%M%S')}.png"
)  # Save with timestamp

# Keep the plot window open at the end
plt.ioff()  # Turn off interactive mode
plt.show()
