
# coding: utf-8

# In[2]:


import os

database_path=r'C:\Users\nhurst\Desktop\dataset'

source = os.path.join(database_path,'PASCAL_format')
destiny = os.path.join(database_path,r'PASCAL_format\Empty')

#source = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A6\dataset\PASCAL_format'
#destiny = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A6\dataset\PASCAL_format\Empty'

lista = [f.replace(".xml","") for f in os.listdir(os.path.join(source, 'Annotations')) if f.endswith(".xml")]

print(lista[:5])


# In[4]:


import xml.etree.ElementTree
from lxml import etree
import json
import numpy as np
from PIL import Image

def Empty(file):  
    filePath=os.path.join(os.path.join(source, 'Annotations'),file)
    tree = etree.parse(filePath)
    object_count=0
    for el in tree.iter('object'):
        object_count=object_count+1
        break
    return object_count==0

def MoveFiles(file):
    print("Moving {}".format(file))
    if(not os.path.isdir(destiny)):
        os.makedirs(destiny)
    
    folders=['Annotations', 'JPEGImages', 'SegmentationClass', 'SegmentationObject']
    
    extensions={'Annotations':'xml', 'JPEGImages':'jpg', 'SegmentationClass':'png', 'SegmentationObject':'png'}
    
    for folder in folders:
        source_folder=os.path.join(source, folder)
        destiny_folder=os.path.join(destiny, folder)
        if(not os.path.isdir(destiny_folder)):
            os.makedirs(destiny_folder)
        os.rename(os.path.join(source_folder,file+"."+extensions[folder]), os.path.join(destiny_folder,file+"."+extensions[folder]))

i = 0
for f in lista:
    filename=f + ".xml"
    if Empty(filename):
        MoveFiles(f)
    if(i%100==0):
        print("{} - {}".format(i,filename))
    i=i+1


# In[5]:


import cv2
import os

#source = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A6\dataset\PASCAL_format\test'
source = r'C:\Users\Paperspace\Documents\Datasets\PASCAL_format'

folders=['SegmentationClass', 'SegmentationObject']

def ThresholdImage(file):
    img = cv2.imread(file,0)
    ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    cv2.imwrite(file, thresh1)
    print(file)

for folder in folders:
    folder=os.path.join(source, folder)
    image_paths=[os.path.join(folder,f) for f in os.listdir(folder) if f.endswith(".png")]
    for p in image_paths:
        ThresholdImage(p)
        
print("Finished!")

