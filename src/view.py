import tkinter as tk
import tkinter.font as tkFont
from PIL import Image
from PIL import ImageTk
import cv2
import os
root_path = os.path.abspath(os.getcwd())

# =====================
# Internal functions
def _process_image(image, nx=200, ny=200):
        #resize image to desired width and height
        #image = image.resize((self.image_width, self.image_height),Image.ANTIALIAS)
        image = cv2.resize(image, (nx,ny))
        
        #if image is RGB (3 channels, which means webcam image) then draw a circle on it
        #for user to focus on that circle to align face
        #if(len(image.shape) == 3):
        #    cv2.circle(image, self.circle_center, self.circle_radius, self.circle_color, 2)
        image = Image.fromarray(image)  #convert image to PIL library format which is required for Tk toolkit
        image = ImageTk.PhotoImage(image)  #convert image to Tk toolkit format
        return image
    

# =====================


class LeftView(tk.Frame):
    ''' tk frame representing left view'''
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)  #call super class (Frame) constructor
        self.root = root  # save root layour for later references
        self.setup_ui() # load all UI
        self.controller = controller
        
    def setup_ui(self):
        #create a output label
        self.output_label = tk.Label(self, text="Webcam Output", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        self.image_label = tk.Label(self)  #create label to hold image
        self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10)  #put the image label inside left screen
        
    def update_image(self, image):
        self.image_label.configure(image=image)  #configure image_label with new image 
        self.image = image #this is to avoid garbage collection, so we hold an explicit reference
    

class MiddleView(tk.Frame):
    ''' tk frame representing right view'''
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)  #call super class (Frame) constructor
        self.root = root  #save root layour for later references
        self.setup_ui()  #load all UI
        self.controller = controller
        
        
    def setup_ui(self):
        # Title
        self.output_label = tk.Label(self, text="Face detection Output", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        # Placeholder for image
        self.image_label = tk.Label(self)  #create label to hold image
        self.image_label.pack(side="top", fill="both", expand="yes", padx=10, pady=10) #put the image label inside left screen
        
        # Create a button
        self.button = tk.Button(self)
        # GButton_513["bg"] = "#f0f0f0"
        self.button["font"] = tkFont.Font(family='Times',size=10)
        self.button["fg"] = "#000000"
        self.button["text"] = "Take picture"
        self.button["command"] = self.buttonclicked
        self.button.pack(side="top", fill="both", expand="yes", padx=10, pady=10)

        #GButton_513["justify"] = "center"
        #self.button.place(x=380,y=260,width=70,height=25)
        #self.button["command"] = None
        
    def buttonclicked(self):
        image1 = Image.open('./ressources/face_icon.png') # open using PIL
        image1 = image1.resize((50, 50), Image.ANTIALIAS) #resize using pIL
        image1 = ImageTk.PhotoImage(image1) # transform
        self.controller.set_screenshot(image1)
        self.root.right_view.update_image()
        
   
    def update_image(self, image):
        self.image_label.configure(image=image) #configure image_label with new image 
        self.image = image  #this is to avoid garbage collection, so we hold an explicit reference
        


class RightView(tk.Frame):
    ''' tk frame representing right view'''
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)  #call super class (Frame) constructor
        self.root = root  #save root layour for later references
        self.controller = controller
        self.setup_ui()  #load all UI
        
    def setup_ui(self):
        #create a webcam output label
        self.output_label = tk.Label(self, text="Face detection Output", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        # placeholder image normalized
        image_tmp = Image.open('./ressources/face_icon.png') # open using PIL
        image_tmp = image_tmp.resize((40, 40), Image.ANTIALIAS) #resize using pIL
        self.img_tk = ImageTk.PhotoImage(image_tmp) # transform to tkinter form
        self.image_label = tk.Label(self, image = self.img_tk)  #create label to hold image    
        self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10) #put the image label inside left screen

                
    def update_image(self, image):
        # img = ImageTk.PhotoImage(Image.open(root_path + "/ressources/screenshot.png"))
        # image1 = Image.open('./ressources/face_icon.png') # open using PIL
        # image1 = image1.resize((40, 40), Image.ANTIALIAS) #resize using pIL
        # self.img_tk = ImageTk.PhotoImage(image1) # transform to tkinter form
        
        self.image_label.configure(image=image) #configure image_label with new image 
        self.image = image  #this is to avoid garbage collection, so we hold an explicit reference
        

