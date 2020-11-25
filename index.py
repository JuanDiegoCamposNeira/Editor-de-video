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
newFrame = ""
combination = ""
band = False
cont2 = 0

# Function auxiliary for mouse event
def check(event,x,y,flags,param):
    global image, videoEdit, band, cont2, newFrame, combination

    bI, gI, rI = 0,0,0
    
    #Conditionals of events for move the image and edit frame
    if event == cv2.EVENT_LBUTTONDOWN:
        #Get current pixel color
        bI, gI, rI = combination.item(y,x,0), combination.item(y,x,1), combination.item(y,x,2)
        print("X: "+str(x)+" ,Y: "+str(y))
        print("B"+str(bI)+" G"+str(gI)+" R"+str(rI))
   
    if event == cv2.EVENT_LBUTTONUP:
        print("X: "+str(x)+" ,Y: "+str(y))
        print("B"+str(bI)+" G"+str(gI)+" R"+str(rI))

    #Conditionals of events for scale the image

    #Conditionals of events for rotate the image


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

        # Layout to display the video and the image
        mediaLayout = QHBoxLayout()
        mediaLayout.addWidget(videoPlayer)
        mediaLayout.addWidget(self.imageLabel)

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
        global image, videoEdit, band, cont2, newFrame, combination

        #Auxiliary variables
        pause = False
        cont2 += 1
        cont = 0
        directoryAct = os.getcwd()
        directoryFrames = os.path.join(directoryAct, "Frames")
        outputVideo = cv2.VideoWriter('Video Edit'+str(cont2)+'.mp4',cv2.VideoWriter_fourcc(*'mp4v'),20.0,(int(videoEdit.get(3)),int(videoEdit.get(4))))

        #This cycle is for play video frame to frame and be able to edit frame with an image
        while(videoEdit.isOpened()):
            #read a frame
            isFrame, frame = videoEdit.read()
            
            if isFrame:
                cont += 1
                newFrame = frame
                #Show the current frame in a new window
                cv2.imshow("Edit Video",newFrame)
                #Action for pause the video and edit this frame
                if cv2.waitKey(15) & 0xFF == ord('p'):
                    #Change route for save the frames to edit
                    os.chdir(directoryFrames)
                    pause = True
                    cv2.waitKey(0)
                    #Save the current frame converting in an image 
                    cv2.imwrite("frame"+str(cont)+".jpg",frame)
                    newFrame = cv2.imread("frame"+str(cont)+".jpg")
                    width = newFrame.shape[1]
                    height = newFrame.shape[0]
                    #After of open the frame to edit, open a new window (after play again the video)
                    if band:
                        #Note: For edit current frame with an image, before play again the video (in the window Edit Video), click in open image button and select the image
                        imageScale = cv2.resize(image,(width,height),interpolation=cv2.INTER_CUBIC)
                        combination = cv2.hconcat([newFrame,imageScale])
                        cv2.imshow("Edit Frame",combination)
                        cv2.setMouseCallback("Edit Frame",check)
                    else:
                        cv2.imshow("Edit Frame",newFrame)
                    pause = False
                #Action for stop the video and close the window
                if cv2.waitKey(15) & 0xFF == ord('q'):
                    band = False
                    os.chdir(directoryAct)
                    break
                if not pause:
                    outputVideo.write(newFrame)
            else:
                break
        
        #Close the video and all windows
        videoEdit.release()
        outputVideo.release()
        cv2.destroyAllWindows()
    # EOF

    # Function to open an image file
    def openImage(self): 
        global image, videoEdit, band, cont2, newFrame, combination
       # Get the path to the video file
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open image") 
        # Save the path to the video 
        self.pathToImageFile = pathToFile
        image = cv2.imread(pathToFile)
        band = True
    # EOF

    # Function to open a video file 
    def openVideo(self):
        global image, videoEdit, band, cont2, newFrame, combination
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
    

    def changeAudio(self):
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open Audio") 
        source_video_path = os.path.join(SAMPLE_INPUTS, self.pathToVideoFile)
        source_audio_path = os.path.join(SAMPLE_INPUTS, pathToFile)
        new_file_path = self.pathToVideoFile[:self.pathToVideoFile.find('.')] +"edit" +self.pathToVideoFile[self.pathToVideoFile.find('.'):] 
        print(new_file_path)
        final_video_path = os.path.join(SAMPLE_OUTPUTS, new_file_path)

        video_clip = VideoFileClip(source_video_path)

        new_audio_clip = AudioFileClip(source_audio_path)
        new_audio_clip = new_audio_clip.subclip(0, video_clip.duration)

        final_clip = video_clip.set_audio(new_audio_clip)
        final_clip.write_videofile(
            final_video_path, codec='libx264', audio_codec="aac"
        )

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
