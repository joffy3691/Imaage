import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
import encrypt
import decrypt
import hashes
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import time
import json
import piexif
import piexif.helper
import parameterisedwithout
import param2
def convert_to_bytes(file_or_bytes, resize=None):
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# --------------------------------- Layout ---------------------------------

left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Text('Secret Key'),sg.In(key='key', size=(10,1))],
            [sg.Text('Public Key'),sg.In(key='Publickey', size=(50,1))],
            [sg.Text('RSA Key'),sg.In(key='Rsakey', size=(50,1))],
            [sg.Button('Encrypt'),sg.Button('Decrypt')],
            [sg.Text('Mode'),sg.Drop(values=('Secure', 'Fast'),key='mode')],
            [sg.Text('avg-Hash calculated: '), sg.Text(size=(15,1), key='-OUTPUT1-')],
            [sg.Text('p-Hash calculated: '), sg.Text(size=(15,1), key='-OUTPUT2-')],
            [sg.Text('d-Hash calculated: '), sg.Text(size=(15,1), key='-OUTPUT3-')],
            [sg.Text('w-Hash calculated: '), sg.Text(size=(15,1), key='-OUTPUT4-')],
            [sg.Text('color-Hash calculated: '), sg.Text(size=(15,1), key='-OUTPUT5-')]]


images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]


layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c')]]

# --------------------------------- Window ---------------------------------
window = sg.Window('Image Locker', layout,resizable=True)
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Encrypt' and values['key']:
        print('Starting encryption')
        im = cv2.imread(values['-FILE LIST-'][0])
        filename = values['-FILE LIST-'][0]
        exif_dict = piexif.load(filename)
        tic = time.perf_counter()
        faces, confidences = cv.detect_face(im)
        # loop through detected faces and add bounding box
        userdata=""
        for face in faces:
            (startX, startY) = face[0], face[1]
            (endX, endY) = face[2], face[3]
            userdata=str(face[0])+" "+str(face[1])+" "+str(face[2])+" "+str(face[3])
            crop = im[startY:endY, startX:endX]
            cv2.imwrite("crop_{0}.jpeg", crop)
            parameterisedwithout.encrypt("crop_{0}.jpeg", values['key'])
            cdfg=cv2.imread("crop_{0}.jpeg")
            im[startY:endY, startX:endX] = cdfg
            exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
                json.dumps(userdata),
                encoding="unicode"
            )
            # insert mutated data (serialised into JSON) into image
            piexif.insert(
                piexif.dump(exif_dict),
                filename
            )
            cv2.imwrite(values['-FILE LIST-'][0], im)

        toc = time.perf_counter()
        print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")
        window.refresh()
    if event == 'Decrypt' and values['key']:
        print('Starting decryption')
        im = cv2.imread(values['-FILE LIST-'][0])
        filename = values['-FILE LIST-'][0]
        exif_dict = piexif.load(filename)
        # Extract the serialized data
        user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        # Deserialize
        d = json.loads(user_comment)
        x1 = d.split()
        print(x1[1])
        print(x1[3])
        print(x1[0])
        print(x1[2])
        crop = im[int(x1[1]):int(x1[3]), int(x1[0]):int(x1[2])]
        cv2.imwrite("crop_{1}.jpeg", crop)
        param2.decrypt('C:/Users/vishn/PycharmProjects/imo/dtjdtg/Image-Encryption-and-Authentication/baboon.png',values['key'], values['Rsakey'], values['Publickey'])
        cdf = cv2.imread("crop_{1}.jpeg")
        im[int(x1[1]):int(x1[3]), int(x1[0]):int(x1[2])] = cdf
        plt.imshow(im)
        plt.show()
        cv2.imwrite("garbage1.jpeg", im)
        window.refresh()
    if event == '-FOLDER-':
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            window['-OUTPUT1-'].update(hashes.ahash(values['-FILE LIST-'][0]))
            window['-OUTPUT2-'].update(hashes.phash(values['-FILE LIST-'][0]))
            window['-OUTPUT3-'].update(hashes.dhash(values['-FILE LIST-'][0]))
            window['-OUTPUT4-'].update(hashes.whash(values['-FILE LIST-'][0]))
            window['-OUTPUT5-'].update(hashes.chash(values['-FILE LIST-'][0]))
            new_size = None
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
        except Exception as E:
            print(f'** Error {E} **')
            pass
# --------------------------------- Close ---------------------------------
window.close()
