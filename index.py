"""
    Libraries 
"""
# Video processing 
# import cv2 as cv
# import numpy as np
# System support
import sys
from typing import ContextManager
# Widgets support
from PySide2.QtWidgets import *
from PySide2.QtCore import *
# Multimedia support
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
# Core elements
from PySide2.QtCore import *
from PySide2.QtGui import *
# Others
import cv2
import numpy as np
import os
import time
# To manage the audio things
from config import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import *
from moviepy.audio.fx.all import volumex
from PIL import Image

"""
    Global Variables
"""
image = ""
videoEdit = ""
cont2 = 0
band = False
posX = 0
posY = 0

# Function auxiliary for move image over video
def overWriteImage(frame, img, position): 
    # Size of the frame 
    frame_height, frame_width = frame.shape[0],frame.shape[1]
    # Size of the image    
    img_height, img_width = img.shape[0],img.shape[1]
    # Position to start the image
    start_row, start_col = position
    # Position to end the image
    end_row, end_col = [start_row + img_height, start_col + img_width]
    # Indices to traverse the image
    img_i = img_j = 0
    # Loop to traverse and override the image 
    if end_row < frame_height and end_col < frame_width and start_row < frame_height and start_col < frame_width:
        for i in range(start_row, end_row): 
            for j in range(start_col, end_col): 
                # If the indices are within the limits of the image, write the pixels of the image
                if img_i >= img_height:
                    break
                frame[i][j] = img[img_i][img_j]
                img_j += 1
                if img_j == img_width:
                    img_j = 0
                    img_i += 1
                # Eoe
            # Eof
            if img_i >= img_height:
                break
        # Eof
    return frame
# EOD

# Function auxiliary for mouse event
def check(event,x,y,flags,param):
    global image, videoEdit, cont2, band, posX, posY
    
    #Conditionals of events for move the image and edit frame
    if event == cv2.EVENT_LBUTTONDOWN:
        posX = x
        posY = y
   
    if event == cv2.EVENT_LBUTTONUP:
        posX = x
        posY = y


