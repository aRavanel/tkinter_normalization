
# coding: utf-8


# explanations 
# - tkinter showing PhotoImage in a loop
# - two tk frames
# - cv2 using VideoCapture, image read one by one in a queue
# - cv2 CascadeClassifier is used to detect faces
# - loop is managed with


import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import queue
from src.view import AppGui
from src.controller_webcam_processing import WebcamThread
from src.controller import Controller
from src.model import Faces

class Wrapper:
    '''
    A GUI Wrappr (Interface) to Connect it with Data
    '''
    def __init__(self):

        self.app_gui = AppGui()
        self.model = Faces()
        self.controller = Controller(self.model, self.app_gui)
        self.app_gui.set_controller(self.controller)
        
        #self.camera = VideoCamera()  #create a Video camera instance
        self.current_frame = None  #intialize variable to hold current webcam video frame
        
        #create a queue to fetch and execute callbacks passed 
        #from background thread
        self.webcam_attempts = 0  #save attempts made to fetch webcam video in case of failure 
        self.app_gui.root.protocol("WM_DELETE_WINDOW", self.on_gui_closing)  #register callback for being called when GUI window is closed
        self.callback_queue = queue.Queue()
        self.webcam_thread = WebcamThread(self.app_gui, self.callback_queue)  #create a thread to fetch webcam feed video

        self.start_video() #start webcam
        self.fetch_webcam_video()  #start fetching video
    
    def on_gui_closing(self):
        self.webcam_attempts = 51
        self.webcam_thread.stop()
        self.webcam_thread.join()
        self.webcam_thread.release_resources()
        self.app_gui.root.destroy()

    def start_video(self):
        self.webcam_thread.start()
        
    def fetch_webcam_video(self):
            try:
                #while True:
                #try to get a callback put by webcam_thread
                #if there is no callback and call_queue is empty
                #then this function will throw a Queue.Empty exception 
                callback = self.callback_queue.get_nowait()
                callback()
                self.webcam_attempts = 0
                #self.app_gui.root.update_idletasks()
                self.app_gui.root.after(70, self.fetch_webcam_video)
                    
            except queue.Empty:
                if (self.webcam_attempts <= 50):
                    self.webcam_attempts = self.webcam_attempts + 1
                    self.app_gui.root.after(100, self.fetch_webcam_video)

    def test_gui(self):
        #test images update
        #read the images using OpenCV, later this will be replaced
        #by live video feed
        image, gray = self.read_images()
        self.app_gui.update_webcam_output(image)
        self.app_gui.update_neural_network_output(gray)
        self.app_gui.update_chat_view("4 + 4 = ? ", "number")  #test chat view update
        self.app_gui.update_emotion_state("neutral")  #test emotion state update
        
    def read_images(self):
        image = cv2.imread('data/test1.jpg')
        #conver to RGB space and to gray scale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image, gray
    
    def launch(self):
        ''''''
        self.app_gui.launch()
        
    def __del__(self):
        ''' when instance is destructed'''
        self.webcam_thread.stop()


# =====================================================================
# ## The Launcher Code For GUI
# =====================================================================

# if __name__ == "__main__":

# create a wrapper instance
wrapper = Wrapper()

# launch the GUI
wrapper.launch()
