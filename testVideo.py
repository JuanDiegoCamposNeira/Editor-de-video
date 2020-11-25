import numpy as np
import cv2 as cv 

def overWriteImage(frame, img, position): 
    result = np.zeros(frame.shape, np.uint8)
    # Size of the frame 
    frame_height, frame_width = frame.shape[:2]
    # Size of the image    
    img_height, img_width = img.shape[:2] 
    # Position to start the image
    start_row, start_col = position
    # Position to end the image
    end_row, end_col = [start_row + img_height, start_col + img_width]
    # Indices to traverse the image
    img_i = img_j = 0
    # Loop to traverse and override the image 
    for i in range(0, frame_height): 
        for j in range(0, frame_width): 
            # If the indices are within the limits of the image, write the pixels of the image
            within_rows = i >= start_row and i < end_row
            within_cols = j >= start_col and j < end_col
            if within_rows and within_cols : 
                result[i][j] = img[img_i][img_j]
                img_j += 1
                if img_j == img_height:
                    img_j = 0
                    img_i += 1
                # Eoi
            # Eoi 
            # Otherwise, write the pixels of the frame
            else: 
                result[i][j] = frame[i][j]
            # Eoe
        # Eof
    # Eof
    return result
# EOD

# Main program
if __name__ == "__main__":

    image = cv.imread('./Frames/img2.png')

    i, j = 100, 100
    index = 1
    video = cv.VideoCapture('prueba.mov')

    ret, frame = video.read()
    height, width, _ = frame.shape
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv.VideoWriter('test.mp4', fourcc, 30, (width, height))
    
    while video.isOpened():
        print(f"Processing : [${index}]")
        index += 1
        ret, frame = video.read()

        if index % 30 != 0: 
            continue

        if ret == False: 
            break

        # Draw image on top of the video
        frame = overWriteImage(frame, image, (i, j))
        i += 3
        j += 3

        # Write frame to otput
        output.write(frame)

    # Eow
        
    video.release()
    cv.destroyAllWindows()
# EOM