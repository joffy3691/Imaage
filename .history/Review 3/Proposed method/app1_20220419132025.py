import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
import time
import encrypting
import decrypting
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
            [sg.Button('Encrypt'),sg.Button('Decrypt')]]


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
        tic = time.perf_counter()
        encrypting.encryption(values['-FILE LIST-'][0], values['key'])
        toc = time.perf_counter()
        print(f"Finished encryption in {toc - tic:0.4f} seconds")
        window.refresh()
    if event == 'Decrypt' and values['key']:
        print('Starting decryption')
        tic = time.perf_counter()
        decrypting.decryption(values['-FILE LIST-'][0],values['key'], values['Rsakey'], values['Publickey'])
        toc = time.perf_counter()
        print(f"Finished decryption in {toc - tic:0.4f} seconds")
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
            new_size = None
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
        except Exception as E:
            print(f'** Error {E} **')
            pass
# --------------------------------- Close ---------------------------------
window.close()