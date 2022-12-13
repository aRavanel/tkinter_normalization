from msilib.schema import PublishComponent
import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import threading
import queue

# ===================================================================================
# Private functions
# ===================================================================================

class VideoCamera:
    '''
    
    '''
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)  #passing 0 to VideoCapture means fetch video from webcam
                
    def __del__(self):
        '''release resources like webcam'''
        self.video_capture.release()
        
    def read_image(self):
        ret, frame = self.video_capture.read()  #get a single frame of video
        return ret, frame  #return the frame to user

    def release(self):
        '''method to release webcam manually '''
        self.video_capture.release()
        

def _detect_face(img):
    '''function to detect face using OpenCV'''
    
    # load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')
    
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);
    
    #if no faces are detected then return original img
    if (len(faces) == 0):
        return img
    
    (x, y, w, h) = faces[0]  # under the assumption that there will be only one face, extract the face area
    return img[y:y+w, x:x+h]  # return only the face part of the image


# ===================================================================================
# Public 
# ===================================================================================

class WebcamThread(threading.Thread):
    '''
    Thread Class for Webcam Feed
    '''
    def __init__(self, app_gui, callback_queue):
        threading.Thread.__init__(self)  #call super class (Thread) constructor
        self.callback_queue = callback_queue  #save reference to callback_queue
        self.app_gui = app_gui  #save left_view reference so that we can update it
        self.should_stop = False  #set a flag to see if this thread should stop
        self.is_stopped = False  #set a flag to return current running/stop status of thread
        self.camera = VideoCamera()  #create a Video camera instance
        
    def run(self):
        '''
        define thread's run method
        '''
        
        #start the webcam video feed
        while (True):
            #check if this thread should stop : if yes then break this loop
            if (self.should_stop):
                self.is_stopped = True
                break
            ret, self.current_frame = self.camera.read_image()  #read a video frame

            if(ret == False):
                print('Video capture failed')
                exit(-1)
                
            #opencv reads image in BGR color space, let's convert it to RGB space
            self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            
            if self.callback_queue.full() == False:
                #put the update UI callback to queue so that main thread can execute it
                self.callback_queue.put((lambda: self.update_on_main_thread(self.current_frame, self.app_gui)))
        
        #fetching complete, let's release camera
        #self.camera.release()
        
            
    #this method will be used as callback and executed by main thread
    def update_on_main_thread(self, current_frame, app_gui):
        app_gui.update_webcam_output(current_frame)
        face = _detect_face(current_frame)
        app_gui.update_neural_network_output(face)
        
    def __del__(self):
        self.camera.release()
            
    def release_resources(self):
        self.camera.release()
        
    def stop(self):
        self.should_stop = True
    
    