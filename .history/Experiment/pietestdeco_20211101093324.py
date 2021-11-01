import io
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
image = Image.open('/home/pratyush/Downloads/Imaage/A.jpeg')
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in image._getexif().items()
    if k in PIL.ExifTags.TAGS
}
print(exif)