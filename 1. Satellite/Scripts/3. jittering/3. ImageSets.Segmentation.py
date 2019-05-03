
# coding: utf-8

# In[4]:


import os
import re

database_path=r'C:\Users\nhurst\Desktop\dataset'

root_path0 = os.path.join(database_path,r'PASCAL_format\ImageSets')
root_path = os.path.join(database_path,r'PASCAL_format\ImageSets\Segmentation')
JPEGImages_path = os.path.join(database_path,r'PASCAL_format\JPEGImages')

#root_path0 = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test\ImageSets'
#root_path = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test\ImageSets\Segmentation'
#JPEGImages_path = r'C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test\JPEGImages'

def GetLista(path, filter_list=None):
    global image_root_path
    image_root_path = path
    if(filter_list is None):
        lista = [f.replace(".json","") for f in os.listdir(image_root_path) if f.endswith(".json")]
    else:
        lista = [f.replace(".jpg","") for f in os.listdir(image_root_path) if f.endswith(".jpg") and re.sub(r'(?is).*\-', '', f.replace(".jpg","")) in filter_list]
    return lista


# In[2]:


import  os

if not os.path.exists(root_path0):
    os.makedirs(root_path0)
if not os.path.exists(root_path):
    os.makedirs(root_path)


# In[5]:


import shutil

shutil.move(os.path.join(root_path,"train.txt"),os.path.join(root_path,"train_old.txt"))
shutil.move(os.path.join(root_path,"trainval.txt"),os.path.join(root_path,"trainval_old.txt"))
shutil.move(os.path.join(root_path,"val.txt"),os.path.join(root_path,"val_old.txt"))


# In[8]:


import numpy as np

#lista=GetLista("../../database/training")
#np.random.seed(1)
#np.random.shuffle(lista)
#batch_size = int(np.ceil(len(lista)/4))
#train_list = lista[:batch_size*3] # 1462 1 0:22
#trainval_list = lista[batch_size*3:batch_size*4] # 2913 2 23:

with open(os.path.join(root_path,"train_old.txt")) as f:
    train_list = f.read().splitlines()
    
with open(os.path.join(root_path,"trainval_old.txt")) as f:
    trainval_list = f.read().splitlines()

with open(os.path.join(root_path,"val_old.txt")) as f:
    val_list = f.read().splitlines()

train_list = GetLista(JPEGImages_path,train_list)
trainval_list = GetLista(JPEGImages_path,trainval_list)
val_list = GetLista(JPEGImages_path,val_list)

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

