import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
image = Image.open('/home/pratyush/Downloads/Imaage/A.jpeg')
exif = {
    TAGS[k]: v
    for k, v in image._getexif().items()
    if k in TAGS
}
print(exif.split())