"""
    Main window class 
"""
# MainWindow, extends QWidget class
class MainWindow(QWidget):
    # Constructor fot the class 
    def __init__(self):
        # Constructor for the parent class (QWidget) 
        super().__init__()
        
        # Path to the video and image files 
        self.pathToVideoFile = ""
        self.pathToImageFile = ""
        self.pathToAudioFile = ""

        # Window configurations
        self.setWindowTitle("Proyecto Final Desarrollo Multimedial") # Title 
        self.setGeometry(250, 100, 800, 550) # (x_coord, y_coord, width, height)

        # Create the media player container 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface) # (parent, flags)
        self.imageLabel = QLabel()

        # Create the widget for the video 
        videoPlayer = QVideoWidget()

        """
            Controls for the video
        """
        # Button to open a video file
        self.openVideoFileButton = QPushButton("Open Video")   
        self.openVideoFileButton.clicked.connect(self.openVideo)
        # Button to open the image file
        self.openImageFileButton = QPushButton("Open image")
        self.openImageFileButton.clicked.connect(self.openImage)
        # Button to play/pause the video 
        self.playPauseButton = QPushButton("Play/Pause") 
        self.playPauseButton.setEnabled(False)
        self.playPauseButton.clicked.connect(self.playPause)
        # Button to stop the video
        self.stopButton = QPushButton("Stop") 
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop)
        # Button to edit the video
        self.editVideoButton = QPushButton("Edit video")
        self.editVideoButton.setEnabled(False)
        self.editVideoButton.clicked.connect(self.editVideo)
        #Button to add a new audio file
        self.changeAudioButton = QPushButton("Change audio")
        self.changeAudioButton.setEnabled(False)
        self.changeAudioButton.clicked.connect(self.changeAudio)
        self.applyAudioButton = QPushButton("Apply new audio")
        self.applyAudioButton.setEnabled(False)
        self.applyAudioButton.clicked.connect(self.applyAudio)
        # Button to save the edited video
        # Slider for the video 
        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setRange(0,0) 
        self.videoSlider.sliderMoved.connect(self.onSliderChange)

        """
            Layout 
        """
        # Layout to open the video and the image
        openFilesLayout = QVBoxLayout()
        openFilesLayout.addWidget(self.openVideoFileButton)
        openFilesLayout.addWidget(self.openImageFileButton)

        # Layout to display the controls horizontally
        controlsLayout = QHBoxLayout()
        controlsLayout.addLayout(openFilesLayout)
        controlsLayout.addWidget(self.playPauseButton)
        controlsLayout.addWidget(self.stopButton)
        controlsLayout.addWidget(self.editVideoButton)
        controlsLayout.addWidget(self.videoSlider)
        controlsLayout.addWidget(self.changeAudioButton)
        controlsLayout.addWidget(self.applyAudioButton)

        # Layout to display the video and the image
        mediaLayout = QHBoxLayout()
        mediaLayout.addWidget(videoPlayer)
        # mediaLayout.addWidget(self.imageLabel)

        # Layout to display the video, the controls and the labels vertically
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(mediaLayout)
        mainLayout.addLayout(controlsLayout)
        

        # Set the mainLayout as the layout for the window 
        self.setLayout(mainLayout)


        """
            Media output
        """
        self.mediaPlayer.setVideoOutput(videoPlayer)

        """
            Controls for the slider
        """
        self.mediaPlayer.stateChanged.connect(self.onMediaStateChange) 
        self.mediaPlayer.positionChanged.connect(self.onMediaPositionChanged)
        self.mediaPlayer.durationChanged.connect(self.onDurationChanged)

        """ 
            Show the window 
        """       
        self.show()

    # EOC
    
    # Function to edit the video
    def editVideo(self): 
        global image, videoEdit, cont2, band, posX, posY

        #Auxiliary variables
        posX = 0
        posY = 0
        cont2 += 1
        width = int(videoEdit.get(3))
        height = int(videoEdit.get(4))
        outputVideo = cv2.VideoWriter('Video_Edit'+str(cont2)+'.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30,(width,height))

        # Cycle for play the video frame to frame
        while videoEdit.isOpened():
            isFrame, frame = videoEdit.read()

            res = frame

            # It's checked if have read a frame of video
            if not(isFrame):
                break
            
            # It's checked if open a image or not for mixed the frame with the image 
            if not(band):
                cv2.imshow("Edit Video",res)
            else:
                imageOut = image
                if image.shape[1] > width:
                    imageOut = cv2.resize(image,(width//2,image.shape[0]//2),interpolation=cv2.INTER_CUBIC)
                # Eoi
                if image.shape[0] > height:
                    imageOut = cv2.resize(image,(image.shape[1]//2,height//2),interpolation=cv2.INTER_CUBIC)
                # Eoi

                # Function to overwrite the image on top of video frame
                res = overWriteImage(frame,imageOut,(posY,posX))
                # Show the current video frame
                cv2.imshow("Edit Video",res)
                # Callback function to keep track of the mouse in the 'Edit video' window
                cv2.setMouseCallback("Edit Video",check)

            # It's checked if finished the video or was pressed the "Esc" key and close the edit video 
            if cv2.waitKey(30) & 0xFF == 27:
                break

            outputVideo.write(res) #Write the frame for the new video edit
        
        #Clear and close all
        videoEdit.release()
        outputVideo.release()
        cv2.destroyAllWindows()

        #To save it with its audio
        source_video_path = os.path.join(SAMPLE_INPUTS, 'Video_Edit'+str(cont2)+'.mp4')
        source_audio_path = os.path.join(SAMPLE_INPUTS, self.pathToVideoFile)
        final_video_path = os.path.join(SAMPLE_OUTPUTS, 'Video_Edit_'+str(cont2)+'.mp4')

        video_clip = VideoFileClip(source_video_path)

        new_audio_clip = AudioFileClip(source_audio_path)
        new_audio_clip = new_audio_clip.subclip(0, video_clip.duration)
        final_clip = video_clip.set_audio(new_audio_clip)
        final_clip.write_videofile(
            final_video_path, codec='libx264', audio_codec="aac"
        )
        os.remove('Video_Edit'+str(cont2)+'.mp4')
        
    #EOF

    # Function to open an image file
    def openImage(self): 
        global image, videoEdit, cont2, band, posX, posY
       # Get the path to the video file
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open image") 
        # Save the path to the video 
        self.pathToImageFile = pathToFile
        image = cv2.imread(pathToFile)
        print(type(image))
        band = True
    # EOF

    # Function to open a video file 
    def openVideo(self):
        global image, videoEdit, cont2, band, posX, posY
        # Get the path to the video file
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open video") 
        # Save the path to the video 
        self.pathToVideoFile = pathToFile
        # Set the video file to the media player
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(pathToFile)))
        videoEdit = cv2.VideoCapture(pathToFile)
        # Enable the buttons to control the video
        self.playPauseButton.setEnabled(True)
        self.editVideoButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.changeAudioButton.setEnabled(True)
        # Play and pause the video to show the first frame
        self.mediaPlayer.play()
        self.mediaPlayer.pause()
    # EOD

    # Function to handle play/pause button  
    def playPause(self):
        # If the video is currently playing
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.mediaPlayer.pause()
        # Otherwise the video is paused
        else: 
            self.mediaPlayer.play()
    # EOD

    # Function to handle stop button 
    def stop(self):
        self.onSliderChange(0) 
        # PLay and pause the video to update the slider
    
    #Function to change the audio
    def changeAudio(self):
        
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open Audio") 
        self.pathToAudioFile = pathToFile
        self.applyAudioButton.setEnabled(True)
        
        
        
        #os.remove(self.pathToVideoFile)
        #os.rename(new_file_path, self.pathToVideoFile)
        
        
    #Function to apply the change
    def applyAudio(self):
        source_video_path = os.path.join(SAMPLE_INPUTS, self.pathToVideoFile)
        source_audio_path = os.path.join(SAMPLE_INPUTS, self.pathToAudioFile)
        new_file_path = self.pathToVideoFile[:self.pathToVideoFile.find('.')] +"edit" +self.pathToVideoFile[self.pathToVideoFile.find('.'):]
        final_video_path = os.path.join(SAMPLE_OUTPUTS, new_file_path)
        self.pathToVideoFile = new_file_path
        video_clip = VideoFileClip(source_video_path)

        new_audio_clip = AudioFileClip(source_audio_path)
        new_audio_clip = new_audio_clip.subclip(0, video_clip.duration)
        final_clip = video_clip.set_audio(new_audio_clip)
        final_clip.write_videofile(
            final_video_path, codec='libx264', audio_codec="aac"
        )
        pos = self.mediaPlayer.position()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.pathToVideoFile)))
        self.onSliderChange(pos)
        self.mediaPlayer.play()
        videoEdit = cv2.VideoCapture(self.pathToVideoFile)
        self.applyAudioButton.setEnabled(False)

    # EOD

    # Function to handle changes in the slider
    def onSliderChange(self, position):
        self.mediaPlayer.setPosition(position)
    # EOD

    # Function to set the state for the slider
    def onMediaStateChange(self, state): 
        pass
    # EOD

    # Function to set the initial position of the slider
    def onMediaPositionChanged(self, position): 
        self.videoSlider.setValue(position) 
    # EOD

    # Function to set the duration of the slider 
    def onDurationChanged(self, duration): 
        self.videoSlider.setRange(0, duration) 

"""
    Main program
"""
if __name__ == "__main__":
    # Create the instance of the Qt application 
    videoPlayer = QApplication(sys.argv)
    
    # Create the window that contains the video player 
    videoPlayerWindow = MainWindow()

    # Exit succesfull from the application
    sys.exit(videoPlayer.exec_())
