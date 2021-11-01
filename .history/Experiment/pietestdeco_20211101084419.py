import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
image = Image.open('C:/Users/vishn/PycharmProjects/imo/dtjdtg/Experiment/A.jpg')
info = image.getexif()
print(info)