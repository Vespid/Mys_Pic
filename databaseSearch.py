import sqlite3, os, time
from PIL import Image

#creates database if one doesn't exist
def create_database(db_file):
    try:
        conn=sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

#connects to database
def create_connection(db_file):
    try:
        conn=sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

#creates table using create_table_sql parameters(SQL code)
def create_table(conn,create_table_sql):
    try:
        c=conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def insert_data(conn,data):
    sql='''INSERT INTO picdata(name,colors)
            VALUES(?,?)'''
    c=conn.cursor()
    c.execute(sql,data)
    return c.lastrowid
    
def select_data(conn,colors):
    c=conn.cursor()
    sqlQuery="SELECT * FROM picdata WHERE colors LIKE '%"+colors[0]+"%'" 
    for x in range(1,len(colors)):
        sqlQuery+="AND colors LIKE '%"+colors[x]+"%'"
        
    c.execute(sqlQuery)
    rows=c.fetchall()
    if len(rows)>0:
        print("Solution Found:")
        sols=[row[1] for row in rows]
        print(sols)
        return sols
    else:
        print("No solution found")
        return None

def rgb2hex(t):
    r, g, b = t
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def getColors(path,rType):
    try:
        colors = Image.open(path).convert("RGB").getcolors()
        if colors==None:
            size=Image.open(path).size
            colors = Image.open(path).convert("RGB").getcolors(size[0]*size[1])
    except Exception:
        return False
    if colors and rType=="string":
        colors = [rgb2hex(color[1]) for color in colors]
        colorStr = ''.join(colors)
        return colorStr
    elif colors and rType=="list":
        colors = [rgb2hex(color[1]) for color in colors]
        return colors
    else:
        return False

def getDominantColors(path):
    im = Image.open(path).convert('RGB')
    x,y=im.size
    
    colors=[]
    for k in range(0,x):
        for i in range(0,y):
            r, g, b = im.getpixel((k, i))
            colors.append(rgb2hex((r,g,b)))
            
    count={}
    for color in colors:
        if color in count.keys():
            count[color]+=1
        else:
            count[color]=1
    print(count)        
    sortedColors=[x for _,x in sorted(zip(list(count.values()),list(count.keys())), reverse=True)]
    return sortedColors[0:2]

def load_images(imagePath):
    database="MysPic.db"
    conn=create_connection(database)
    with conn:
        for folderName, subfolders, filenames in os.walk(imagePath):
            print("The current folder is: " + folderName)
            img_directory=folderName
            all_images = filenames
            
            for og_img in all_images:
                img_colors=getColors(img_directory+"\\"+og_img,"string")
                if img_colors==False:
                    continue
                else:
                    dataInsert=(og_img,img_colors)
                    insert_data(conn,dataInsert)

def find_solution(database,img):
    print("Searching...")
    t1=time.time()
    colors=getColors(img,"list")
    colors=getDominantColors(img)
    print(colors)
    conn=create_connection(database)
    solution=select_data(conn,colors)
    print("Time: ", time.time()-t1)
    return solution
    
def main():
    #User parameters
    database="MysPic.db" #location of image database
    imagepath="images"  #location of images
    mysPic=r"F:\Programming\Projects\Mystery_Pic\1507_24653.gif" #location of mystery pic
    
    #Creates database and loads images if it does not exist
#    if os.path.isfile(database):
#        conn=create_connection(database)
#    else:
#        conn=create_database(database)
#        conn=create_connection(database)
#        picData=""" CREATE TABLE IF NOT EXISTS picdata (
#                                            id integer PRIMARY KEY,
#                                            name text NOT NULL,
#                                            colors text NOT NULL
#                                        ); """
#        if conn:
#            create_table(conn,picData)
#        load_images(imagepath)
    
    #find solution of Mystery Pic in database    
    find_solution(database,mysPic)  
    
if __name__=="__main__":
    main()  