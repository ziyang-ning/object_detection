import matplotlib.pyplot as plt
import numpy as np

def process_file(file_path):
    """Parse the text file to extract function run times."""
    function_run_times = []

    # Open the file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("function run time:,"):
                # Extract the function run time after the comma and convert it to an integer
                run_time = int(line.split(',')[1].strip())
                function_run_times.append(run_time)
    return function_run_times

def plot_run_times(file_list, num_bins=30):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Predefined colors for the plots
    color_index = 0

    # Determine the global min and max across all files to ensure consistent bins
    all_run_times = []
    for file_path in file_list:
        all_run_times.extend(process_file(file_path))
    global_min = min(all_run_times)
    global_max = max(all_run_times)
    
    # Define the common bin edges based on the global min and max
    bins = np.linspace(global_min, global_max, num_bins + 1)
    
    plt.figure(figsize=(10, 6))  # Create a new figure for the combined plots
    
    for file_path in file_list:
        # Process file and get stats
        run_times_array = np.array(process_file(file_path))
        
        # Create histogram of function run times with consistent bins
        plt.hist(run_times_array, bins=bins, edgecolor='black', alpha=0.5, label=file_path, color=colors[color_index % len(colors)])
        
        # Increment color_index for next file
        color_index += 1

    # Add title and labels
    plt.title('Memory Access of 5670 Pixels Histogram')
    plt.xlabel('Function Run Time (us)')
    plt.ylabel('Frequency')
    
    # Add legend
    plt.legend()
    
    # Show the plot
    plt.show()

# List of file paths to plot
files_to_plot = ['data/skip_access_timing.txt', 'data/inorder_access_timing.txt', 'data/random_access_timing.txt']
plot_run_times(files_to_plot)