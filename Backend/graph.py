import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import time

# Connect to the database
db = mysql.connector.connect(
    host="localhost",  # Replace with your host, usually 'localhost'
    user="root",  # Replace with your database username
    password="ananyavastare2345",  # Replace with your database password
    database="SPROCTOR",  # Database name
)

cursor = db.cursor()

# Query to retrieve exam durations
cursor.execute("SELECT duration FROM Exams")
durations = cursor.fetchall()

# Close the cursor and database connection
cursor.close()
db.close()

# Prepare heatmap data
heatmap_data = np.zeros((10, 10))  # Create a 10x10 grid

# Populate heatmap data based on durations
for index, (duration,) in enumerate(durations):
    row = index // 10  # Determine row index
    col = index % 10  # Determine column index
    if row < 10 and col < 10:  # Check bounds
        heatmap_data[row, col] = duration  # Use duration as heatmap value

# Ensure first row has different colors (values)
first_row_values = np.random.rand(10) * 10  # Random values for the first row
heatmap_data[0] = first_row_values

# Initialize the figure
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()  # Create a subplot


# Declare heatmap_data as global to modify it within the function
def update_heatmap():
    global heatmap_data  # Declare as global variable
    # Lighten the heatmap data by adding random small changes
    heatmap_data[1:] += np.random.uniform(
        0, 1, size=heatmap_data[1:].shape
    )  # Random small increments
    heatmap_data = np.clip(
        heatmap_data, 0, np.max(heatmap_data)
    )  # Keep values within bounds
    heatmap.set_data(heatmap_data)  # Update heatmap data


# Create the heatmap
heatmap = ax.imshow(
    heatmap_data,
    cmap="YlOrRd",
    interpolation="nearest",
    vmin=0,
    vmax=np.max(heatmap_data),
)
plt.colorbar(heatmap)  # Add a colorbar to indicate scale
plt.title("Heatmap of Exam Durations")

# Loop to update heatmap every 5 seconds
for _ in range(10):  # Run the loop 10 times
    update_heatmap()  # Update the heatmap
    plt.draw()  # Redraw the updated heatmap
    plt.pause(1)  # Pause for 5 seconds

# Save the figure
plt.savefig(f"heatmap_{time.strftime('%Y%m%d_%H%M%S')}.png")  # Save with timestamp

# Keep the plot window open at the end
plt.ioff()  # Turn off interactive mode
plt.show()
