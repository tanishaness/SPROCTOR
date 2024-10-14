import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import time

# Function to connect to the database and fetch data
def fetch_head_movement_data():
    try:
        # Connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ananyavastare2345",
            database="SPROCTOR"
        )
        cursor = db.cursor()
        
        # Query to retrieve look_up, look_down, look_left, and look_right values from HeadMovements
        cursor.execute("SELECT look_up, look_down, look_left, look_right FROM HeadMovements")
        head_movement_values = cursor.fetchall()  # Retrieve all values

    except mysql.connector.Error as e:
        print(f"Error fetching data from MySQL: {e}")
        head_movement_values = []

    finally:
        cursor.close()
        db.close()

    return head_movement_values

# Fetch head movement data
head_movement_values = fetch_head_movement_data()

# Determine grid size based on the number of records
grid_size = int(len(head_movement_values) ** 0.5) + 1  # Adjust as needed for layout
heatmap_data = np.zeros((grid_size, grid_size, 4))  # Create a grid for RGBA channels

# Populate heatmap data based on head movement values
for index, (look_up, look_down, look_left, look_right) in enumerate(head_movement_values):
    row = index // grid_size  # Determine row index
    col = index % grid_size  # Determine column index
    if row < grid_size and col < grid_size:  # Check bounds
        # Assign values to different channels
        heatmap_data[row, col] = [look_up, look_down, look_left, look_right]

# Normalize the heatmap data to the range [0, 1]
heatmap_data_normalized = heatmap_data / np.max(heatmap_data)

# Create the combined heatmap by averaging the channels
combined_heatmap = np.mean(heatmap_data_normalized, axis=2)

# Initialize the figure
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

# Create the heatmap
heatmap = ax.imshow(
    combined_heatmap,
    cmap="YlOrRd",  # Choose a color map
    interpolation="nearest",
    vmin=0,
    vmax=1,
)
plt.colorbar(heatmap)  # Add a colorbar to indicate scale
plt.title("Combined Heatmap of Look Directions")

# Add labels for each direction without overlap
directions = ["Look Up", "Look Down", "Look Left", "Look Right"]
for i, direction in enumerate(directions):
    ax.text(
        0.5,
        -0.15 - (i * 0.05),
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
    # Lightly modify the heatmap data for demonstration (simulates transition)
    heatmap_data_normalized += np.random.uniform(0, 0.1, heatmap_data_normalized.shape)
    heatmap_data_normalized = np.clip(heatmap_data_normalized, 0, 1)

    # Create a new combined heatmap by averaging the updated data
    combined_heatmap = np.mean(heatmap_data_normalized, axis=2)

    # Update the heatmap
    heatmap.set_array(combined_heatmap)
    plt.draw()
    plt.pause(1)

# Save the figure
plt.savefig(f"heatmap_combined_{time.strftime('%Y%m%d_%H%M%S')}.png")

# Keep the plot window open at the end
plt.ioff()
plt.show()
