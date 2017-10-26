import requests, bs4, os, threading
#need to redo up to 11240

def find_urls(url):
    print("Downloading page %s.." % url)
    res=requests.get(url)
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text, "lxml")

    imgElem=soup.select("[class='search-img-display']")
    if imgElem == []:
        print("Could not find any images")
    else:
        return imgElem,soup
        
def download_img(start,end):        
    for x in range(start,end):
        imgURL=imgElem[x].get('src')
#        print("Downloading image %s..." % imgURL)
        res = requests.get(imgURL)
        try:
            res.raise_for_status()
        except:
            continue
        directory=imgURL[26:].replace("/","\\")
        folder=os.path.join("images",os.path.split(directory)[0])
        os.makedirs(folder, exist_ok=True)
        imageFile=open(os.path.join("images",directory), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

def find_urlsJN(url):
    print("Downloading page %s.." % url)
    res=requests.get(url)
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text, "lxml")

    imgElem=soup.select("[class='item-result-image']")
    if imgElem == []:
        print("Could not find any images")
    else:
        return imgElem,soup

def download_imgJN(start,end):        
    for x in range(start,end):
        imgURL=imgElem[x].get('src')
#        print("Downloading image %s..." % imgURL)
        imgURL="https://items.jellyneo.net"+imgURL
        res = requests.get(imgURL)
        try:
            res.raise_for_status()
        except:
            continue
        directory=imgURL[26:].replace("/","\\")
        folder="images\\itemsJN"
        os.makedirs(folder, exist_ok=True)
        filename=directory.split(sep="\\")[-1]
        imageFile=open(os.path.join(folder,filename), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()        

#need to redo up to 11240        
url="http://www.drsloth.com/search/newest/?start=0"

while not url.endswith("#"):
    imgElem,soup=find_urls(url)
    
    downloadThreads=[]
    for i in range(0,len(imgElem),5):
        downloadThread=threading.Thread(target=download_img, args=(i,i+4))
        downloadThreads.append(downloadThread)
        downloadThread.start()
    for downloadThread in downloadThreads:
        downloadThread.join()      
        
    try:
        nextPage=soup.select("[class='arrow'] a")[1]
        url="http://www.drsloth.com" + nextPage.get("href")
    except:
        break
print("Done")    

#url="https://items.jellyneo.net/search/?start=31250"
#
#while not url.endswith("#"):
#    imgElem,soup=find_urlsJN(url)
#    
#    downloadThreads=[]
#    for i in range(0,len(imgElem),5):
#        downloadThread=threading.Thread(target=download_imgJN, args=(i,i+4))
#        downloadThreads.append(downloadThread)
#        downloadThread.start()
#    for downloadThread in downloadThreads:
#        downloadThread.join()      
#        
#    try:
#        nextPage=soup.select("[class='arrow'] a")[1]
#        url="https://items.jellyneo.net/search/" + nextPage.get("href")
#    except:
#        break
#print("Done")   


#os.makedirs('images', exist_ok=True)
#while not url.endswith("#"):
#    print("Downloading page %s.." % url)
#    res=requests.get(url)
#    res.raise_for_status()
#    soup=bs4.BeautifulSoup(res.text, "lxml")
#    
#    imgElem=soup.select("[class='search-img-display']")
#    if imgElem == []:
#        print("Could not find any images")
#    else:
#        for x in range(len(imgElem)):
#            imgURL=imgElem[x].get('src')
#            print("Downloading image %s..." % imgURL)
#            res = requests.get(imgURL)
#            try:
#                res.raise_for_status()
#            except:
#                continue
#            directory=imgURL[26:].replace("/","\\")
#            folder=os.path.join("images",os.path.split(directory)[0])
#            os.makedirs(folder, exist_ok=True)
#            imageFile=open(os.path.join("images",directory), 'wb')
#            for chunk in res.iter_content(100000):
#                imageFile.write(chunk)
#            imageFile.close()
#    try:
#        nextPage=soup.select("[class='arrow'] a")[1]
#        url="http://www.drsloth.com" + nextPage.get("href")
#    except:
#        break

            
