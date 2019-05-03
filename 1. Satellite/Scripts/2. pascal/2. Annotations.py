
# coding: utf-8

# In[1]:


import os

database_path=r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\1. Dataset\1. Satellite\Dataset\ITESM_20'
root_path = os.path.join(database_path,r'PASCAL_format\Annotations')
new_image_root_path=os.path.join(database_path,r'PASCAL_format\JPEGImages')

def GetLista(path):  
    global image_root_path
    image_root_path=path
    lista = [f.replace(".json","") for f in os.listdir(image_root_path) if f.endswith(".json")]
    return lista


# In[2]:


import  os
if not os.path.exists(root_path):
    os.makedirs(root_path)


# In[3]:


import os
from lxml import etree

def GenerateFile(filename, xml):
    s = etree.tostring(root, pretty_print=True).decode("utf-8") 
    file_path = os.path.join(root_path, filename)
    if(os.path.isfile(file_path)):
        os.remove(file_path)
    with open(file_path, 'w') as f:
        f.write(s)
    print("file written:", file_path)


# In[4]:


from lxml import etree
import json
import numpy as np
from PIL import Image

def GenerateXML(file):
    def GetBoundingBox(_points):
        xmin, ymin, xmax, ymax = np.inf, np.inf, 0, 0
        for _point in _points:
            if(_point[0]<xmin):
                xmin=_point[0]
            if(_point[1]<ymin):
                ymin=_point[1]
            if(_point[0]>xmax):
                xmax=_point[0]
            if(_point[1]>ymax):
                ymax=_point[1]
        return int(np.floor(xmin)), int(np.floor(ymin)), int(np.ceil(xmax)), int(np.ceil(ymax))
    _json_path = os.path.join(image_root_path,file+'.json')
    with open(_json_path, 'r') as f:
        read_data = f.read()
    _data = json.loads(read_data)
    
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
    
    _image_path = os.path.join(new_image_root_path,file+'.jpg')
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
    
    for _shape in _data['shapes']:
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

        _xmin, _ymin, _xmax, _ymax = GetBoundingBox(_shape['points'])
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

lista=GetLista(os.path.join(database_path,r"training"))
for f in lista:
    root = GenerateXML(f)
    GenerateFile(f + ".xml", root)

lista=GetLista(os.path.join(database_path,r"testing"))
for f in lista:
    root = GenerateXML(f)
    GenerateFile(f + ".xml", root)

