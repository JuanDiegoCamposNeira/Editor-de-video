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
        self.imageLabel.setMaximumSize(230, 700)

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
        print("Here you can edit the video")
    # EOF

    # Function to open an image file
    def openImage(self): 
       # Get the path to the video file
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open image") 
        # Save the path to the video 
        self.pathToImageFile = pathToFile
        # Put the image into the label 
        self.imageLabel.setPixmap(QPixmap.fromImage(pathToFile))
        self.imageLabel.show()
    # EOF

    # Function to open a video file 
    def openVideo(self):
        # Get the path to the video file
        [pathToFile, x] = QFileDialog.getOpenFileName(self, "Open video") 
        # Save the path to the video 
        self.pathToVideoFile = pathToFile
        # Set the video file to the media player
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(pathToFile)))
        # Enable the buttons to control the video
        self.playPauseButton.setEnabled(True)
        self.editVideoButton.setEnabled(True)
        self.stopButton.setEnabled(True)
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
