from PIL import Image
import piexif
import pickle

tags = {'url_current'   : 'https://stackoverflow.com/q/52729428/1846249',}

data = pickle.dumps(tags)
exif_ifd = {piexif.ExifIFD.MakerNote: data}

exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {},
             "thumbnail": None, "GPS": {}}

img = Image.new('RGB', (500, 500), 'green')
exif_dat = piexif.dump(exif_dict)
img.save('image.jpg',  exif=exif_dat)