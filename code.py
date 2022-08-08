from pynput.mouse import Button, Controller # library that able the function of the mouse
import cv2 # library to de computer vision
import numpy as np # library that able to work with arrays
import wx
from tkinter import *
from PIL import Image, ImageTk
from screeninfo import get_monitors

screen = get_monitors()[0]

#****************************************************************************************************************
#******************************************FUNCTIONS*************************************************************
#****************************************************************************************************************

def videoCapture():
    cam = cv2.VideoCapture(0)
    return cam


def masksProcess(img, lowerBound, upperBound, kernelOpen, kernelClose):

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert BGR to HSV

    # create the Masks
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen) # removes false positive
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose) # removes false negative
    maskFinal = maskClose

    return maskFinal


def mousePosition(camx, camy, sx, sy, mouseLoc):

    xf = mouseLoc[0]*sx/camx  #calculus that converts the mouse pointer to move for all the screen on axys x, also reverted
    yf = mouseLoc[1]*sy/camy # sy - mouseLoc[1]*sy/camy #calculus that converts the mouse pointer to move for all the screen on axys y
    
    checkMousePosition(xf, yf) 


def contourColor(conts, mLocOld, DampingFactor, sx, sy):

    if len(conts) > 0:
        #this block calculates the central point of the circle drawn when the color is detected  
        c = max(conts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  


        if radius > 1:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)

            (camx, camy) = (640, 420) #camera capture resolution
            cx = (x*sx/camx)
            cy = (y*sy/camy)
            mouseLoc = mLocOld + ((cx, cy)-mLocOld)/DampingFactor


            mousePosition(camx, camy, sx, sy, mouseLoc)


def addX(coordenadas, velocidade):
    if coordenadas[0] < screen.width:
        coordenadas[0]+=velocidade
    else:
        coordenadas[0] = screen.width
    
    return coordenadas[0]


def subX(coordenadas, velocidade):
    if coordenadas[0] > 0:
        coordenadas[0]-=velocidade
    else:
        coordenadas[0] = 0
    
    return coordenadas[0]


def addY(coordenadas, velocidade):
    if coordenadas[1] < screen.height:
        coordenadas[1]+=velocidade

    else:
        coordenadas[1] = screen.height
    
    return coordenadas[1]

def subY(coordenadas, velocidade):
    
    if coordenadas[1] > 0:
        coordenadas[1]-=velocidade
        
    else:
        coordenadas[1] = 0
    
    return coordenadas[1]

def mouseControl(coordenadas, comando):
    if comando == 1:        #up
        coordenadas[1] = subY(coordenadas, velocidade) # movimenta p/ cima
        
    elif comando == 2:      #right
        coordenadas[0] = addX(coordenadas, velocidade) # movimenta p/ direita

        
    elif comando == 3:      #down
        coordenadas[1] = addY(coordenadas, velocidade) # movimenta p/ baixo

    elif comando == 4:      #left
        coordenadas[0] = subX(coordenadas, velocidade)

    
    elif comando == 5:      #Up and left
        coordenadas[0] = subX(coordenadas, velocidade)
        coordenadas[1] = subY(coordenadas, velocidade)

    
    elif comando == 6:      #Up and right
        coordenadas[0] = addX(coordenadas, velocidade)
        coordenadas[1] = subY(coordenadas, velocidade)


    elif comando == 7:      #Down and left
        coordenadas[0] = subX(coordenadas, velocidade)
        coordenadas[1] = addY(coordenadas, velocidade)
     
    
    elif comando == 8:      #Down and right
        coordenadas[0] = addX(coordenadas, velocidade)
        coordenadas[1] = addY(coordenadas, velocidade)
      
    mouse.position = (coordenadas[0],coordenadas[1])


def drawRectangle(img):
    
    cv2.rectangle(img, (400,120),(500,200),(255, 255, 0), 2) # up left
    cv2.rectangle(img, (300,120),(400,200),(255, 255, 0), 2) # up 
    cv2.rectangle(img, (200,120),(300,200),(255, 255, 0), 2) # up right

    cv2.rectangle(img, (200,200),(300,280), (255, 255, 0), 2) # left
    cv2.rectangle(img, (400,200),(500,280),(255, 255, 0), 2) # right

    
    cv2.rectangle(img, (200,280),(300,360),(255, 255, 0), 2) # down left
    cv2.rectangle(img, (300,280),(400,360),(255, 255, 0), 2) # down 
    cv2.rectangle(img, (400,280),(500,360),(255, 255, 0), 2) # down right

    

def checkMousePosition(x, y):
    if (x > 460 and x < 650) and (y > 220 and y < 340): # up left
        mouseControl(coordenadas, 5)

    if (x > 900 and x < 1100) and (y > 345 and y < 470):#   right
        mouseControl(coordenadas, 2)

    if (x > 685 and x < 890) and (y > 475 and y < 600): # down
        mouseControl(coordenadas, 3)

    if (x > 460 and x < 650) and (y > 345 and y < 470):#   left
        mouseControl(coordenadas, 4)

    if (x > 685 and x < 890) and (y > 220 and y < 340): #up
        mouseControl(coordenadas, 1)

    if (x > 900 and x < 1100) and (y > 220 and y < 340): #up right
        mouseControl(coordenadas, 6)

    if (x > 460 and x < 650) and (y > 475 and y < 600): #down left 
        mouseControl(coordenadas, 7)

    if (x > 900 and x < 1100) and (y > 475 and y < 600): #down right
        mouseControl(coordenadas, 8)


#****************************************************************************************************************
#****************************************************************************************************************



mouse = Controller()

lowerBound=np.array([105, 115, 130])
upperBound=np.array([179, 255, 255])


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

mLocOld = np.array([0,0])
mouseLoc = np.array([0,0])
DampingFactor = 2


coordenadas = [712,370]
velocidade = 1


# VIDEOCAPTURE
app = wx.App(False)
(sx, sy) = wx.GetDisplaySize() #coordinates of the size of the screen

(camx, camy) = (640, 420) #camera capture resolution
cam = videoCapture()
cam.set(3,camx)
cam.set(4, camy)

mouse.position = (700,350)


# ************************************* TKINTER ****************************************************************
# *****************************************************************************************************************************

root = Tk()
root.title("Mouse Virtual Acessível")
root.geometry("750x340+300+100")
lb4 = Label(root,text="0",font="Arial 50", fg= "red", bg="white")
lb4.place(x=50, y=50)
root.configure(bg="black")
f1 = LabelFrame(root, bg="blue")
f1.pack()
L1 = Label(f1, bg="blue")
L1.pack()

root=Toplevel()

root.title('Legenda')
root.geometry("300x200+560+500")
image = PhotoImage(file='img/legenda.png')
label = Label(root, image=image)
label.place(anchor='center', relx=0.5, rely=0.35)


while(True):

    ret, img=cam.read() # decodes and returns the next video frame
    img = cv2.flip(img, 1) # Flips a 2D array around vertical, horizontal, or both axes.
    maskFinal = masksProcess(img, lowerBound, upperBound, kernelOpen, kernelClose)

    result = cv2.bitwise_and(img, img, mask = maskFinal)

    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    contourColor(conts, mLocOld, DampingFactor, sx, sy)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    drawRectangle(img)

    img = ImageTk.PhotoImage(Image.fromarray(img))

    L1['image'] = img

    root.update()

    cv2.destroyAllWindows()

