import os

class ImageConfig:
    def __init__(self):
        self.IMG_FOLDER = os.path.join("static", "IMG")
        self.Apple = os.path.join(self.IMG_FOLDER, "apple.png")
        
    def get_apple_image(self):
        return self.Apple