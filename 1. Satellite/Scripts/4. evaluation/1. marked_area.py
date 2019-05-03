
# coding: utf-8

# In[18]:


import os

PASCAL_PATH = '../../database/PASCAL_format_train300'
root_path = os.path.join(PASCAL_PATH,r"Annotations")
labelme_root_path = os.path.join(PASCAL_PATH,r"labelme")

def GetLista():
    global labelme_root_path
    lista = [f.replace(".json","") for f in os.listdir(labelme_root_path) if f.endswith(".json")]
    return lista

def GetDataset(dataset):
    file_list = []
    with open(os.path.join(PASCAL_PATH,r"ImageSets\Segmentation\{}.txt".format(dataset)), 'r') as filehandle:  
        file_list = ["{}".format(current_file.rstrip()) for current_file in filehandle.readlines()]
    return file_list


# In[19]:


import json

def CountShapes(file):
    _json_path = os.path.join(labelme_root_path,file+'.json')
    with open(_json_path, 'r') as f:
        read_data = f.read()
    _data = json.loads(read_data)
    count=0
    for _shape in _data['shapes']:
        count=count+1
    return count


# In[21]:


file_counts={"train":0,"val":0,"test":0}
area_counts={"train":0,"val":0,"test":0}
train=GetDataset("train")
val=GetDataset("trainval")
test=GetDataset("val")
lista=GetLista()
for f in lista:
    count = CountShapes(f)
    if f in train:
        file_counts["train"]=file_counts["train"]+1
        area_counts["train"]=area_counts["train"]+count
    if f in val:
        file_counts["val"]=file_counts["val"]+1
        area_counts["val"]=area_counts["val"]+count
    if f in test:
        file_counts["test"]=file_counts["test"]+1
        area_counts["test"]=area_counts["test"]+count

print(file_counts)
print(area_counts)

