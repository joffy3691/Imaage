import cv2
def uaci2(loc1,loc2):
    img1=cv2.imread(loc1,1)
    img2=cv2.imread(loc2,1)
    height,width=img1.shape
    value=0
    for y in range(height):
        for x in range(width):
            value+=(abs(int(img1[x,y])-int(img2[x,y])))
    value=value*100/(width*height*255)
    return value