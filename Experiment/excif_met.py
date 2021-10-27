import json
import piexif
import piexif.helper

# %% Write out exif data
# load existing exif data from image
filename="C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/asds.jpg"
exif_dict = piexif.load(filename)
# insert custom data in usercomment field
import array as arr

# array with int type

exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
    json.dumps(userdata),
    encoding="unicode"
)
# insert mutated data (serialised into JSON) into image
piexif.insert(
    piexif.dump(exif_dict),
    filename
)