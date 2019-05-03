
# coding: utf-8

# In[1]:


from imgaug import augmenters as iaa


# In[2]:


from scipy import ndimage, misc
#from matplotlib import pyplot

def read_jpg(image_path):
    #print(image_path)
    img = ndimage.imread(image_path, mode="RGB")
    return img


# In[3]:


import imgaug as ia
import numpy as np

multiplier=100

np.random.seed(1)
ia.seed(1)

seq_blur = iaa.Sequential([
    iaa.GaussianBlur(sigma=(0, 2.0)) # blur images with a sigma of 0 to 3.0
])
seq_blur=seq_blur.to_deterministic()
seqs=[]
for seqn in range(multiplier):
    np.random.seed(seqn)
    ia.seed(seqn)
    seq = iaa.Sequential([
        iaa.Crop(px=(0, 50)), # crop images from each side by 0 to 16px (randomly chosen)
        iaa.Fliplr(0.5), # horizontally flip 50% of the images
        iaa.Flipud(0.5),
        iaa.Affine(rotate=(-45, 45))
    ])
    seq=seq.to_deterministic()
    seqs.append(seq)

print(len(seqs))


# In[4]:


import os
import PIL.Image
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
    
PASCAL_PATH=r"C:\Users\nhurst\Desktop\dataset\PASCAL_format"
OUTPUT_PASCAL_PATH=r"C:\Users\nhurst\Desktop\dataset\PASCAL_format"

#PASCAL_PATH=r"C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\database\PASCAL_format"
#OUTPUT_PASCAL_PATH=r"C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\scripts\jittering\test"
    
IMAGE_DIR=os.path.join(PASCAL_PATH,r"JPEGImages")

jpg_training_list = []
with open(os.path.join(PASCAL_PATH,r"ImageSets\Segmentation\train.txt"), 'r') as filehandle:
    jpg_training_list = ["{}.jpg".format(current_file.rstrip()) for current_file in filehandle.readlines()]
    
png_training_list = []
with open(os.path.join(PASCAL_PATH,r"ImageSets\Segmentation\train.txt"), 'r') as filehandle:  
    png_training_list = ["{}.png".format(current_file.rstrip()) for current_file in filehandle.readlines()]

OUTPUT_IMAGE_DIR=os.path.join(OUTPUT_PASCAL_PATH,r"JPEGImages")

MASK_DIR=os.path.join(PASCAL_PATH,r"SegmentationClass")

OUTPUT_MASK_DIR=os.path.join(OUTPUT_PASCAL_PATH,r"SegmentationClass")

image_paths=[os.path.join(IMAGE_DIR,f) for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg") and os.path.basename(f) in  jpg_training_list]
images = [read_jpg(f) for f in image_paths]
mask_paths=[os.path.join(MASK_DIR,f) for f in os.listdir(MASK_DIR) if f.endswith(".png") and os.path.basename(f) in  png_training_list]
images_masks = [read_jpg(f) for f in mask_paths]

i=0
for seqn, seq in enumerate(seqs):
    images_aug = seq_blur.augment_images(seq.augment_images(images))
    images_aug_masks = seq.augment_images(images_masks)
    #print(len(image_paths), len(images_aug), len(images_aug_masks))
    zips=zip(image_paths, images_aug, images_aug_masks)
    for image_path, image, image_mask in zips:
        if(i%multiplier==0):
            print("{} - {}".format(i,image_path))
        quality = 100 # 75
        filename=os.path.splitext(os.path.basename(image_path))[0]
        i=i+1
        if(os.path.exists(os.path.join(OUTPUT_MASK_DIR,"{}-{}.png".format(seqn,filename))) or os.path.exists(os.path.join(OUTPUT_IMAGE_DIR,"{}-{}.jpg".format(seqn,filename)))):
            continue
        im = PIL.Image.fromarray(image)
        im_mask = PIL.Image.fromarray(image_mask)
        im.save(os.path.join(OUTPUT_IMAGE_DIR,"{}-{}.jpg".format(seqn,filename)), format="JPEG", quality=quality)
        im_mask.save(os.path.join(OUTPUT_MASK_DIR,"{}-{}.png".format(seqn,filename)), format="PNG", quality=quality)

print("Finished!")

