#proposed fast algorithm
#will take input of 240X240 image
#We first need to convert jpg to Grayscale matrix, 
#this will not be needed for C/C++ implementation
#Input of PIXFORMAT_GRAYSCALE, // 1BPP/GRAYSCALE

import csv
import numpy as np
import matplotlib.pyplot as plt
import heapq
from matplotlib.patches import Circle
from PIL import Image

## Input: filename string
## Output: RGB matrix of the image
## Use: Convert jpg file to RGB888 matrix
def convert_jpg_to_matrix(filename):
    # Open the image file using PIL
    with Image.open(filename) as img:
        # Convert the image to RGB (if not already in this mode)
        gray_img = img.convert()
        # Convert the image to a NumPy array
        matrix = np.array(gray_img)
        return matrix

# def matrix2buff(mat, image_shape):
#     buff_vec = []
#     for i in range(len(mat[0])):
#         buff_vec = 
#     return


# Function to read the CSV data into a 2D NumPy array for a grayscale image
def read_csv_to_grayscale_image(filename, image_shape):
    # Initialize an empty array to hold the image data
    image_data = np.empty((image_shape[0], image_shape[1]), dtype=np.uint8)
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            # Convert the string data to uint8
            pixel_value = int(row[0])
            # Calculate the x, y coordinates
            y = i // image_shape[1]
            x = i % image_shape[1]
            # Place the pixel at the correct position
            image_data[y, x] = pixel_value

    return image_data

def make_gray_buffer(filename, image_shape):
    buff_vec = np.zeros((image_shape[0] * image_shape[1]), dtype=np.uint8)

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for i, row in enumerate(csv_reader):
            # Convert the string data to uint8
            pixel_value = int(row[0])
            # print(pixel_value)
            # Place the pixel at the correct position
            buff_vec[i] = int(row[0])
    return buff_vec

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

def plot_bin(image, thresh):
    bin_image = np.where(image > thresh, 1, 0)
    # Plot the binary image
    plt.imshow(bin_image, cmap='gray')  # Use a grayscale colormap
    plt.axis('off')  # Hide the axes
    plt.show()


##############
## TESTS
##############

# Configuration
csv_filename = 'data/graydata/gray2_240X240.csv'  # Replace with your CSV file's path
# csv_filename = 'data/graydata/FOV_verification3.csv'  # Replace with your CSV file's path
# csv_filename = 'data/graydata/all_black.csv'  # Replace with your CSV file's path
image_shape = (240, 240)  # Image dimensions (height, width)

# Load the image from the CSV
image = read_csv_to_grayscale_image(csv_filename, image_shape)

# Plot the image in grayscale
plt.imshow(image, cmap='gray')
plt.axis('off')  # Hide the axes
plt.show()

# prepare the buffer
gray_buff = make_gray_buffer(csv_filename, image_shape)
# print(gray_buff)

# plot the buffer
plot_buffer(gray_buff, image_shape)

################
## median ##

def plot_image_with_median_circle(buff_vec, image_shape, median_x, median_y):
    # Reshape buff_vec to 2D image for plotting
    image_data = buff_vec.reshape(image_shape)
    fig, ax = plt.subplots()
    # Plot the grayscale image
    ax.imshow(image_data, cmap='gray')
    # Add a red circle at the median coordinates
    circle = Circle((median_x, median_y), 5, color='red', fill=False)
    ax.add_patch(circle)
    plt.axis('off')  # Hide axes
    plt.show()


