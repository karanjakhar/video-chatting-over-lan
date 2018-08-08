#####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ####KJ#####
#Karan Jakhar#

import cv2,io,numpy
from PIL import Image
import socket
import pyaudio
cap=cv2.VideoCapture(0)

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,
              channels=1,rate=44100,
              input=True,
              output=True,
              frames_per_buffer=20*1024
              )
def audio_send(client):
        data=stream.read(20*1024)
        client.send(data)
def audio_rec(client):
        data=client.recv(20*1024)
        stream.write(data)
def vreceive(sock):
        totrec=0  
        metarec=0
        
        msgArray = bytearray()
        metaArray = []
        #audio_rec(sock)
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

        #audio_send(sock)
        sent = sock.send((lengthstr).encode())
           
        
        
        while totalsent < length :
            sent = sock.send(framestring[totalsent:])
            
            totalsent += sent

def mshow(im_b):
    p=io.BytesIO(im_b)
    pi=Image.open(p)
     
    img = cv2.cvtColor(numpy.array(pi), cv2.COLOR_RGB2BGR)
    cv2.imshow('Me',img)
    cv2.waitKey(1)

def show(im_b):
    p=io.BytesIO(im_b)
    pi=Image.open(p)
    
    img = cv2.cvtColor(numpy.array(pi),cv2.COLOR_RGB2BGR)
   
    cv2.imshow('Friend',img)
    cv2.waitKey(1)  
       

def send(client):
    
    ret,img=cap.read()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    pimg=Image.fromarray(img)
    b=io.BytesIO()
    pimg.save(b,'jpeg')
    im_b=b.getvalue()
    mshow(im_b)
    
    
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
   audio_send(s)
   audio_rec(s)
   #send(s)
   #vreceive(s)
                

