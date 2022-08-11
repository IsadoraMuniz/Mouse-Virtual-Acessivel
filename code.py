from pynput.mouse import Controller # lib de controle do mouse
import cv2 # lib para manipulacao de imagem
import numpy as np 
import wx
from tkinter import * # lib para desenvolvimento de GUI
from PIL import Image, ImageTk
from screeninfo import get_monitors # lib que permite informar o tamanho da tela

screen = get_monitors()[0]

#****************************************************************************************************************
#******************************************FUNCOES*************************************************************
#****************************************************************************************************************

def videoCapture():
    cam = cv2.VideoCapture(0)
    return cam


def masksProcess(img, lowerBound, upperBound, kernelOpen, kernelClose):

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert BGR to HSV

    # Cria mascara
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen) # Remove falsos positivos
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose) # Remove falsos negativos
    maskFinal = maskClose

    return maskFinal


def mousePosition(camx, camy, sx, sy, mouseLoc):

    xf = mouseLoc[0]*sx/camx  # calculo que converte a posicao em eixo X do cursor do mouse em relacao a tela do computador
    yf = mouseLoc[1]*sy/camy #  # calculo que converte a posicao em eixo Y do cursor do mouse em relacao a tela do computador
    
    checkMousePosition(xf, yf) 


def contourColor(conts, mLocOld, DampingFactor, sx, sy):

    if len(conts) > 0:
        #esse bloco calcula o ponte médio do círculo desenhado ao redor da cor detectada 
        c = max(conts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))  


        if radius > 1:
			# desenha o círculo e ponto medio sobre o frame,
            cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)

            (camx, camy) = (640, 420) #
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
    if comando == 1:        
        coordenadas[1] = subY(coordenadas, velocidade) # movimenta p/ cima
        
    elif comando == 2:      
        coordenadas[0] = addX(coordenadas, velocidade) # movimenta p/ direita

        
    elif comando == 3:      
        coordenadas[1] = addY(coordenadas, velocidade) # movimenta p/ baixo

    elif comando == 4:      
        coordenadas[0] = subX(coordenadas, velocidade) # movimenta p/ esquerda

    
    elif comando == 5:      
        coordenadas[0] = subX(coordenadas, velocidade)# movimenta p/ diagonal esquerda cima
        coordenadas[1] = subY(coordenadas, velocidade)

    
    elif comando == 6:      
        coordenadas[0] = addX(coordenadas, velocidade)# movimenta p/ diagonal direita cima
        coordenadas[1] = subY(coordenadas, velocidade)


    elif comando == 7:      
        coordenadas[0] = subX(coordenadas, velocidade)
        coordenadas[1] = addY(coordenadas, velocidade)# movimenta p/ diagonal esquerda baixo
     
    
    elif comando == 8:     
        coordenadas[0] = addX(coordenadas, velocidade)
        coordenadas[1] = addY(coordenadas, velocidade)# movimenta p/ diagonal direita baixo
      
    mouse.position = (coordenadas[0],coordenadas[1])


def drawRectangle(img):
    
    cv2.rectangle(img, (400,120),(500,200),(255, 255, 0), 2) # espaco cima-esquerda 
    cv2.rectangle(img, (300,120),(400,200),(255, 255, 0), 2) # espaco cima 
    cv2.rectangle(img, (200,120),(300,200),(255, 255, 0), 2) # espaco cima direita

    cv2.rectangle(img, (200,200),(300,280), (255, 255, 0), 2) # espaco esquerda
    cv2.rectangle(img, (400,200),(500,280),(255, 255, 0), 2) # espaco direita

    
    cv2.rectangle(img, (200,280),(300,360),(255, 255, 0), 2) # espaco baixo esquerda
    cv2.rectangle(img, (300,280),(400,360),(255, 255, 0), 2) # espaco baixo 
    cv2.rectangle(img, (400,280),(500,360),(255, 255, 0), 2) # espaco baixo direita

    

def checkMousePosition(x, y):
    if (x > 460 and x < 650) and (y > 220 and y < 340): # cima-esquerda
        mouseControl(coordenadas, 5)

    if (x > 900 and x < 1100) and (y > 345 and y < 470):#   direita
        mouseControl(coordenadas, 2)

    if (x > 685 and x < 890) and (y > 475 and y < 600): # baixo
        mouseControl(coordenadas, 3)

    if (x > 460 and x < 650) and (y > 345 and y < 470):#   esquerda
        mouseControl(coordenadas, 4)

    if (x > 685 and x < 890) and (y > 220 and y < 340): #   cima
        mouseControl(coordenadas, 1)

    if (x > 900 and x < 1100) and (y > 220 and y < 340): #  cima-direita
        mouseControl(coordenadas, 6)

    if (x > 460 and x < 650) and (y > 475 and y < 600): #   baixo-esquerda 
        mouseControl(coordenadas, 7)

    if (x > 900 and x < 1100) and (y > 475 and y < 600): #  baixo-direita
        mouseControl(coordenadas, 8)



# ************************************* DEFINIÇÕES TKINTER ****************************************************************
# *****************************************************************************************************************************

janelaMouseVirtual = Tk()
janelaMouseVirtual.title("Mouse Virtual Acessível")
janelaMouseVirtual.geometry("750x340+300+100") # define o tamanho e posição da janela criada
configuracaoJanela = Label(janelaMouseVirtual,text="0",font="Arial 50", fg= "red", bg="white")
configuracaoJanela.place(x=50, y=50)
janelaMouseVirtual.configure(bg="black")
frameMouseVirtual = LabelFrame(janelaMouseVirtual, bg="blue")
frameMouseVirtual.pack()
labelMouseVirtual = Label(frameMouseVirtual, bg="blue")
labelMouseVirtual.pack()

janelaMouseVirtual=Toplevel() # Criação da janela de legenda - "janela filha"

janelaMouseVirtual.title('Legenda')
janelaMouseVirtual.geometry("300x200+560+500")
image = PhotoImage(file='img/legenda.png')
label = Label(janelaMouseVirtual, image=image)
label.place(anchor='center', relx=0.5, rely=0.35)


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
(sx, sy) = wx.GetDisplaySize() # coordenadas de tamanho da tela

(camx, camy) = (640, 420) # tamanho do frame de captura da camera
cam = videoCapture()
cam.set(3,camx)
cam.set(4, camy)

mouse.position = (700,350) # coordenadas iniciais de posição do cursor do mouse


while(True):

    ret, img=cam.read() # captura cada frame vindo da webcam

    img = cv2.flip(img, 1) # Inverte a imagem em sentido do eixo X
    
    maskFinal = masksProcess(img, lowerBound, upperBound, kernelOpen, kernelClose)

    result = cv2.bitwise_and(img, img, mask = maskFinal)

    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    contourColor(conts, mLocOld, DampingFactor, sx, sy)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    drawRectangle(img)

    img = ImageTk.PhotoImage(Image.fromarray(img))

    labelMouseVirtual['image'] = img

    janelaMouseVirtual.update()

    cv2.destroyAllWindows()

