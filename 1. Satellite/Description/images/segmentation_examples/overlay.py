import numpy as np
import cv2
import os
import argparse
from os.path import basename

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-m", "--mask", required=True,
	help="path to the mask image")
args = vars(ap.parse_args())

image_root_path=os.path.join(os.getcwd(),args["image"])
mask_root_path=os.path.join(os.getcwd(),args["mask"])

alpha=0.8

output=cv2.imread(image_root_path)
overlay=cv2.imread(mask_root_path)
overlay = cv2.bitwise_or(output, overlay)
cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
cv2.imwrite(os.path.join(os.path.dirname(mask_root_path), os.path.splitext(basename(mask_root_path))[0]+".overlay" + ".png"), output)