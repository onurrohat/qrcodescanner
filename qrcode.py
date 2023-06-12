import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
#from openpyxl import Workbook
import os
#from firebase import firebase
import json
#import imutils
from datetime import date
from datetime import datetime
from smtplib import SMTP

#fb_app = firebase.FirebaseApplication('https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/',None)

subject="WARNUNG Für İhr Lager !"

mymail="onuroktayr@gmail.com"
password="khamcatdauvqcrpz"

sendTo="e180501030@stud.tau.edu.tr"
mail = SMTP("smtp.gmail.com",587,timeout=10)
mail.ehlo()
mail.starttls()
mail.login(mymail, password)



cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(3,640)
cap.set(4,480)
font = cv2.FONT_HERSHEY_COMPLEX
outputlist = []
        

df = pd.read_excel(r'C:\Users\z004ca6a\qrcodescanner\validation.xlsx')

today = date.today()

day=today.strftime("%Y-%m-%d")

#print(day)

def extract_order_date(myData):
            
    start_index = myData.find("Order Date:")  # "Order Date:" nin index değerini bulur.
    date_string = myData[start_index + len("Order Date:") : start_index + len("Order Date:") + 10]  # tarih bilgisini string olarak alır.
    return date_string




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

            # Split MyData For Getting Some Spesific Info
           
            order_date = extract_order_date(myData)
            
            start = "Serial Number:"
            end=" Order Date"

            
            p_serialnumber=myData.split(start)[1].split(end)[0]

           
        
            p_date = datetime.strptime(order_date,"%d-%m-%Y").date()
        
        
            difference = p_date - today # calculation of left times for order
            dif_in_day= difference.total_seconds()

            dif_in_day=dif_in_day  * 1000000  
            int_dif=int(dif_in_day)

            dif=int_dif/86400000000
            #print(dif)
                    
            if myData not in outputlist :
                if center[0] < 320 and center[1] > 240 and "Sensitive" in myData  :
                    outputlist.append(myData)

                    print( "Info for ", myData, "Ihr Produkt ist sensitiv, bitte stellen Sie es in ein sicheres Regal.")
                    message ="Info für ", myData, "Ihr Produkt ist sensitiv, bitte stellen Sie es in ein sicheres Regal. "
                    content = "Subject: {0} \n\n {1}".format(subject,message)
                    mail.sendmail(mymail, sendTo, content.encode("utf-8"))
                    if   dif < 8 :
                        ShortTime = "Der Liefertermin des Produkts",p_serialnumber," naht, stellen Sie es auf das Regal am Ausgang" 
                        content = "Subject: {0} \n\n {1}".format(subject,ShortTime)
                        mail.sendmail(mymail, sendTo, content.encode("utf-8"))
                    
                

                elif center[0] > 320 and center[1] > 240 and "Sensitive" in myData  :
                    outputlist.append(myData)

                    print( "Info for ", myData, "Ihr Produkt ist sensitiv, bitte stellen Sie es in ein sicheres Regal.")  
                    message = "Info for ", myData, "Ihr Produkt ist sensitiv, bitte stellen Sie es in ein sicheres Regal."
                    content = "Subject: {0} \n\n {1}".format(subject,message)
                    mail.sendmail(mymail, sendTo, content.encode("utf-8"))
                    if   dif < 8 :
                        ShortTime = "Der Liefertermin des Produkts",p_serialnumber," naht, stellen Sie es auf das Regal am Ausgang" 
                        content = "Subject: {0} \n\n {1}".format(subject,ShortTime)
                        mail.sendmail(mymail, sendTo, content.encode("utf-8"))
                    
                
                    break
                break



            #Messages On Stream
            pts2= barcode.rect
            cv2.putText(grayscale,Validation,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
            0.9,Color,2)
        

            # Add new Output to list and delete duplicates
            
            outputlist=list(dict.fromkeys(outputlist)) #delete duplicates from a list
            json_output = json.dumps(outputlist)
            #print(json_output)


            #Find Total Numbers of QR Codes
            productsnumber = len(outputlist) 
            json_totalnum = json.dumps(productsnumber)


            #Firebase Connection
           # send_to_firebase = fb_app.patch("https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/",{"/QR Code/Outputs" : json_output})
            #send_to_firebase_totalnum = fb_app.patch("https://mec427inventorymanagement-default-rtdb.europe-west1.firebasedatabase.app/",{"/QR Code/Total Number ":json_totalnum})
        
        

        cv2.imshow('Result',grayscale)
        cv2.waitKey(30)
        

    

   










