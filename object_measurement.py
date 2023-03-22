import cv2
import numpy as np
import utils



cam= False

cap=cv2.VideoCapture(0)

path="test.jpeg"

cap.set(10,160)
cap.set(3,1920)
cap.set(4,1080)
scale=3
wP=210 * scale
hP =297 *scale
scm= scale*10 # for mm to cm


while True:
    if cam :success,img=cap.read()

    else: img=cv2.imread(path)

    imgContours, conts = utils.getContours(img,minArea=5000,filter=4)

    if len(conts)!=0:
        biggest = conts [0][2]
        
        imgWarp=utils.warpImg (img,biggest,wP,hP)
        
    
        imgContours2, conts2 = utils.getContours(imgWarp,minArea=2000,filter=4,threshold=[50,50],draw=False)
        

        if len(conts) !=0:
            for obj in conts2:
                cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                nPoints=utils.reorder(obj[2])
               
                
            
                pW=round(utils.findDis(nPoints[0][0]// scm, nPoints[1][0]//scm)/1,1) # width of product in cm
                pH=round(utils.findDis(nPoints[0][0]// scm, nPoints[2][0]//scm)/1 ,1) # height of product in cm

                print(nPoints[3][0])
                
               
                e1=[0,0]
                e2=[630,0]
                e3=[0,891]
                e4=[630,891]
                fD1=utils.freeSpc(nPoints[0][0],e1 ,e2,e3,e4)
                fD2=utils.freeSpc(nPoints[1][0],e1 ,e2,e3,e4)
                fD3=utils.freeSpc(nPoints[2][0],e1 ,e2,e3,e4)
                fD4=utils.freeSpc(nPoints[3][0],e1 ,e2,e3,e4)//scm

                print(fD4)
                
                
             

                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(pW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(pH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

        cv2.imshow("Wrapped",imgContours2)
    imgContours2=cv2.resize(img,(0,0),None,0.5,0.5)
   


    #cv2.imshow("Original",img)
    cv2.waitKey(1)
 