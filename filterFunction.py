import numpy
import cv2
import wx
from math import sqrt,atan2,cos,sin
from random import randint

def BGR2RGB(src):
    (B,G,R) = cv2.split(src)
    img=cv2.merge([R,G,B])
    return img

#-------------------------颜色变化-------------------------------------------
def symphonyOfColors(src):
    src=cv2.resize(src,(200,200))
    height,width=src.shape[:2]  
    imgColor=[x for x in range(12)]
    display=numpy.zeros((height*3, width*4, 3), dtype=numpy.uint8)
    gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)  
    for i in range(12): 
        imgColor[i]=cv2.applyColorMap(gray,i)
        x=i%4
        y=i//4  
        displayROI=cv2.resize(imgColor[i],(width,height))
        display[y*height:y*height+height,x*width:x*width+width]=displayROI
    return display
#    cv2.imshow("colorImg",display) 
#    cv2.waitKey(0)  
#src = cv2.imread('c:\\pic\\2.png')
#symphonyOfColors(src)
#------------------------------------------------------------------


#---------------------------浮雕----------------------------------------
def cameo(src):
    height,width,channel=src.shape[:3] 
    if channel!=3:
        src = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)

    (B,G,R) = cv2.split(src.astype(numpy.int16))
    height,width=B.shape[:2] 
    nB1=numpy.zeros((height, width), dtype=numpy.int16) 
    nG1=numpy.zeros((height, width), dtype=numpy.int16) 
    nR1=numpy.zeros((height, width), dtype=numpy.int16)

    nB2=numpy.zeros((height, width), dtype=numpy.int16) 
    nG2=numpy.zeros((height, width), dtype=numpy.int16) 
    nR2=numpy.zeros((height, width), dtype=numpy.int16)

    nB1[0:height-2][0:width-1]=B[1:height][1:width]
    nG1[0:height-2][0:width-1]=G[1:height][1:width]
    nR1[0:height-2][0:width-1]=R[1:height][1:width]

    nB2[1:height][1:width]=B[0:height-2][0:width-1]
    nG2[1:height][1:width]=G[0:height-2][0:width-1]
    nR2[1:height][1:width]=R[0:height-2][0:width-1]
    nB=nB1-nB2
    nG=nG1-nG2
    nR=nR1-nR2
    img=cv2.merge([nB,nG,nR])

    img+=128            
    img[img>255]=255
    img[img<0]=0
    return img.astype(numpy.uint8)
#    cv2.imshow("浮雕",img)
#    cv2.waitKey(0)
#src = cv2.imread('c:\\pic\\2.png') 
#cameo(src)
#-------------------------------------------------------------------------

#--------------------------------------雕刻-------------------------------------
def carve(src):
    height,width,channel=src.shape[:3] 
    if channel!=3:
        src = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)

    (B,G,R) = cv2.split(src.astype(numpy.int16))
    height,width=B.shape[:2] 
    nB1=numpy.zeros((height, width), dtype=numpy.int16) 
    nG1=numpy.zeros((height, width), dtype=numpy.int16) 
    nR1=numpy.zeros((height, width), dtype=numpy.int16)

    nB2=numpy.zeros((height, width), dtype=numpy.int16) 
    nG2=numpy.zeros((height, width), dtype=numpy.int16) 
    nR2=numpy.zeros((height, width), dtype=numpy.int16)

    nB1[0:height-2][0:width-1]=B[1:height][1:width]
    nG1[0:height-2][0:width-1]=G[1:height][1:width]
    nR1[0:height-2][0:width-1]=R[1:height][1:width]

    nB2[1:height][1:width]=B[0:height-2][0:width-1]
    nG2[1:height][1:width]=G[0:height-2][0:width-1]
    nR2[1:height][1:width]=R[0:height-2][0:width-1]
    nB=nB2-nB1
    nG=nG2-nG1
    nR=nR2-nR1
    img=cv2.merge([nB,nG,nR])

    img+=128            
    img[img>255]=255
    img[img<0]=0
    return img.astype(numpy.uint8)
