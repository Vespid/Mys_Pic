from PIL import Image
import os

img_directory="test"

def rgb2hex(t):
    r, g, b = t
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def getDoc(path):
    doc = {}
    try:
        colors = Image.open(path).convert("RGB").getcolors()
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

all_images = os.listdir(img_directory)

img_colors={}
for image in all_images:
    img_colors[image]=getDoc(img_directory+"/"+image)

find_img="1029_71743.gif"
find_colors=getDoc(find_img)

all_keys=list(img_colors.keys())
all_colors=list(img_colors.values())
for x in range(len(all_colors)):
    if all_colors[x]==False:
        continue
    elif set(find_colors).issubset(set(all_colors[x])):
        print("Match found:", all_keys[x])
print("Done")