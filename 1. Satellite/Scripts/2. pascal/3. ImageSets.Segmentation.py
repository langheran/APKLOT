
# coding: utf-8

# In[1]:


import os

database_path=r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\1. Dataset\1. Satellite\Dataset\ITESM_20'

image_root_path = r""
root_path0 = os.path.join(database_path,r'PASCAL_format/ImageSets')
root_path = os.path.join(database_path,r'PASCAL_format/ImageSets/Segmentation')

def GetLista(path):
    global image_root_path
    image_root_path = path
    lista = [f.replace(".json","") for f in os.listdir(image_root_path) if f.endswith(".json")]
    return lista


# In[2]:


import  os

if not os.path.exists(root_path0):
    os.makedirs(root_path0)
if not os.path.exists(root_path):
    os.makedirs(root_path)


# In[3]:


import numpy as np

lista=GetLista(os.path.join(database_path,r'training'))
np.random.seed(1)
np.random.shuffle(lista)
batch_size = int(np.ceil(len(lista)/4))
train_list = lista[:batch_size*3] # 1462 1 0:22
trainval_list = lista[batch_size*3:batch_size*4] # 2913 2 23:
val_list = GetLista(os.path.join(database_path,r'testing'))

print(len(train_list))
print(len(trainval_list))
print(len(val_list))

import os
def GenerateFile(filename, lista):
    file_path = os.path.join(root_path, filename)
    if(os.path.isfile(file_path)):
        os.remove(file_path)
    with open(file_path, 'w') as f:
        f.write("\n".join(lista))
    print("file written:", file_path)

GenerateFile("train.txt", train_list)
GenerateFile("trainval.txt", trainval_list)
GenerateFile("val.txt", val_list)

