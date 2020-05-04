# imports
import base64
from io import BytesIO
import re
from PIL import Image


class ImageHolder:
    def __init__(self, imgtype, imgname, imgpath, imgpil, img64):
        self.imgtype = imgtype
        self.imgname = imgname
        self.imgpath = imgpath
        self.imgpil = imgpil
        self.img64 = img64

    def image_to_base64(self):
        ctoimg = Image.fromarray(self.imgpil.astype('uint8'), 'RGB')
        buffer = BytesIO()
        ctoimg.save(buffer, format='JPEG')
        self.img64 = "data:image/jpg;base64,"+base64.b64encode(buffer.getvalue()).decode('ascii')

    def base64_to_pil(self):
        img_data = re.sub('^data:image/.+;base64,', '', self.img64)
        self.imgpil = BytesIO(base64.b64decode(img_data))
