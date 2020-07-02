import os
import base64
import json
import codecs
from PIL import Image


def GenerateFile(_json_path, ratio):
    with open(_json_path, 'r') as f:
        read_data = f.read()
    _data = json.loads(read_data)
    imgdata = base64.b64decode(_data['imageData'])
    # I assume you have a way of picking unique filenames
    filename = os.path.join(output_folder,  _data['imagePath'])
    with open(filename, 'wb') as f:
        f.write(imgdata)
    ResizeImage(filename, ratio)
    ResizeAnnotation(_json_path, ratio)


def ResizeImage(infile, ratio=0.5):
    im = Image.open(infile)
    # basewidth = 300
    # wpercent = (basewidth/float(img.size[0]))
    wsize = int((float(im.size[0])*float(ratio)))
    hsize = int((float(im.size[1])*float(ratio)))
    im = im.resize((wsize, hsize), Image.ANTIALIAS)
    os.remove(os.path.join(output_folder, os.path.basename(infile)))
    im.save(os.path.join(output_folder, os.path.basename(infile)), "PNG")


def ResizeImageReference(infile, ratio=0.5):
    im = Image.open(infile)
    wsize = int((float(im.size[0])*float(ratio)))
    hsize = int((float(im.size[1]) * float(ratio)))
    im = Image.open(os.path.join(images_folder, os.path.basename(infile)))
    im = im.resize((wsize, hsize), Image.ANTIALIAS)
    if (os.path.exists(os.path.join(output_folder, os.path.basename(infile)))):
        os.remove(os.path.join(output_folder, os.path.basename(infile)))
    im.save(os.path.join(output_folder, os.path.basename(infile)), "PNG")


def ResizeAnnotation(_json_path, ratio=0.5):
    with open(_json_path, 'r') as f:
        read_data = f.read()
    _data = json.loads(read_data)
    for i, _shape in enumerate(_data["shapes"]):
        for j, _points in enumerate(_shape["points"]):
            _data["shapes"][i]["points"][j] = [
                int(round(_point * ratio)) for _point in _points]
    filename = os.path.join(
        output_folder,  os.path.splitext(os.path.basename(_data['imagePath']))[0]+'.png')
    with open(filename, 'rb') as f:
        read_data = f.read()
        _data['imageData'] = base64.b64encode(read_data).decode('UTF-8')
    _new_json_path = os.path.join(output_folder, os.path.basename(_json_path))
    with open(_new_json_path, 'wb') as f:
        json.dump(_data, codecs.getwriter('utf-8')
                  (f), ensure_ascii=False, indent=4)


annotations_folder = os.path.join(os.getcwd(), 'testing')
imagesizes_folder = os.path.join(os.getcwd(), 'testing')
images_folder = os.path.join(os.getcwd(), 'testing')
output_folder = os.path.join(os.getcwd(), 'images')

lista = [os.path.join(imagesizes_folder, f) for f in os.listdir(imagesizes_folder) if f.endswith(
    ".png")]
for f in lista:
    ResizeImageReference(f, 0.5)

lista = [os.path.join(annotations_folder, f) for f in os.listdir(annotations_folder) if f.endswith(
    ".json")]
for f in lista:
    print(f)
    ResizeAnnotation(f, 0.5)
