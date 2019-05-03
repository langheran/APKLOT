
# coding: utf-8

# In[29]:


import warnings
warnings.filterwarnings('ignore')


# In[30]:


import os

#scrips_folder=r"C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training\scripts"
scrips_folder=r"C:\Users\nhurst\Desktop\resultsTec"

pred_batch_folder=os.path.join(scrips_folder, r'pred_batch')
true_batch_folder=os.path.join(scrips_folder, r'true_batch')
overlay_folder=os.path.join(scrips_folder, r'overlays')
false_negatives=os.path.join(scrips_folder, r'false_negatives')
false_positives=os.path.join(scrips_folder, r'false_positives')
true_negatives=os.path.join(scrips_folder, r'true_negatives')
true_positives=os.path.join(scrips_folder, r'true_positives')

pascal_folder=r'W:\Dropbox\MCC-I Masters\Thesis\A17\1. Training\database\PASCAL_format_train300'
SegmentationClass_folder=os.path.join(pascal_folder, r'SegmentationClass')

images_folder=os.path.join(pascal_folder,'JPEGImages')
images_folder=r"C:\Users\nhurst\Desktop\single\images"


# In[31]:


get_ipython().run_line_magic('run', 'evaluate.py')


# In[32]:


import os
from shutil import copyfile, rmtree

for f in os.listdir(pred_batch_folder):
    copyfile(os.path.join(SegmentationClass_folder,f), os.path.join(true_batch_folder,f))


# In[33]:


from scipy import misc
import os
import numpy as np

y_true_batch=[]
y_pred_batch=[]

true_batch_folder_files = [f for f in os.listdir(true_batch_folder) if os.path.isfile(os.path.join(true_batch_folder,f))]
for f in true_batch_folder_files:
    true_mask = misc.imread(os.path.join(true_batch_folder,f), mode='L')
    y_true_batch.append(true_mask)
    pred_mask = misc.imread(os.path.join(pred_batch_folder,f), mode='L')
    y_pred_batch.append(pred_mask)
    if(len(pred_mask)!=len(true_mask)):
        print("{},{},{}".format(f,len(pred_mask),len(true_mask)))

result, results1,results2 = computeIoU(y_true_batch, y_pred_batch)

import pandas as pd
print(len(true_batch_folder_files))
print(result)
#print(np.average(results[np.where(results != -1)]))

df = pd.DataFrame({'file': true_batch_folder_files, 'independent_result': results1[np.where(results1 != -1)], 'dlib_result': results2[np.where(results2 != -1)]})
df.sort_values(by='independent_result', ascending=True, inplace=True)
df


# In[34]:


df[df['file']=='104101927.png']


# In[36]:


df.to_csv(os.path.join(scrips_folder,"results.csv"), sep=',', encoding='utf-8')


# In[37]:


import base64

pd.set_option('display.max_colwidth', -1)

def get_thumbnail(path):
    image = None
    if(path is not None):
        image = open(path, 'rb')
    return image

def image_base64(image):
    if isinstance(image, str):
        image = get_thumbnail(image)
    image_read = image.read()
    image.close()
    image_64_encode = base64.encodestring(image_read)
    data = image_64_encode.decode('ascii') 
    return data
    
def svg_image_formatter(im):
    return f'<img style="background-color: #cccccc" width=200 height=200 src="data:image/svg+xml;base64,{image_base64(im)}">'

def jpeg_image_formatter(im):
    return f'<img style="background-color: #cccccc" width=200 height=200 src="data:image/jpeg;base64,{image_base64(im)}">'

def png_image_formatter(im):
    return f'<img style="background-color: #cccccc" width=200 height=200 src="data:image/png;base64,{image_base64(im)}">'


# In[40]:


import cv2

images = [f.replace(".png","") for f in os.listdir(true_batch_folder) if f.endswith(".png")]

alpha=0.8

for image in images:
    output=cv2.imread(os.path.join(images_folder, image + ".png"))
    groud_truth=cv2.imread(os.path.join(true_batch_folder, image + ".png"))
    overlay=cv2.imread(os.path.join(pred_batch_folder, image + ".png"))
    overlay = cv2.cvtColor(overlay,cv2.COLOR_BGR2RGB)
    overlay[np.where(((overlay!=[255,255,255]) & (groud_truth==[255,255,255])).all(axis=2))] = [0,0,255]
    overlay[np.where(((groud_truth==[255,255,255]) & (overlay==[255,255,255])).all(axis=2))] = [0,255,0]
    overlay[np.where((overlay==[255,255,255]).all(axis=2))] = [255,0,0]
    overlay = cv2.bitwise_or(output, overlay)
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    cv2.imwrite(os.path.join(overlay_folder, image  + ".png"), output)


# In[45]:


import pdfkit
from IPython.display import HTML

df["JPEGImage"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(images_folder,row['file'])), axis=1)
df["ground_truth"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(true_batch_folder,row['file'])), axis=1)
df["prediction"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(pred_batch_folder,row['file'])), axis=1)
df["overlay"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(overlay_folder,row['file'])), axis=1)

df.sort_values(by='independent_result', ascending=True, inplace=True)
html_string=df[['file','independent_result','dlib_result','JPEGImage','ground_truth','prediction','overlay']].to_html(formatters={'JPEGImage': png_image_formatter, 'ground_truth': png_image_formatter, 'prediction': png_image_formatter, 'overlay': png_image_formatter}, escape=False)
HTML(html_string)

f=open(os.path.join(scrips_folder,"icons.html"), "w+")
f.write(html_string)

pdfkit.from_string(html_string,os.path.join(scrips_folder,'results.pdf'))


# In[44]:


import pdfkit
from IPython.display import HTML

df["JPEGImage"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(images_folder,row['file'].replace('.png','.jpg'))), axis=1)
df["ground_truth"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(true_batch_folder,row['file'])), axis=1)
df["prediction"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(pred_batch_folder,row['file'])), axis=1)
df["overlay"]=df[['file']].apply(lambda row: get_thumbnail(os.path.join(overlay_folder,row['file'])), axis=1)

df.sort_values(by='independent_result', ascending=True, inplace=True)
html_string=df[['file','independent_result','dlib_result','JPEGImage','ground_truth','prediction','overlay']][:20].to_html(formatters={'JPEGImage': jpeg_image_formatter, 'ground_truth': png_image_formatter, 'prediction': png_image_formatter, 'overlay': png_image_formatter}, escape=False)
HTML(html_string)

f=open(os.path.join(scrips_folder,"icons.html"), "w+")
f.write(html_string)

pdfkit.from_string(html_string,os.path.join(scrips_folder,'bad_results.pdf'))

df.sort_values(by='independent_result', ascending=False, inplace=True)
html_string=df[['file','independent_result','dlib_result','JPEGImage','ground_truth','prediction','overlay']][:20].to_html(formatters={'JPEGImage': jpeg_image_formatter, 'ground_truth': png_image_formatter, 'prediction': png_image_formatter, 'overlay': png_image_formatter}, escape=False)
HTML(html_string)

f=open(os.path.join(scrips_folder,"icons.html"), "w+")
f.write(html_string)

pdfkit.from_string(html_string,os.path.join(scrips_folder,'good_results.pdf'))