class RightView2(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)  #call super class (Frame) constructor
        self.root = root  #save root layour for later references
        self.controller = controller
        self.setup_ui()  #load all UI
        
    def setup_ui(self):
      
       #create a webcam output label
        self.output_label = tk.Label(self, text="test", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        # create a frame
        # frame = tk.Frame(self.root, width=200, height=200)
        # frame.pack(side="left")
        # frame.place(anchor='center', relx=0.5, rely=0.5)
        
        #img = ImageTk.PhotoImage(Image.open('./ressources/user.jpg'))  # Create an object of tkinter ImageTk
        #image1 = img.resize((50, 50), Image.ANTIALIAS)
        
        image1 = Image.open('./ressources/user.jpg') # open using PIL
        image1 = image1.resize((50, 50), Image.ANTIALIAS) #resize using pIL
        self.img_tk = ImageTk.PhotoImage(image1) # transform to tkinter format
        # label = tk.Label(self.root, image = img_tk)  # Create a Label Widget to display the text or Image
        # label.pack(side="top")

        
        # image normalized
        #img = ImageTk.PhotoImage(Image.open("./ressources/face_icon.png"))
        # img = ImageTk.PhotoImage( file = './ressources/user.jpg')
        # print('img, :', img)
        #img = _process_image(img)
        # self.image_label = tk.Label(self, image = img)  #create label to hold image    
        # self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10) #put the image label inside left screen

        self.canvas = tk.Canvas(self, width = 300, height = 300)      
        self.canvas.pack(side="top")      
        # img_tk = ImageTk.PhotoImage(file='./ressources/user.jpg')      
        self.canvas.create_image(20,20, anchor=tk.NW, image=self.img_tk)  
                


class AppGui:
    '''main gui + functions attached to it'''
            
    def __init__(self, width=950, height=400):
        self.root = tk.Tk()  #initialize the gui toolkit
        self.root.title("Face Detection")  #set title of window
        self.controller = None
        
        # set the size
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr) #self.root.geometry("550x300+300+150")  #set the geometry of the window
        self.root.resizable(width=True, height=False)

        #create left screen view (camera)
        self.left_view = LeftView(self.root, self.controller)
        self.left_view.pack(side='left')
        
        #create middle screen view (cropped camera)
        self.middle_view = MiddleView(self.root, self.controller)
        self.middle_view.pack(side='left')
        
        #create right screen view (screenshot)
        self.right_view = RightView(self.root, self.controller)
        self.right_view.pack(side='left')
        
        #create the right 2 view (normalized image)
        self.right_view2 = RightView2(self.root, self.controller)
        self.right_view2.pack(side='left')
        
        #define image width/height that we will use
        #while showing an image in webcam/neural network
        #output window
        self.image_width=200
        self.image_height=200
        
        #define the center of the cirlce based on image dimentions
        #this is the cirlce we will use for user focus
        self.circle_center = (int(self.image_width/2),int(self.image_height/4))
        self.circle_radius = 15  #define circle radius
        self.circle_color = (255, 0, 0)  #define circle color == red
        self.is_ready = True
        
    def set_controller(self, controller):
        print('controller is set')
        self.controller = controller

    def launch(self):
        #start the gui loop to listen for events
        self.root.mainloop()
        
    def process_image(self, image):
        #resize image to desired width and height
        #image = image.resize((self.image_width, self.image_height),Image.ANTIALIAS)
        image = cv2.resize(image, (self.image_width, self.image_height))
        
        #if image is RGB (3 channels, which means webcam image) then draw a circle on it
        #for user to focus on that circle to align face
        #if(len(image.shape) == 3):
        #    cv2.circle(image, self.circle_center, self.circle_radius, self.circle_color, 2)
        image = Image.fromarray(image)  #convert image to PIL library format which is required for Tk toolkit
        image = ImageTk.PhotoImage(image)  #convert image to Tk toolkit format
        return image
        
    def update_webcam_output(self, image):
        image = self.process_image(image)   #pre-process image to desired format, height etc.
        self.left_view.update_image(image)  #pass the image to left_view to update itself
        
    def update_chat_view(self, question, answer_type): # unused?
        self.left_view.update_chat_view(question, answer_type)
        
    def update_neural_network_output(self, image):
        image = self.process_image(image)  #pre-process image to desired format, height etc.
        self.middle_view.update_image(image)  #pass the image to right_view to update itself
         
    def update_emotion_state(self, emotion_state):
        self.middle_view.update_emotion_state(emotion_state)
        
        
        
    def take_screenshot(self):
        '''
        '''
        current_cropped_image = self.middle_view.image
        self.right_view.update_image(current_cropped_image)
        
    
    
