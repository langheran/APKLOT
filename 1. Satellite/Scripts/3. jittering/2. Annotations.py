
# coding: utf-8

# In[1]:


import os

database_path=r'C:\Users\nhurst\Desktop\dataset'

image_root_path = os.path.join(database_path,r"PASCAL_format\SegmentationClass")
root_path = os.path.join(database_path,r'PASCAL_format\Annotations')

#image_root_path = r"C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test\SegmentationClass"
#root_path = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test\Annotations'

lista = [f.replace(".png","") for f in os.listdir(image_root_path) if f.endswith(".png")]
# and f.find("-")!=-1

print(lista[:5])


# In[2]:


import cv2

def ReadBWImage(file):
    src = cv2.imread(os.path.join(image_root_path,"{}.png".format(file)), 1)
    return src

def ExtractBoundingBox(file):
    if(os.path.exists(file)):
        file=os.path.splitext(os.path.basename(file))[0]
    #print(file)
    src = ReadBWImage(file)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, threshold_output = cv2.threshold(src_gray, 100, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(threshold_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    src_gray = cv2.cvtColor(src_gray, cv2.COLOR_GRAY2BGR)
    boundRect=[]
    for i, contour in enumerate(contours):
        boundRect.append([coord for coord in cv2.boundingRect(contour)])
        # print(boundRect[i])
    return boundRect, src_gray


# In[3]:


import cv2
from matplotlib import pyplot as plt

for file in lista[:5]:
    boundRects,src_gray = ExtractBoundingBox(file)
    for boundRect in boundRects:
        src_gray=cv2.rectangle(src_gray, (boundRect[0], boundRect[1]), (boundRect[0]+boundRect[2], boundRect[1]+boundRect[3]), (255,0,0), 2)

    width = 12
    height = 12
    plt.figure(figsize=(width, height))
    plt.axis("off")
    plt.imshow(src_gray)
    plt.show()


# In[4]:


import os
from lxml import etree

def GenerateFile(filename, xml):
    s = etree.tostring(root, pretty_print=True).decode("utf-8") 
    file_path = os.path.join(root_path, filename)
    if(os.path.isfile(file_path)):
        # os.remove(file_path)
        return
    with open(file_path, 'w') as f:
        f.write(s)
    #print("file written:", file_path)


# In[5]:


from lxml import etree
import json
import numpy as np
from PIL import Image

def GenerateXML(file):    
    _mask_path = os.path.join(image_root_path,file+'.png')
    
    root = etree.Element('annotation')
    folder = etree.Element('folder')
    folder.text = 'VOC2012'
    root.append(folder)
    
    filename = etree.Element('filename')
    filename.text = file + '.jpg'
    root.append(filename)
    
    source = etree.Element('source')
    database = etree.Element('database')
    database.text = 'The VOC2007 Database'
    source.append(database)
    annotation = etree.Element('annotation')
    annotation.text = 'PASCAL VOC2007'
    source.append(annotation)
    root.append(source)
    
    new_image_root_path=os.path.join(image_root_path, '../JPEGImages')
    _image_path = os.path.join(new_image_root_path,file+'.jpg')
    if(not os.path.exists(_image_path)):
        return None
    _im = Image.open(_image_path)
    _width, _height = _im.size
    _width, _height = str(_width), str(_height)
    size = etree.Element('size')
    width = etree.Element('width')
    width.text = _width
    size.append(width)
    height = etree.Element('height')
    height.text = _height
    size.append(height)
    depth = etree.Element('depth')
    depth.text = '3' # TODO
    size.append(depth)
    root.append(size)
    
    segmented = etree.Element('segmented')
    segmented.text = '1'
    root.append(segmented)
    
    boundRects,src_gray = ExtractBoundingBox(_mask_path)
    
    for _shape in boundRects:
        objecta = etree.Element('object')
        name = etree.Element('name')
        name.text = 'parkingspot'
        objecta.append(name)
        pose = etree.Element('pose')
        pose.text = 'Frontal'
        objecta.append(pose)
        truncated = etree.Element('truncated')
        truncated.text = '0'
        objecta.append(truncated)
        difficult = etree.Element('difficult')
        difficult.text = '0'
        objecta.append(difficult)

        _xmin, _ymin, _xmax, _ymax = _shape[0], _shape[1], _shape[0]+_shape[2], _shape[1]+_shape[3]
        _xmin, _ymin, _xmax, _ymax = str(_xmin), str(_ymin), str(_xmax), str(_ymax)
        
        bndbox = etree.Element('bndbox')
        xmin = etree.Element('xmin')
        xmin.text = _xmin
        bndbox.append(xmin)
        ymin = etree.Element('ymin')
        ymin.text = _ymin
        bndbox.append(ymin)
        xmax = etree.Element('xmax')
        xmax.text = _xmax
        bndbox.append(xmax)
        ymax = etree.Element('ymax')
        ymax.text = _ymax
        bndbox.append(ymax)
        objecta.append(bndbox)

        root.append(objecta)
    
    return root

#root = GenerateXML(f)
#GenerateFile("24833427.xml", root)
for i, f in enumerate(lista):
    if(i%1000==0):
        print(f)
    root = GenerateXML(f)
    if root is not None:
        GenerateFile(f + ".xml", root)

print("Finished!")

