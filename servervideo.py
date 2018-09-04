#####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ#####
#Karan Jakhar#

import cv2,io,numpy
from PIL import Image
import socket
cap=cv2.VideoCapture(0)

#first receiving size of the frame or data to receive and the data
def vreceive(sock):
        totrec=0
         
        msgArray = bytearray()
        
         
        c= sock.recv(8)
        c=c.decode()
            
        length=int(c)

        while totrec<length :
            chunk = sock.recv(length - totrec)
            msgArray.extend(chunk)
            totrec+=len(chunk)

        show(msgArray)
             
#first sending the size of the frame and then the frame
def vsend(framestring,sock):
        totalsent = 0
        metasent = 0
        length =len(framestring)
        lengthstr=str(length).zfill(8) 

       
        sent = sock.send((lengthstr).encode())
          
        
        
        while totalsent < length:
          
            sent = sock.send(framestring[totalsent:])
            totalsent+=sent

 #showing send frames(images)
def mshow(im_b):
    p=io.BytesIO(im_b)
    pi=Image.open(p)
     
    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)
    cv2.imshow('Me',img)
    cv2.waitKey(1)    

#showing received frames(images) 
def show(im_b):
    p=io.BytesIO(im_b)
    pi=Image.open(p)
    
    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)
    cv2.imshow('Friend',img)
    cv2.waitKey(1)  
       
#capturing and sending frames(images)
def send(client):
    ret,img=cap.read()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pimg=Image.fromarray(img)
    b=io.BytesIO()
    pimg.save(b,'jpeg')
    im_b=b.getvalue()
    mshow(im_b)
    vsend(im_b,client)

 #creating server and listening on port provided 
def inet_connect(serverport):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('',serverport))
        s.listen(5)
        print("Wait...")
        (client,(ip,port))=s.accept()
        print("Connection Established with :",ip,":",port)
        return client
 

     
 

#taking port to create server 
serverport=int(input("Enter port :")) 
client=inet_connect(serverport)

#regularly sends and receives data
while True:
        
         
       vreceive(client)
       send(client)
    
    
