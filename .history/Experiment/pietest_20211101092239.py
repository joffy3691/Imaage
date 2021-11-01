import piexif
import piexif.helper
import hashlib
import pickle
from PIL import Image
my_img = Image.open('/home/pratyush/Downloads/Imaage/Experiment/Photo_self.jpeg')
column=[(1,2,3),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata = ' '.join([str(elem) for elem in column])
column=[(1,2,4),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata1 = ' '.join([str(elem) for elem in column])
column=[(2,2,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata2 = ' '.join([str(elem) for elem in column])
column=[(1,2,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata3 = ' '.join([str(elem) for elem in column])
column=[(1,6,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata4 = ' '.join([str(elem) for elem in column])
column=[(1,3,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata5 = ' '.join([str(elem) for elem in column])
column=[(1,1,1),(1,1,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata6 = ' '.join([str(elem) for elem in column])
column=[(1,1,1),(1,1,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata6 = ' '.join([str(elem) for elem in column])
column=[(1,1,1),(1,1,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5),(3,4,5)]
for i in range (500):
    column.append((i,i,i))
userdata6 = ' '.join([str(elem) for elem in column])

tags = {}

for i in range(5):
    uniquecol = []
    for j in range(1000):
        uniquecol.append((i,j,j))
    userdata6 = ' '.join([str(elem) for elem in uniquecol])
    tags[i] = userdata6


# tags = {
#     'url_current' : userdata,
# 'url_current1'   : userdata1,
# 'url_current2'   : userdata2,
# 'url_current3'   : userdata3,
# 'url_current4'   : userdata4,
# 'url_current5'   : userdata5,
# 'url_current6'   : userdata6,
# }

data = pickle.dumps(tags)
exif_ifd = {piexif.ExifIFD.MakerNote: data}


exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {},
             "thumbnail": None, "GPS": {}}


exif_dat = piexif.dump(exif_dict)
my_img.save('A.jpeg',  exif=exif_dat)