## input gray_buff, an image_shape[0] * image_shape[i] sized 1d array values inside are 8 bit gray scale pixel
## input image_shape, defines the size of the image
## threshold, 8 bit integer 
## USE: iterate through each row of the image with gray_buff, find the median of the x cooridnate
## for each row of the image, call it x_row_median, in the end find the median of the x_row_median, and
## it's corresponding y cooridnate
def pix_median_jason(gray_buff, image_shape, threshold):
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    for j in range(image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        # all_y_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0
        for i in range(image_shape[1]):
            if gray_buff[pixcount] > threshold:
                x = i
                y = j
                all_x_gt_thresh.append(x)
                # all_y_gt_thresh.append(y)
                all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 1

            pixcount = pixcount + 1
        # The median function
        # I don't think 1 pixel difference matters, so not going to do even odd, improves speed
        #//-------NEED TO ADD CONDITION WHERE EVERYTHING IS DARK ----------------
        if(all_x_gt_thresh_real_length != 0):
            x_medians.append(all_x_gt_thresh[all_x_gt_thresh_real_length // 2 ]) # floor division
            y_vals_of_x_medians.append(j)
    
    ###----Added condition for all black or almost all black)
    ### already implemented in arduino code
    if(len(x_medians) >= 5):
        x_median_final = x_medians[len(x_medians) // 2]
        y_median_final = y_vals_of_x_medians[len(x_medians) // 2]
    else:
        x_median_final = 0
        y_median_final = 0
    print("the y_vals_of_x_medians vec: ", y_vals_of_x_medians)
    return x_median_final, y_median_final

# idea: (row by row)check 3 pixels at a time, if all white, then do not jump, 
#search to the right until reach a black pixel (cannot go to the left since that will cause array to be unsorted), 
#if all black, jump 10 pixels ahead
# if no white found do the same the next row
# if white found jump to the x index of the median from last row and see there's 3 whites
# if yes, search left and right until black pixel
# if no start from the begining  
def fam1_p1(gray_buff, image_shape, threshold):
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    arr_pixvisited = [0] * image_shape[0]*image_shape[1]     # purely for visualization
    numpixvisited = 0

    for j in range(image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0

        index_largestBlob = -1  #the starting location of the largest blob (the one we want to track)
        index_currentBlob = -1
        len_largestBlob = 0
        len_currentBlob = 0

        i = 0
        while (i < image_shape[1]):

            if(gray_buff[pixcount] <= threshold or gray_buff[pixcount+1] <= threshold or gray_buff[pixcount+2] <= threshold):
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

                #can do this later, track the largest blob
                # if(index_largestBlob == -1):
                #     index_largestBlob = i
                #     index_currentBlob = i

                #searach to the right
                while(gray_buff[pixcount] > threshold and i < image_shape[1]):
                    x = i
                    all_x_gt_thresh.append(x)
                    all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 1
                    i = i + 1
                    pixcount = pixcount + 1
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


        # The median function
        # I don't think 1 pixel difference matters, so not going to do even odd, improves speed
        if(all_x_gt_thresh_real_length != 0):
            x_medians.append(all_x_gt_thresh[all_x_gt_thresh_real_length // 2 ]) # floor division
            y_vals_of_x_medians.append(j)

    ###----Added condition for all black or almost all black)
    ### already implemented in arduino code
    if(len(x_medians) >= 5):
        x_median_final = x_medians[len(x_medians) // 2]
        y_median_final = y_vals_of_x_medians[len(x_medians) // 2]
    else:
        x_median_final = 0
        y_median_final = 0

    #visualization
    plot_buffer(arr_pixvisited, image_shape)
    print("num pix visited: ", numpixvisited)
    print("the y_vals_of_x_medians vec: ", y_vals_of_x_medians)
    return x_median_final, y_median_final

def fam1_p2(gray_buff, image_shape, threshold):
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    arr_pixvisited = [0] * image_shape[0]*image_shape[1]     # purely for visualization
    numpixvisited = 0

    num_conseq_black_rows = 0
    last_row_black = 0      #Let this be a bool in C++ implementation

    # for j in range(image_shape[0]):
    j = 0
    while( j < image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0

        i = 0
        while (i < image_shape[1] and pixcount < (image_shape[0] *image_shape[1])):

            if(gray_buff[pixcount] <= threshold or gray_buff[pixcount+1] <= threshold or gray_buff[pixcount+2] <= threshold):
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

                #can do this later, track the largest blob
                # if(index_largestBlob == -1):
                #     index_largestBlob = i
                #     index_currentBlob = i

                #searach to the right
                while(gray_buff[pixcount] > threshold and i < image_shape[1]):
                    x = i
                    all_x_gt_thresh.append(x)
                    all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 1
                    i = i + 1
                    pixcount = pixcount + 1
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


        # The median function
        # I don't think 1 pixel difference matters, so not going to do even odd, improves speed
        if(all_x_gt_thresh_real_length != 0):
            x_medians.append(all_x_gt_thresh[all_x_gt_thresh_real_length // 2 ]) # floor division
            y_vals_of_x_medians.append(j)

            last_row_black = 0
        else:
            num_conseq_black_rows = num_conseq_black_rows + 1
            last_row_black = 1


        if(num_conseq_black_rows > 2 and last_row_black and j+3 < image_shape[0]):
            j = j + 2
            pixcount = pixcount + 2 * image_shape[1]
        
        j = j + 1



    ###----Added condition for all black or almost all black)
    ### already implemented in arduino code
    if(len(x_medians) >= 5):
        x_median_final = x_medians[len(x_medians) // 2]
        y_median_final = y_vals_of_x_medians[len(x_medians) // 2]
    else:
        x_median_final = 0
        y_median_final = 0

    #visualization
    plot_buffer(arr_pixvisited, image_shape)
    print("num pix visited: ", numpixvisited)
    print("the y_vals_of_x_medians vec: ", y_vals_of_x_medians)
    return x_median_final, y_median_final

#I think it's better to redo the whole thing, draw it out, too many branches to think about
def fam2_p1(gray_buff, image_shape, threshold):
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    arr_pixvisited = [0] * image_shape[0]*image_shape[1]     # purely for visualization
    numpixvisited = 0

    detected = 0 #make this a bool in C++

    for j in range(image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0

        blob_start_index = -1  #the left most starting index of the first blob detected
        

        if(blob_start_index != -1):
            i = blob_start_index
        else:
            i = 0
        
        # print("blob start index: ", blob_start_index)

        while (i < image_shape[1]):
            #if no 3 whites in a row, then skip 10 ahead
            if(gray_buff[pixcount] <= threshold or gray_buff[pixcount+1] <= threshold or gray_buff[pixcount+2] <= threshold):
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
                    blob_start_index = i - 20

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
                    i = i + 1
                    pixcount = pixcount + 1
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
                i = i + len(image[1]) #automatically moves to the next row
                

        # The median function
        # I don't think 1 pixel difference matters, so not going to do even odd, improves speed
        if(all_x_gt_thresh_real_length != 0):
            x_medians.append(all_x_gt_thresh[all_x_gt_thresh_real_length // 2 ]) # floor division
            y_vals_of_x_medians.append(j)
        elif(all_x_gt_thresh_real_length == 0 and blob_start_index == -1 and detected):
            break

    ###----Added condition for all black or almost all black)
    ### already implemented in arduino code
    if(len(x_medians) >= 5):
        x_median_final = x_medians[len(x_medians) // 2]
        y_median_final = y_vals_of_x_medians[len(x_medians) // 2]
    else:
        x_median_final = 0
        y_median_final = 0

    #visualization
    plot_buffer(arr_pixvisited, image_shape)
    print("num pix visited: ", numpixvisited)
    print("the y_vals_of_x_medians vec: ", y_vals_of_x_medians)
    return x_median_final, y_median_final



# Example usage:
threshold = 210  # Define your threshold

# median_x, median_y = process_image(gray_buff, image_shape, threshold)
# print(f"Median X Coordinate: {median_x}")
# print(f"Median Y Coordinate: {median_y}")
# plot_image_with_median_circle(gray_buff, image_shape, median_x, median_y)

plot_bin(image, threshold)

median_x, median_y = pix_median_jason(gray_buff, image_shape, threshold)
print("num pix visited: 57600")
print("median_x: ", median_x, "median_y: ", median_y)
# plot_image_with_median_circle(gray_buff, image_shape, median_x, median_y)

#family 1 proposed 1
#tested and works, ready for ESP implementation
nonlin_x, nonlin_y = fam1_p1(gray_buff, image_shape, threshold)
plot_image_with_median_circle(gray_buff, image_shape, nonlin_x, nonlin_y)
print("nonlin_x: ", nonlin_x, "nonlin_y: ", nonlin_y)

#family 1 propsed 2
nonlin_x, nonlin_y = fam1_p2(gray_buff, image_shape, threshold)
plot_image_with_median_circle(gray_buff, image_shape, nonlin_x, nonlin_y)
print("fam1_p2 x: ", nonlin_x, "fam1_p2 y: ", nonlin_y)

#family 2 propsed 1
nonlin_x, nonlin_y = fam2_p1(gray_buff, image_shape, threshold)
plot_image_with_median_circle(gray_buff, image_shape, nonlin_x, nonlin_y)
print("fam2_p1 x: ", nonlin_x, "fam2_p1 y: ", nonlin_y)