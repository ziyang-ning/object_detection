import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image

image_shape = (240, 240)  # Image dimensions (height, width)
threshold = 210  # Define your threshold

# defalut x y = 0, 0
x_median_final = 0
y_median_final = 0
prev_diameter = 0
x_termination = image_shape[1]

##--- Helper functions, for plotting only ---
def plot_buffer(buffvec, image_shape):
    image_data = np.empty((image_shape[0], image_shape[1]), dtype=np.uint8)
    for i in range(len(buffvec)):
            # Convert the string data to uint8
            pixel_value = int(buffvec[i])
            # Calculate the x, y coordinates
            y = i // image_shape[1]
            x = i % image_shape[1]
            # print(y,x)
            # Place the pixel at the correct position
            image_data[y, x] = pixel_value
    # Plot the image in grayscale
    plt.imshow(image_data, cmap='gray')
    plt.axis('off')  # Hide the axes
    plt.show()

def convert_jpg_to_matrix(filename):
    # Open the image file using PIL
    with Image.open(filename) as img:
        # Convert the image to RGB (if not already in this mode)
        gray_img = img.convert()
        # Convert the image to a NumPy array
        matrix = np.array(gray_img)
        return matrix


def image_to_1d_array(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to grayscale if it's not already
        grayscale_img = img.convert('L')
        
        # Convert the image data to a numpy array
        np_array = np.array(grayscale_img)
        
        # Flatten the 2D array to 1D
        flat_np_array = np_array.flatten()

    return flat_np_array


def plot_image_with_median_circle(buff_vec, image_shape, median_x, median_y):
    # Reshape buff_vec to 2D image for plotting
    image_data = buff_vec.reshape(image_shape)
    fig, ax = plt.subplots()
    # Plot the grayscale image
    ax.imshow(image_data, cmap='gray')
    # Add a red circle at the median coordinates
    circle = Circle((median_x, median_y), 2, color='red', fill=False)
    ax.add_patch(circle)
    plt.axis('off')  # Hide axes
    plt.show()


# -- main function
def fam2_p2(gray_buff, image_shape, threshold):
    global x_median_final, y_median_final, prev_diameter, x_termination
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    arr_pixvisited = [0] * image_shape[0]*image_shape[1]     # purely for visualization
    numpixvisited = 0

    detected = 0 #make this a bool in C++
    blob_start_index = -1  #the left most starting index of the first blob detected

    num_conseq_black_rows = 0
    last_row_black = 0      #Let this be a bool in C++ implementation

    # for j in range(image_shape[0]):
    j = 0
    if (x_median_final != 0 and y_median_final != 0):
        if (y_median_final - 2 * prev_diameter > 0):
            j = y_median_final - 2 * prev_diameter
            pixcount = pixcount + j * image_shape[1]

    while( j < image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0

        if(blob_start_index != -1 and blob_start_index - 20 > 0):
            i = blob_start_index - 20
            pixcount = pixcount + i
        elif(x_median_final != 0 and y_median_final != 0):
            # if(x_median_final - 2 * prev_diameter > 0):
            i = x_median_final - 2 * prev_diameter
            i = max(0, x_median_final - 2 * prev_diameter)
            pixcount = pixcount + i
            x_termination = min(image_shape[1], x_median_final + 2 * prev_diameter)
        else:
            i = 0
            x_termination = image_shape[1]

        while (i < image_shape[1] and pixcount < (image_shape[0] *image_shape[1])):
            if(i > x_termination):
                pixcount = pixcount + image_shape[1] - i
                i = i + image_shape[1] #automatically moves to the next row

            elif(gray_buff[pixcount] <= threshold or gray_buff[pixcount+1] <= threshold or gray_buff[pixcount+2] <= threshold):
                if(i+10 < image_shape[1]):

                    #for visualization, yeah shitty code i know
                    if(gray_buff[pixcount] <= threshold):
                        numpixvisited = numpixvisited + 1
                        arr_pixvisited[pixcount] = 255
                    elif(gray_buff[pixcount+1] <= threshold):
                        numpixvisited = numpixvisited + 2
                        arr_pixvisited[pixcount] = 255
                        arr_pixvisited[pixcount+1] = 255
                    elif(gray_buff[pixcount+2] <= threshold):
                        numpixvisited = numpixvisited + 3
                        arr_pixvisited[pixcount] = 255
                        arr_pixvisited[pixcount+1] = 255
                        arr_pixvisited[pixcount+2] = 255

                    i = i + 10
                    pixcount = pixcount + 10
                    

                else:
                    #for visualization, yeah shitty code i know
                    if(gray_buff[pixcount] <= threshold):
                        numpixvisited = numpixvisited + 1
                        arr_pixvisited[pixcount] = 255
                    elif(gray_buff[pixcount+1] <= threshold):
                        numpixvisited = numpixvisited + 2
                        arr_pixvisited[pixcount] = 255
                        arr_pixvisited[pixcount+1] = 255
                    elif(gray_buff[pixcount+2] <= threshold):
                        numpixvisited = numpixvisited + 3
                        arr_pixvisited[pixcount] = 255
                        arr_pixvisited[pixcount+1] = 255
                        arr_pixvisited[pixcount+2] = 255

                    pixcount = pixcount + image_shape[1] - i
                    i = image_shape[1]
                    numpixvisited = numpixvisited + 1
                    
            ## if 3 whites
            ##------MIGHT GO OUT OF BOUND HERE----- ACTUALLY NO, but it woun't behave as expected)
            # elif gray_buff[pixcount]>threshold and gray_buff[pixcount+1]>threshold and gray_buff[pixcount+2]>threshold:
            else:

                detected = 1

                if(i - 20 < 0):
                    blob_start_index = 0
                else:
                    blob_start_index = i

                x = i
                all_x_gt_thresh.append(x)
                all_x_gt_thresh.append(x+1)
                all_x_gt_thresh.append(x+2)
                all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 3
                i = i + 3
                pixcount = pixcount + 3
                numpixvisited = numpixvisited + 3

                #for visualization
                arr_pixvisited[pixcount-1] = arr_pixvisited[pixcount-2] =  arr_pixvisited[pixcount-3] = 255

                #searach to the right
                while(gray_buff[pixcount] > threshold and i < image_shape[1]):
                    x = i
                    all_x_gt_thresh.append(x)
                    all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 1
                    i = i + 5
                    pixcount = pixcount + 5
                    numpixvisited = numpixvisited + 1

                    #for visualization
                    arr_pixvisited[pixcount-1] = 255

                #this means that the current pixcount is already checked and it's not white
                if i != image_shape[1]:
                    i = i + 1
                    pixcount = pixcount + 1
                    numpixvisited = numpixvisited + 1

                    #for visualization
                    arr_pixvisited[pixcount-1] = 255

                ##CONTENT ADDED HERE
                #moving to the next row!
                pixcount = pixcount + image_shape[1] - i
                i = i + image_shape[1] #automatically moves to the next row

        # The median function
        # I don't think 1 pixel difference matters, so not going to do even odd, improves speed
        if(all_x_gt_thresh_real_length != 0):
            x_medians.append(all_x_gt_thresh[all_x_gt_thresh_real_length // 2 ]) # floor division
            y_vals_of_x_medians.append(j)

            last_row_black = 0
            num_conseq_black_rows = 0
        else:
            num_conseq_black_rows = num_conseq_black_rows + 1
            last_row_black = 1

        if(all_x_gt_thresh_real_length == 0 and blob_start_index != -1 and detected):
            break

        if(num_conseq_black_rows > 2 and last_row_black and j+3 < image_shape[0]):
            j = j + 2
            pixcount = pixcount + 2 * image_shape[1]
        
        j = j + 2
        pixcount = pixcount + image_shape[1]

    ###----Added condition for all black or almost all black)
    ### already implemented in arduino code
    if(len(x_medians) >= 5):
        x_median_final = x_medians[len(x_medians) // 2]
        y_median_final = y_vals_of_x_medians[len(x_medians) // 2]
        prev_diameter = y_vals_of_x_medians[-1] - y_vals_of_x_medians[0]
    else:
        x_median_final = 0
        y_median_final = 0
    #visualization
    plot_buffer(arr_pixvisited, image_shape)
    print("num pix visited: ", numpixvisited)
    print("the y_vals_of_x_medians vec: ", y_vals_of_x_medians)
    return x_median_final, y_median_final

# -- main function end --

# -- file inputs
for i in range(10):
    # filename = 'data/arduinoViz_data/animation_test_arduinoViz/ball_ard_test_240X240_' + str(i) + ".csv" 
    i = i + 1
    filename = 'data/seq_data/' + str(i) + '.jpg'
    gray_buff = image_to_1d_array(filename)
    image = convert_jpg_to_matrix(filename)
    #family 2 propsed 2
    nonlin_x, nonlin_y = fam2_p2(gray_buff, image_shape, threshold)
    plot_image_with_median_circle(gray_buff, image_shape, nonlin_x, nonlin_y)
    print("fam2_p2 x: ", nonlin_x, "fam2_p2 y: ", nonlin_y)