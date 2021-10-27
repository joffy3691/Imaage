import json
import piexif
import piexif.helper

# %% Write out exif data
# load existing exif data from image
filename="C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/asds.jpg"
exif_dict = piexif.load(filename)
# Extract the serialized data
user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
# Deserialize
d = json.loads(user_comment)
print("Read in exif data: %s" % d)