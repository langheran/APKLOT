
# coding: utf-8

# In[1]:


import os
import cv2

source_path=os.getcwd()

files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path,f)) and f.find('.png')!=-1]
files


# In[2]:


from PIL import Image

for file in files:
    col = Image.open(file)
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')
    bw.save(file)

