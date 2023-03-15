import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
from openpyxl import Workbook
import os
from firebase import firebase
import json
import imutils 
from datetime import date
from datetime import datetime

fb_app = firebase.FirebaseApplication('https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/',None)


cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

cap.set(3,640)
cap.set(4,480)
font = cv2.FONT_HERSHEY_COMPLEX
outputlist = []
        

df = pd.read_excel(r'C:\Python311\qrcodescanner\validation.xlsx')

today = date.today()

day=today.strftime("%Y-%m-%d")


print(day)

while True:
    
        #outputlist.clear()
        #productsnumber=0
        success,test1 = cap.read()
    
        grayscale=cv2.cvtColor(test1,cv2.COLOR_BGR2GRAY)


        for barcode in decode(grayscale):
       

           myData= barcode.data.decode('utf-8')

                # Product Validation
           if myData in df :

            Validation = "Scanned"
            Color = (0,255,0)

           else :
            Validation = "Invalid Product "
            Color = (0,0,255)
          
    
        
        
         #BoundingBoxes
            pts =np.array([barcode.polygon],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(grayscale,[pts],True,Color,5)

            rectn= cv2.minAreaRect(pts)


        # Get 2D Coordinates

            box = cv2.boxPoints(rectn)
            box= np.int0(box)
            center = np.mean(box, axis=0)

            for i in range(4):

          
                #print("Product:",myData," //","Center Coordinates :  ({}, {})".format(center[0], center[1]))

                if center[0] < 320 and center[1] > 240 :
               
                    location = "upper left"

                elif center[0] > 320 and center[1] > 240 :
             
                    location = "upper right"

                elif  center[0] < 320 and center[1] < 240 :
                    location = "lower left"
                else :
                    location = "lower right"
                    break
     
  
            if center[0] < 320 and center[1] > 240 and "Sensitive" in myData  :

                print( "Info for ", myData, "WARNING !!! Sensitive product is located in the upper left part !!")

            elif center[0] > 320 and center[1] > 240 and "Sensitive" in myData  :

                print( "Info for ", myData, "WARNING !!! Sensitive product is located in the upper right part !!")  
                break

            # Split MyData For Getting Some Spesific Info

            
            start = "Serial Number:"
            end=" Order Date"

            
            p_serialnumber=myData.split(start)[1].split(end)[0]

            #print(p_serialnumber)
            

            orddate= myData.split("Order Date:")

        
            p_date = datetime.strptime(orddate[-1],"%d-%m-%Y").date()
        
        
            difference = p_date - today # calculation of left times for order
            dif_in_day= difference.total_seconds()

            dif_in_day=dif_in_day  * 1000000  
            int_dif=int(dif_in_day)

            dif=int_dif/86400000000
            
           
            
            if dif < 8 :
                ShortTime = "It's almost time to order, place the products towards the exit" 
                print(ShortTime + " for the "  + p_serialnumber +"  located in "+ location )
            else :
                break 
        


            #Messages On Stream
            pts2= barcode.rect
            cv2.putText(grayscale,Validation,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
            0.9,Color,2)
        

            # Add new Output to list and delete duplicates
            outputlist.append(myData)
            outputlist=list(dict.fromkeys(outputlist)) #delete duplicates from a list
            json_output = json.dumps(outputlist)
            #print(json_output)


            #Find Total Numbers of QR Codes
            productsnumber = len(outputlist) 
            json_totalnum = json.dumps(productsnumber)


            #Firebase Connection
            send_to_firebase = fb_app.patch("https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/",{"/QR Code/Outputs" : json_output})
            send_to_firebase_totalnum = fb_app.patch("https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/",{"/QR Code/Total Number ":json_totalnum})
        
        

        cv2.imshow('Result',grayscale)
        cv2.waitKey(30)
        

    

   










