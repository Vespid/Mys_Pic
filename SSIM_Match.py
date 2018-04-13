import cv2
import numpy as np
from PIL import Image
import os
from shutil import copyfile

def gif2rgb(img):
    pil_image = Image.open(img).convert('RGB')
    size=pil_image.size
    b, g, r = pil_image.split()
    pil_image = Image.merge("RGB", (r, g, b))
    img1 = np.array(pil_image) 
    return img1, size

def gif2grey(img):
    im=Image.open(img).convert('LA')
    size=im.size
    return np.array(im), size

template_img=r"F:\Programming\Projects\Mystery_Pic\1512_18048.gif"
img_size=(10,10)
#template_img="1497_37124.gif"
#test_image="archives_office_headless_4772e92b0c.gif"
#test_image="chef_main.gif"

templateImage,templateSize=gif2rgb(template_img)
templateImage = cv2.cvtColor(templateImage, cv2.COLOR_RGB2GRAY)
templateMean=templateImage.mean()

img1=templateImage
img1=cv2.resize(img1,img_size, interpolation = cv2.INTER_CUBIC)
img1=img1.reshape([-1])
ux=img1.mean()


L=255
k1=.01
k2=.03
c1=(k1*L)**2
c2=(k2*L)**2

for folderName, subfolders, filenames in os.walk('priority/Locations'):
    print("The current folder is: " + folderName)
    img_directory=folderName
    all_images = filenames
    
    for og_img in all_images:
        filepath=img_directory+"\\"+og_img
        testImage,testSize=gif2rgb(filepath)
        testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2GRAY)
#        testImage = cv2.resize(testImage,templateSize, interpolation = cv2.INTER_NEAREST)
        
        if testImage.shape[0]<testImage.shape[1]: #height<width
            scaleFactor=int(testImage.shape[0]/img_size[0])
            testImage = cv2.resize(testImage,(int(testImage.shape[1]/scaleFactor),img_size[0]), interpolation = cv2.INTER_CUBIC)
        else:
            scaleFactor=int(testImage.shape[1]/img_size[1])
            testImage = cv2.resize(testImage,(img_size[1],int(testImage.shape[0]/scaleFactor)), interpolation = cv2.INTER_CUBIC)
        
        croppedImage=testImage
        
        for x in range(max(testImage.shape)-9):
            if croppedImage.shape[0]<croppedImage.shape[1]:
                testImage=croppedImage[0:img_size[0],x:img_size[1]+x]
            else:
                testImage=croppedImage[x:img_size[0]+x,0:img_size[1]]
                
            testImage=testImage.reshape([-1])
            uy=testImage.mean()    
            
            variance=np.cov(img1,testImage)
            ox=variance[0,0]
            oxy=variance[0,1]
            oy=variance[1,1]
    
            SSIM=((2*ux*uy+c1)*(2*oxy+c2))/((ux**2+uy**2+c1)*(ox+oy+c2))
            
            total=0
            for x in range(len(img1)):
                total+=(int(testImage[x])-int(img1[x]))**2
            
            MSE=total/(testSize[0]*testSize[1])
    
            #debug
#            print("File:",og_img)
#            print("SSIM: ", SSIM)
#            print("MSE: ", MSE)
    
#            backup values: MSE<11 and SSIM>.28
#            default values: MSE<6 and SSIM>.5
            if MSE<6 and SSIM>.28:
                print("Match found:", og_img)
                print("SSIM: ", SSIM)
                print("MSE: ", MSE)
                print()
                copyfile(img_directory+"\\"+og_img, "guesses"+"\\"+og_img)
                continue