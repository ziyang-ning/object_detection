def fam2_p2(gray_buff, image_shape, threshold):
    pixcount = 0    #using this iterator, might be more efficent than doing mult everytime
    x_medians = []   # size will the the y length of the image
    y_vals_of_x_medians = []
    numpixvisited = 0

    detected = 0 #make this a bool in C++
    blob_start_index = -1  #the left most starting index of the first blob detected

    num_conseq_black_rows = 0
    last_row_black = 0      #Let this be a bool in C++ implementation

    # for j in range(image_shape[0]):
    j = 0
    while( j < image_shape[0]):
        all_x_gt_thresh = []    #max size will be the x length of the image
        all_x_gt_thresh_real_length = 0

        if(blob_start_index != -1 and blob_start_index - 20 > 0):
            i = blob_start_index - 20
            pixcount = pixcount + i
        else:
            i = 0

        while (i < image_shape[1] and pixcount < (image_shape[0] *image_shape[1])):

            if(gray_buff[pixcount] <= threshold or gray_buff[pixcount+1] <= threshold or gray_buff[pixcount+2] <= threshold):
                if(i+10 < image_shape[1]):
                    i = i + 10
                    pixcount = pixcount + 10
                    

                else:
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

                #searach to the right
                while(gray_buff[pixcount] > threshold and i < image_shape[1]):
                    x = i
                    all_x_gt_thresh.append(x)
                    all_x_gt_thresh_real_length = all_x_gt_thresh_real_length + 1
                    i = i + 5
                    pixcount = pixcount + 5
                    numpixvisited = numpixvisited + 1



                #this means that the current pixcount is already checked and it's not white
                if i != image_shape[1]:
                    i = i + 1
                    pixcount = pixcount + 1
                    numpixvisited = numpixvisited + 1

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
    else:
        x_median_final = 0
        y_median_final = 0

    return x_median_final, y_median_final