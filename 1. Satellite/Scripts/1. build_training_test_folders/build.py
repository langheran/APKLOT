
# coding: utf-8

# In[1]:


IMAGES_PATH=r'H:\ITESM\Dataset ITESM\MCC-I Masters\Thesis\A17\0. labeling\images'

BUILD_DAY=r'8Oct'

BUILD_OUTPUT=r'C:\Users\nhurst\Desktop\dataset' # Database path


# In[16]:


get_ipython().run_line_magic('run', 'sound.py')
Audio(data=sound_signal, rate=8000.0, autoplay=True)


# In[2]:


import os
import numpy as np

BUILD_FOLDER = os.path.join(os.getcwd(),r"builds\{}".format(BUILD_DAY))
TRAIN_FILE = os.path.join(BUILD_FOLDER,"training.txt")
TEST_FILE = os.path.join(BUILD_FOLDER,"testing.txt")

if not os.path.exists(BUILD_FOLDER):
    os.makedirs(BUILD_FOLDER)

training_number=400
testing_number=100
np.random.seed(1)
arr = [f.replace(".json","") for f in os.listdir(IMAGES_PATH) if f.endswith(".json")]
np.random.shuffle(arr)
training=arr[:training_number]
with open(TRAIN_FILE, 'a') as the_file:
    for t in training:
        the_file.write('{}\n'.format(t))
testing=arr[training_number:(training_number+testing_number)]
with open(TEST_FILE, 'a') as the_file:
    for t in testing:
        the_file.write('{}\n'.format(t))

TRAIN_OUTPUT_FOLDER = os.path.join(BUILD_OUTPUT, "training")
TEST_OUTPUT_FOLDER = os.path.join(BUILD_OUTPUT, "testing")


# In[3]:


import os
from shutil import copyfile, rmtree

if not os.path.exists(BUILD_FOLDER):
    raise

training = []
with open(TRAIN_FILE, 'r') as filehandle:
    training = ["{}".format(current_file.rstrip()) for current_file in filehandle.readlines()]
    
testing = []
with open(TEST_FILE, 'r') as filehandle:
    testing = ["{}".format(current_file.rstrip()) for current_file in filehandle.readlines()] 

if os.path.exists(TRAIN_OUTPUT_FOLDER):
    print("Removing '{}'...".format(TRAIN_OUTPUT_FOLDER))
    rmtree(TRAIN_OUTPUT_FOLDER)

if os.path.exists(TEST_OUTPUT_FOLDER):
    print("Removing '{}'...".format(TEST_OUTPUT_FOLDER))
    rmtree(TEST_OUTPUT_FOLDER)
    
if not os.path.exists(TRAIN_OUTPUT_FOLDER):
    os.makedirs(TRAIN_OUTPUT_FOLDER)
if not os.path.exists(TEST_OUTPUT_FOLDER):
    os.makedirs(TEST_OUTPUT_FOLDER)

    
print("Building '{}'...".format(TRAIN_OUTPUT_FOLDER))
for parking in training:
    copyfile(os.path.join(IMAGES_PATH,"{}.png".format(parking)), os.path.join(TRAIN_OUTPUT_FOLDER,"{}.png".format(parking)))
    copyfile(os.path.join(IMAGES_PATH,"{}.json".format(parking)), os.path.join(TRAIN_OUTPUT_FOLDER,"{}.json".format(parking)))

print("Building '{}'...".format(TEST_OUTPUT_FOLDER))
for parking in testing:
    copyfile(os.path.join(IMAGES_PATH,"{}.png".format(parking)), os.path.join(TEST_OUTPUT_FOLDER,"{}.png".format(parking)))
    copyfile(os.path.join(IMAGES_PATH,"{}.json".format(parking)), os.path.join(TEST_OUTPUT_FOLDER,"{}.json".format(parking)))

print("Finished!")
#Audio(data=sound_signal, rate=8000.0, autoplay=True)

