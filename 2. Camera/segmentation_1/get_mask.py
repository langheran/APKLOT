import argparse
import os
from lxml import etree
import json
import cv2
import numpy as np

def GenerateFile(file, image_root_path):
    _json_path = os.path.join(image_root_path,file+'.json')
    with open(_json_path, 'r') as f:
        read_data = f.read()
    _data = json.loads(read_data)
    _shapes = [shape["points"] for shape in _data["shapes"] if shape["label"]=="1"]
    
    filename = file + ".png"
    file_path = os.path.join(root_path, filename)
    if(os.path.isfile(file_path)):
        os.remove(file_path)
    
    _image_path = os.path.join(image_root_path,file+'.png')
    print(_image_path)
    _img = cv2.imread(_image_path, 1)
    
    _mask = np.zeros((_img.shape[0], _img.shape[1]))
    for _shape in _shapes:
        _shape.append(_shape[0])
        _shape = [[int(round(pt[0], 0)), int(round(pt[1], 0))] for pt in _shape]
        _pts=np.array(_shape)
        _roi_pts = _pts.reshape((-1, 1, 2))
        cv2.fillConvexPoly(_mask, _roi_pts, 1)
        
    _mask = _mask.astype(np.bool)  
    out = np.zeros_like(_img)
    out[_mask] = 255
    cv2.imwrite(file_path, out)

    print("file written:", file_path)
    
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the image")
args = vars(ap.parse_args())
input=args["input"]
image_root_path=os.path.dirname(input)
root_path=os.path.join(image_root_path, "masks")
file=os.path.splitext(os.path.basename(input))[0]
GenerateFile(file, image_root_path)