#    cv2.imshow("浮雕",img)
#    cv2.waitKey(0)
#src = cv2.imread('c:\\pic\\2.png') 
#carve(src)
#-------------------------------------------------------------------

#--------------------------------扩张------------------------------------
def expand(src):
    height,width,channel=src.shape[:3]  
    cx=width/2
    cy=height/2
    img=src.copy()  
    #局部放大  
    R=sqrt(width*width+height*height)//2#直接关系到放大的力度,与R1成正比;  
    r=min(cx,cy)
    R=min(R/2,r/2)   
    for y in range(height-1):
        for x in range(width-1): 
            dis=sqrt((x-cx)**2+(y-cy)**2)
            if dis<R:
                newX = int((x-cx)*dis/R+cx)
                newY = int((y-cy)*dis/R+cy)
                img[y][x][0]=src[newY][newX][0]  
                img[y][x][1]=src[newY][newX][1] 
                img[y][x][2]=src[newY][newX][2]  
    return img
#    cv2.imshow("扩张",img)
#    cv2.waitKey(0)
#src = cv2.imread('c:\\pic\\test.png') 
#expand(src)
#---------------------------------------------------------------

#------------------------------------挤压--------------------------------
def squeeze(src):
    height,width,channel=src.shape[:3]  
    cx=width/2
    cy=height/2
    img=src.copy()        
    for y in range(height-1):
        for x in range(width-1): 
            theta=  atan2((y-cy),(x-cx))
            R=numpy.power(((x-cx)**2+(y-cy)**2),0.25)*8
            newX = int(cx+R*cos(theta))
            newY = int(cy+R*sin(theta))
            if newX<=0:
                newX=0
            elif newX>=width:
                newX=width-1
            if newY<=0:
                newY=0
            elif newY>=height:
                newY=eight-1    

            img[y][x][0]=src[newY][newX][0]  
            img[y][x][1]=src[newY][newX][1] 
            img[y][x][2]=src[newY][newX][2]  
    return img
#    cv2.imshow("挤压",img)
#    cv2.waitKey(0)
#src = cv2.imread('c:\\pic\\test.png') 
#squeeze(src)
#_---------------------------------------------------------------------------

#-------------------------------------素描------------------------------------
def sketch(src):
    height,width,channel=src.shape[:3]   
    #去色  
    gray0=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    #反色  
    gray1=255-gray0
    #高斯模糊,高斯核的Size与最后的效果有关  
    gray1=cv2.GaussianBlur(gray1,(11,11),0).astype(numpy.int)
    gray0=gray0.astype(numpy.int)
    #融合：颜色减淡  
    img=gray0+(gray0*gray1)/(256-gray1)
    img[img>255]=255
    img=cv2.merge([img,img,img])
    return img.astype(numpy.uint8)
#    cv2.imshow("素描",img)  
#    cv2.waitKey(0)
#src = cv2.imread('c:\\pic\\test.png') 
#sketch(src)
#-------------------------------------------------------------------------------

#-------------------------------------毛玻璃-------------------------------------------
def frostedGlass(src):
    height,width,channel=src.shape[:3]
    img=src.copy()
    for y in range(1,height-2):  
        for x in range(1,width-2):
            tmp=randint(0,9)  
            nY=y-1+tmp//3
            nX=x-1+tmp%3
            img[y][x][0]=src[nY][nX][0]  
            img[y][x][1]=src[nY][nX][1]
            img[y][x][2]=src[nY][nX][2]
    return img
#    cv2.imshow("扩散",img) 
#    cv2.waitKey(0)  
#src = cv2.imread('c:\\pic\\test.png') 
#frostedGlass(src)
#-----------------------------------------------------------------------------------------

