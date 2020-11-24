import cv2 as cv
import numpy as np

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


if __name__ == "__main__":
    # Read first image
    frame = cv.imread('./Frames/img1.png')
    # Read second image
    img = cv.imread('./Frames/img2.png')
    
    # Image to store the result
    # image.shape -> returns (height, width, chanels) 
    #result = np.zeros(frame.shape, np.uint8)
    #result = overWriteImage(frame, img, (200, 350))
    #cv.imshow("Result", result)
    #cv.waitKey(0)
    

    # Create a video output
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    # fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    height, width, _ = frame.shape
    # video_out = cv.VideoWriter('test.mp4', fourcc, 20.0, frame.shape[:2])

    result = overWriteImage(frame, img, (350, 350))
    result2 = overWriteImage(frame, img, (200, 200))
    result3 = overWriteImage(frame, img, (0,0))
    video = cv.VideoWriter('video_test.mp4', fourcc, 60, (width, height))
    
    for i in range(0, 180):
        video.write(result)

    for i in range(0, 180):
        video.write(result2)

    for i in range(0, 180):
        video.write(result3)
    
    cv.destroyAllWindows()
    video.release()


# EOM