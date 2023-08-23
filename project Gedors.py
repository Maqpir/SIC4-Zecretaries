from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import pyrebase
import subprocess
import requests

#tele
TOKEN = '6112676569:AAFb7cGIHMoBOrcONRBCUuSHsjOGKlTUrXk'
chat_id = 801404111   #chat id pengguna
image_name = os.getcwd() + "/" + "img.jpg"
list_chat_id = ["801404111"]

GPIO.setmode(GPIO.BCM)
GPIO.setup (23, GPIO.IN) #set pin sensor sentuh

def kirim_foto(nama_file):
    for chat_id in list_chat_id:
        image = open(nama_file,'rb')
        #print(chat_id)
        url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'   #query  
        resp = requests.post(url, files={'photo':image})

        #res = requests.post(url , json=payload)
        print(resp.status_code)
        if int(resp.status_code) == 200:
            print("succes send image")

#set firebase
firebaseConfig = {
    'apiKey': "AIzaSyCi0lpv85pke7hrZl9_2nTQao0aSWP_eqo",
    'authDomain': "cobalagi-745f2.firebaseapp.com",
    'databaseURL': "https://cobalagi-745f2-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "cobalagi-745f2",
    'storageBucket': "cobalagi-745f2.appspot.com",
    'messagingSenderId': "245927400129",
    'appId': "1:245927400129:web:557f3402a438c4d031fa40",
    'measurementId': "G-8KS7FD38MS"

}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def tosen() :
    if GPIO.input(23) == 1 :#isipin
        print ("ada orang")
        pirsensor = 1
        suara (c)
        AmbilGambar()

    elif GPIO.input (23) == 0 : #isipin
        print ("tidak ada orang")
        pirsensor = 0

    return tosen

def suara(inputcommand):
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output

def AmbilGambar () :
    print("Ambil Gambar!")
    nama_file = "img.jpg"
    #os.remove(nama_file)
    #print("File Removed")
    camera = PiCamera()
    time.sleep(2)
    camera.resolution = (1600,1600)
    camera.vflip = True
    camera.contrast = 10
    camera.capture(nama_file)
    storage.child(nama_file).put(nama_file)
    kirim_foto(nama_file)
    print(nama_file)
    print("Image sent")
    camera.close()

while True :
    a = 'cheese.'
    c = 'espeak -ven+f4 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % a
    tosen()
    
    time.sleep(1)
    