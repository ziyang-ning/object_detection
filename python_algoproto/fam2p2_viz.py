import csv
import numpy as np
from PIL import Image

# Define the image size
width, height = 240, 240

# Initialize the image array with zeros (black pixels)
image_array = np.zeros((height, width), dtype=np.uint8)

# Path to the CSV file with coordinates
csv_file_path = 'data/newdata.csv'  # Change to your CSV file path

# Read the CSV file using the csv module
with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        # Convert string coordinates to integers and get the column and row
        # Assume each row of the CSV has two columns: first is 'col' and second is 'row'
        col, row = map(int, row)
        # Ensure the coordinates are within the image bounds
        if 0 <= col < width and 0 <= row < height:
            image_array[row, col] = 255  # Set the pixel to white

# Create the image from the array
image = Image.fromarray(image_array)

# Save or display the image
# image.save('output_image.png')  # Save the image to a file
image.show()  # This would display the image if you have a GUI environment