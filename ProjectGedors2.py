#Coba update firebase->touch/ultrasonic->camera->kirim firebase&tele

from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import pyrebase
import subprocess
import requests

#set firebase
firebaseConfig = {
  'apiKey': "AIzaSyCGjZf7Bo92OqUn_NbfjOdRsEChVPGpbdE",
  'authDomain': "gedors-790a5.firebaseapp.com",
  'databaseURL': "https://gedors-790a5-default-rtdb.firebaseio.com",
  'projectId': "gedors-790a5",
  'storageBucket': "gedors-790a5.appspot.com",
  #'messagingSenderId': "573141795266",
  #'appId': "1:573141795266:web:82d662cdb02a82d2e8565b",
  #'measurementId': "G-3HYRG104QN"   
}

#tele
TOKEN = '6112676569:AAFb7cGIHMoBOrcONRBCUuSHsjOGKlTUrXk'
chat_id = 801404111   #chat id pengguna
image_name = os.getcwd() + "/" + "img.jpg"
list_chat_id = ["801404111"]

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
db = firebase.database() #set database
#db.child("gedors").update({"nourut":0}) #set 0 no urut
camera = PiCamera () #open camera
time.sleep(2)
trigger = 3
echo = 4

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup (23, GPIO.IN) #pin sensor tosen
GPIO.setup (trigger, GPIO.OUT) #pin trigger SR04
GPIO.setup (echo, GPIO.IN) #pin echo SR04



def Ambil_Gambar(urut):
    print ("ambil gambar")
    nama_file = "img" + str(urut) + ".jpg"
    camera.resolution = (1000, 1000)
    camera.vflip = True
    camera.contrast = 10
    camera.capture (nama_file)
    storage.child(nama_file).put(nama_file) #send storage
    print (nama_file)
    print ("sent !")
    #camera.close()
    
#kirim tele
def send_msg(text):
   token = "6112676569:AAFb7cGIHMoBOrcONRBCUuSHsjOGKlTUrXk"
   chat_id = "801404111"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   print ('tele terkirim')


def tosen(hitung) :
    if GPIO.input(23) == 1 :#sensor high
        tosen = hitung + 1
        Ambil_Gambar(tosen)
        kirim_data(tosen)
    elif GPIO.input (23) == 0 : #sensor low
        tosen = hitung + 0

    return tosen


def suara(inputcommand):
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output


#sensor SR04
def dekat ():
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dekat = (TimeElapsed * 34300) / 2
 
    return dekat
     


def kirim_data(urut):
    db.child("gedors").update({"nourut":urut})



if __name__ == '__main__':
    try:
        while True :
            angka_awal = db.child("gedors").child("nourut").get().val()
            jarak = dekat()
            print ("ready!")
            print (angka_awal)
            a = "Welcome"
            c = 'espeak -ven+f4 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % a
            if jarak < 30 : #jika dibawah 30 cm
                angka_awal = angka_awal+1
                send_msg("Tamu ada di depan")
                suara(c)
                Ambil_Gambar(angka_awal)
                kirim_data(angka_awal)
          
            else :
                angka_awal = angka_awal
                #tosen(angka_awal)
    
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        print("clean up")
        GPIO.cleanup() # cleanup all GPIO 