#---------------------------------怀旧-----------------------------------------
def reminiscence(src): 

    (B,G,R) = cv2.split(src.astype(numpy.int16))
    nB=0.272*R+0.534*G+0.131*B
    nG=0.349*R+0.686*G+0.168*B 
    nR=0.393*R+0.769*G+0.189*B
    img=cv2.merge([nB,nG,nR])
    img[img>255]=255
    img[img<0]=0
    return img.astype(numpy.uint8)

#    cv2.imshow("怀旧色",img)
#    cv2.waitKey()
#src = cv2.imread('c:\\pic\\test.png') 
#reminiscence(src)
#-------------------------------------------------------------------------

#--------------------------------连环画---------------------------------------
def comicBook(src): 
    (B,G,R) = cv2.split(src.astype(numpy.int))
    nB=abs(B-G+B+R)*G/256
    nG=abs(B-G+B+R)*R/256 
    nR=abs(G-B+G+R)*R/256  
    img=cv2.merge([nB,nG,nR])
    img[img>255]=255
    img[img<0]=0
    return img.astype(numpy.uint8)
#    cv2.imshow("怀旧色",img)
#    cv2.waitKey()
#src = cv2.imread('c:\\pic\\test.png') 
#comicBook(src)
#---------------------------------------------------------------------------

#-----------------------------------熔铸----------------------------------------
def casting(src): 
    (B,G,R) = cv2.split(src.astype(numpy.int))
    nB=B*128/(G+R +1)
    nG=G*128/(R+B +1)
    nR=R*128/(G+B +1)
    img=cv2.merge([nB,nG,nR])
    img[img>255]=255
    img[img<0]=0
    return img.astype(numpy.uint8)
#    cv2.imshow("熔铸",img)
#    cv2.waitKey()
#src = cv2.imread('c:\\pic\\test.png') 
#casting(src)
#------------------------------------------------------------------

#---------------------------冰冻-----------------------------------
def frozen(src): 
    (B,G,R) = cv2.split(src.astype(numpy.int))
    nB=(B-G-R)*3/2
    nG=(G-R-B)*3/2
    nR=(R-G-B)*3/2
    img=cv2.merge([nB,nG,nR])
    img[img>255]=255
    img[img<0]=-img[img<0]
    return img.astype(numpy.uint8)
#    cv2.imshow("冰冻",img)
#    cv2.waitKey()
#src = cv2.imread('c:\\pic\\test.png') 
#frozen(src)
#-------------------------------------------------------------

#--------------------------羽化-------------------------------------
def eclosion(src):
    height,width,channel=src.shape[:3] 
    cX=width/2
    cY=height/2
    maxV=cX*cX+cY*cY
    minV=(int)(maxV*0.5)  
    diff= maxV -minV
    ratio =height/width if width >height else width/height
    img=src.copy() 
    dst= src.copy() 
    for y in range(height-1):
        for x in range(width-1):  
            b=img[y][x][0]  
            g=img[y][x][1]  
            r=img[y][x][2]  
            dx=cX-x  
            dy=cY-y
            if width > height:  
                 dx= dx*ratio
            else:  
                dy = dy*ratio  
            dstSq = dx*dx + dy*dy
            v = (dstSq / diff)*255
            r = (int)(r +v)
            g = (int)(g +v) 
            b = (int)(b +v) 
            if b<0:
                b=0
            if b>255:
                b=255  
            if g<0:
                g=0 
            if g>255:
                g=255  
            if r<0:
                r=0 
            if r>255:
                r=255  
            dst[y][x][0] = b  
            dst[y][x][1] = g  
            dst[y][x][2] = r  
    return dst
#    cv2.imshow("羽化",dst)
#    cv2.waitKey()
#src = cv2.imread('c:\\pic\\test.png') 
#eclosion(src)

def binaryzation(src):
    src=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret,img=cv2.threshold(src,100,255,cv2.THRESH_BINARY)
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
