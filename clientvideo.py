#####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ#####
#Karan Jakhar#

import cv2,io,numpy
from PIL import Image
import socket
cap=cv2.VideoCapture(0)
def vreceive(sock):
        totrec=0  
        metarec=0
        
        msgArray = bytearray()
        metaArray = []
        
        c = sock.recv(8)
        c=c.decode()
         
        length=int(c)

        while totrec<length :
            chunk = sock.recv(length-totrec)
            msgArray.extend(chunk)
            totrec += len(chunk)

             
        show(msgArray)
             
        

         
 

def vsend(framestring,sock):
        totalsent = 0
        metasent = 0
        length =len(framestring)
        lengthstr=str(length).zfill(8)

        
        sent = sock.send((lengthstr).encode())
           
        
        
        while totalsent < length :
            sent = sock.send(framestring[totalsent:])
            
            totalsent += sent

def show(im_b):
    p=io.BytesIO(im_b)
    pi=Image.open(p)
    
    img = cv2.cvtColor(numpy.array(pi),cv2.COLOR_RGB2BGR)
   
    cv2.imshow('kj',img)
    cv2.waitKey(1)  
       

def send(client):
    
    ret,img=cap.read()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pimg=Image.fromarray(img)
    b=io.BytesIO()
    pimg.save(b,'jpeg')
    im_b=b.getvalue()
     
    
    
    vsend(im_b,client)
 

def inet_connect(ip,serverport):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,serverport))
    print("Connection Established with :",ip,":",serverport)
    print("Wait...")
    return s
 
 
serverport=int(input("Enter Port:"))
ip=input("Enter IP:")
s=inet_connect(ip,serverport)
while True:
   
   send(s)
   vreceive(s)
                

