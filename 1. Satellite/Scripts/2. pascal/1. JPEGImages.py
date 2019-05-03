
# coding: utf-8

# In[1]:


import os

database_path=r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\1. Dataset\1. Satellite\Dataset\ITESM_20'
pascal_path = os.path.join(database_path,r'PASCAL_format')
root_path = os.path.join(database_path,r'PASCAL_format\JPEGImages')

def GetLista(path):
    global image_root_path
    image_root_path = path
    lista = [f.replace(".json","") for f in os.listdir(image_root_path) if f.endswith(".json")]
    return lista


# In[2]:


import  os
if not os.path.exists(pascal_path):
    os.makedirs(pascal_path)
if not os.path.exists(root_path):
    os.makedirs(root_path)
print(root_path)


# In[3]:


from PIL import Image

def SaveJPEG(lista):
    for file in lista:
        _png_path = os.path.join(image_root_path,file+'.png')
        _im = Image.open(_png_path)
        _rgb_im = _im.convert('RGB')
        _jpg_path = os.path.join(root_path,file+'.jpg')
        if(os.path.isfile(_jpg_path)):
            os.remove(_jpg_path)
        _rgb_im.save(_jpg_path)


# In[4]:


lista=GetLista(os.path.join(database_path,'testing'))
SaveJPEG(lista)


# In[5]:


lista=GetLista(os.path.join(database_path,'training'))
SaveJPEG(lista)

