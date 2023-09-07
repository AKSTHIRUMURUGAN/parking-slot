import cv2
import pickle
import cvzone
import numpy as np

#video feed
cap=cv2.VideoCapture("carPark.mp4")

with open('carparkpos','rb')as f:
    posList=pickle.load(f)

width,height=107,48
def checkparkingspace(imgpro):
    spaceCounter=0
    space=0
    for pos in posList:
        x,y=pos


        imgcrop=imgpro[y:y+height,x:x+width]
      #  cv2.imshow(str(x*y),imgcrop)
        count=cv2.countNonZero(imgcrop)

        if count<900:
            color=(0,255,0)
            thickness=5
            spaceCounter+=1
            space+=1
            cvzone.putTextRect(img, f'S:{spaceCounter}', (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
        else:
            color=(0,0,255)
            thickness = 2
            spaceCounter += 1
           # cvzone.putTextRect(img, f'S:{spaceCounter}', (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)




    # cvzone.putTextRect(img, f'S:{}', (x, y + height - 3),scale=1,thickness=2,offset=0,colorR=color)
       # cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
   # cvzone.putTextRect(img, f'Free:{space}/{len(posList)}', (100,50), scale=5, thickness=5, offset=20, colorR=(0,200,0))
    cvzone.putTextRect(img, f'Free:{space}/{len(posList)}', (100, 50), scale=5, thickness=5, offset=20,
                       colorR=(0, 200, 0))
    #cvzone.putTextRect(img, f'S:{1}', (x, y + height - 3),scale=1,thickness=2,offset=0,colorR=color)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)

    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedium=cv2.medianBlur(imgThreshold,5)

    kernel=np.ones((3,3),np.uint8)
    imgdilate=cv2.dilate(imgMedium,kernel,iterations=1)


    checkparkingspace(imgdilate)


    cv2.imshow("Image",img)
#    cv2.imshow("Imageblur",imgBlur)
#   cv2.imshow("ImageThres",imgMedium)



    cv2.waitKey(10)
