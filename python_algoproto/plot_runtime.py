import matplotlib.pyplot as plt
import numpy as np

# Parse the text file to extract function run times
function_run_times = []

# Open the file and process each line
with open('data/inord_func_timing.txt', 'r') as file:
    for line in file:
        if line.startswith("function run time:,"):
            # Extract the function run time after the comma and convert it to an integer
            run_time = int(line.split(',')[1].strip())
            function_run_times.append(run_time)

# Convert the list to a numpy array for statistical calculations
run_times_array = np.array(function_run_times)

# Calculate mean, median and standard deviation
mean_run_time = np.mean(run_times_array)
median_run_time = np.median(run_times_array)
std_dev_run_time = np.std(run_times_array)
sample_size = len(run_times_array)
print(f"Number of Samples: {sample_size}")

# Print the statistical values
print(f"Mean Function Run Time: {mean_run_time:.2f} us")
print(f"Median Function Run Time: {median_run_time:.2f} us")
print(f"Standard Deviation of Function Run Time: {std_dev_run_time:.2f} us")

# Create histogram of function run times
plt.hist(run_times_array, bins=10, edgecolor='black')
plt.title('Inorder Access (of 5670 pixels) Time Histogram')
plt.xlabel('Function Run Time (us)')
plt.ylabel('Frequency')

# Embed statistical information in the graph
textstr = f"Mean: {mean_run_time:.2f} us\nMedian: {median_run_time:.2f} us\nStd Dev: {std_dev_run_time:.2f} us\nSamples: {sample_size}"
# Place the text on the upper left of the histogram
plt.text(0.6, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.5))

# Show the plot
plt.show()