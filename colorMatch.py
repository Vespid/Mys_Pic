from PIL import Image
import os
from shutil import copyfile

def rgb2hex(t):
    r, g, b = t
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def getDoc(path):
    doc = {}
    try:
        colors = Image.open(path).convert("RGB").getcolors()
        if colors==None:
            size=Image.open(path).size
            colors = Image.open(path).convert("RGB").getcolors(size[0]*size[1])
    except Exception:
        return False
    if colors:
        colors = [rgb2hex(color[1]) for color in colors]
        doc["name"] = path.split("/")[-1]
        for color in colors:
            doc[color] = True
        return doc
    else:
        return False
    

find_img="1493_11938.gif" #one
find_colors=getDoc(find_img)
find_colors=list(find_colors)


for folderName, subfolders, filenames in os.walk('guesses'):
    print("The current folder is: " + folderName)
    img_directory=folderName
    all_images = filenames
    
    for og_img in all_images:
        img_colors=getDoc(img_directory+"\\"+og_img)
#        if set(find_colors).issubset(set(img_colors)):
#            print("Match found:", og_img)
#            copyfile(img_directory+"\\"+og_img, "guesses"+"\\"+og_img)
        if img_colors==False:
            continue
        else:
            img_colors=list(img_colors)
            if 100.0 * len(set(find_colors) & set(img_colors)) / (len(find_colors))>=50:
                print("Match found:", og_img)
#                print(100.0 * len(set(find_colors) & set(img_colors)) / (len(find_colors)))
                copyfile(img_directory+"\\"+og_img, "guesses"+"\\"+og_img)

print("Done")


