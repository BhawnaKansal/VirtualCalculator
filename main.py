import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self,pos,width,height,value):
        self.pos=pos
        self.width=width
        self.height=height
        self.value=value
    def draw(self,img):  
        cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height) ,(225,225,225),cv.FILLED)
        cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height) ,(50,50,50),3)
        cv.putText(img,self.value,(self.pos[0]+20,self.pos[1]+50),cv.FONT_HERSHEY_PLAIN,2,(50,50,50),2)
    def checkClick(self,x,y):
        if self.pos[0]<x<self.pos[0]+ self.width and self.pos[1]<y<self.pos[1]+ self.height:
            cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height) ,(200,200,200),cv.FILLED)
            cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height) ,(50,50,50),3)
            cv.putText(img,self.value,(self.pos[0]+20,self.pos[1]+70),cv.FONT_HERSHEY_PLAIN,2,(0,0,0),5)
            return True
        else:
            return False


#Webcam
cap=cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#detection of hands
detector=HandDetector(detectionCon=0.8,maxHands=1)

#creating buttons
buttonlistvalues=[['7','8','9','*'],
                  ['4','5','6','-'],
                  ['1','2','3','+'],
                  ['0','.','=','%']]


buttonlist=[]

for x in range(4):
    for y in range(4):
        xpos=x*100+800
        ypos=y*100+150
        buttonlist.append(Button((xpos,ypos),100,100,buttonlistvalues[y][x]))

#Variables
myEquation=''
delayCount=0


while True:
    success,img=cap.read()
    img=cv.flip(img,1)

    hands,img=detector.findHands(img,flipType=False)

    cv.rectangle(img,(800,70),(800+400,70+100) ,(225,225,225),cv.FILLED)
    cv.rectangle(img,(800,70),(800+400,70+100)  ,(50,50,50),3)
    for button in buttonlist:
        button.draw(img)
    
    #check hand
    if hands:
        lmlist=hands[0]["lmList"]
        length, _,img=detector.findDistance(lmlist[8][:2],lmlist[12][:2],img)
        # print(length)
        x,y=lmlist[8][:2]
        # y=lmlist[12][:2]
        if length<50:
            for i,button in enumerate(buttonlist):
                if button.checkClick(x,y) and delayCount==0:
                    myValue=(buttonlistvalues[int(i%4)][int(i/4)])
                    if myValue == '=':
                        myEquation=str(eval(myEquation))
                    else:
                        myEquation +=myValue
                    delayCount=1

    #Avoid duplicates
    if delayCount !=0:
        delayCount+=1
        if delayCount >15:
            delayCount=0



    #Display the Equation
    cv.putText(img,myEquation,(810,130),cv.FONT_HERSHEY_PLAIN,3,(50,50,50),3)

    #Display Image
    cv.imshow('Image',img)
    key=cv.waitKey(1)

    if key== ord('c'):
        myEquation=''
