import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
image = Image.open('/home/pratyush/Downloads/Imaage/Experiment/Photo_self.jpeg')
info = image.getexif()
print(info)