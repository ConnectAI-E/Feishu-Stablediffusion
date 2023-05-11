from util.logger import app_logger

class ImageHandler:
    def __init__(self) -> None:
        pass
    
    def img2img(self, img):
        return img
    
    def img2txt(self, img) -> str:
        return ''
    
    def handle_image(self, myevent):
        app_logger.info(f"handle image {myevent.image}")
        return True