import cv2
import numpy as np
from PIL import Image
import os

template_img="775_64077.gif"; img_size=(10,10)
template_img="737_2170.gif"; img_size=(9,9)
template_img="1029_71743.gif"; img_size=(11,11)
template_img="1476_43455.gif"; img_size=(10,10)

pil_image = Image.open(template_img).convert('RGB') 
img1 = np.array(pil_image) 
img1 = cv2.resize(img1,img_size, interpolation = cv2.INTER_CUBIC)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) 
template = img1
w, h = template.shape[::-1]

#rotate
#M = cv2.getRotationMatrix2D((w/2,h/2),90,1)
#dst = cv2.warpAffine(img1,M,(h,w))
###

img_directory="test"
all_images = os.listdir(img_directory)

for og_img in all_images:
    pil_image = Image.open(img_directory+"/"+og_img).convert('RGB') 
    img2 = np.array(pil_image)
    img_rgb=img2
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) 
    
    img_gray = img2
    
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    
    if loc[0].size!=0:
        print("Match found: ", og_img)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
        
#        cv2.imshow('Detected',img_rgb)
print("Done")
