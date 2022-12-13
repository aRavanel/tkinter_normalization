class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def set_screenshot(self,img):
        self.model.screenshot_face = img
        
    def get_screenshot(self):
        return self.model.screenshot_face
    
    def update_rightview(self):
        self.view.right_view.update_image(self.model.screenshot_face)
        
        
        