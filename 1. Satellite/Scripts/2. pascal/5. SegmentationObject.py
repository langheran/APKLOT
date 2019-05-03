
# coding: utf-8

# In[1]:


import os

database_path=r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\1. Dataset\1. Satellite\Dataset\ITESM_20'
PASCAL_PATH = os.path.join(database_path,r'PASCAL_format')
image_root_path = os.path.join(PASCAL_PATH,r"JPEGImages")
mask_root_path = os.path.join(PASCAL_PATH,r"SegmentationClass")
object_mask_root_path = os.path.join(PASCAL_PATH,r"SegmentationObject")

def GetLista():
    global image_root_path
    lista = [f.replace(".jpg","") for f in os.listdir(image_root_path) if f.endswith(".jpg")]
    return lista


# In[2]:


import  os
if not os.path.exists(object_mask_root_path):
    os.makedirs(object_mask_root_path)


# In[3]:


import seaborn as sns
import cv2
import os
import numpy as np

def PaintArea(l):
    filename=os.path.join(mask_root_path,'{}.png'.format(l))
    img = cv2.imread(filename,1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cmap = sns.diverging_palette(240, 10, n=len(contours), as_cmap=False, center="light")
    mask = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
    for i, contour in enumerate(contours):
        cv2.drawContours(mask, [contour], 0, (int(cmap[i][0]*255),int(cmap[0][1]*255),int(cmap[i][2]*255)), -1)
    filename_output=os.path.join(object_mask_root_path,'{}.png'.format(l))
    cv2.imwrite(filename_output, mask)
    return 0


# In[4]:


import pandas as pd
from matplotlib import pyplot as plt
from IPython.display import display, Markdown, Latex

lista=GetLista()
for i,l in enumerate(lista):
    PaintArea(l)

