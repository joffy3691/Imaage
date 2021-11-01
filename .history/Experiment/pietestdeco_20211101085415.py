import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
image = Image.open('/home/pratyush/Downloads/Imaage/A.jpeg')
info = image.getexif()
print(info)