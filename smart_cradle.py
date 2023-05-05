import time
import threading
from temperature_humidity import get_temperature, get_humidity
from webcam import start_webcam
from sound_intensity import get_sound_intensity
import RPi.GPIO as GPIO
import urllib.request as urllib2
import math

myAPI = 'GI7RJTBX7A2FKNGN' 
# URL where we will send the data, Don't change it

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

#import firebase_admin as f
#from firebase_admin import credentials
#from firebase_admin import firestore

# Initialize Firebase Admin SDK with service account credentials
#cred = f.credentials.Certificate('serviceaccount.json')
#f.initialize_app(cred)



import pyrebase

# Initialize Pyrebase with your Firebase project configuration
config = {
      "apiKey": "AIzaSyBN1A2igFG16p0ALEqAspQPAVP4i4px6zc",
      "authDomain": "cradle-intelligence.firebaseapp.com",
      "databaseURL": "https://cradle-intelligence-default-rtdb.asia-southeast1.firebasedatabase.app",
      "storageBucket": "cradle-intelligence.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get the authenticated user's UID
uid = "gKmiSaHtbRNBXd9tVbu0qql0QLq2"

# Create a reference to the user's document in Firestore
db = firebase.database()
#db = firebase.firestore()

# Set up the servo motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 50)
servo.start(0)

temp=None
hum=None
sound=None
cry=None

def run_temperature_humidity():
    try:
        while True:
            global temp
            global hum
            temp = get_temperature()
            hum = get_humidity()
            
            if math.isnan(temp):
                temp = 0

            if math.isnan(hum):
                hum = 0
            
            '''# Sending the data to thingspeak
            conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s' % (temp, hum))
            print(conn.read())
            # Closing the connection
            conn.close()'''
            
            # Update the temperature and humidity fields
            data = {"temp":temp, "hum":hum}
            
            db.child("users").child(uid).update(data)
            #db.child("users").update(data)
       
            print(f'Temp: {temp} C, Hum: {hum}%\n')
            time.sleep(5)
    except:
        print('Exception in DHT11 Sensor')

def run_webcam():
    start_webcam()

def run_sound_intensity():
    try:
        global cry
        # Initialize the timer
        swing_timer = None
        crying = False
        cry=0
        
        data = {"crying":crying}
        db.child("users").child(uid).update(data)
        
        # Update the crying field
        #db.child("users").child(uid).update({
            #"crying": (f'{crying}')
        #})
        
        while True:
            global sound
            sound = get_sound_intensity()
            
            data = {"sound":sound}
            
            db.child("users").child(uid).update(data)
            
            '''# Sending the data to thingspeak
            conn = urllib2.urlopen(baseURL + '&field3=%s' % (sound))
            print(conn.read())
            # Closing the connection
            conn.close()'''
            
            print(f'Sound Intensity: {sound}\n')
    
            # Update the sound field
            #db.child("users").child(uid).update({
                #"sound": (f'{sound}')
            #})
            

            if sound > 300 and sound < 2000:
                print('Crying detected! Starting swing...')
                crying = True
                cry = 1
                
                data = {"crying":crying}
                db.child("users").child(uid).update(data)
            
                
                
                '''# Sending the data to thingspeak
                conn = urllib2.urlopen(baseURL + '&field4=1')
                print(conn.read())
                # Closing the connection
                conn.close()'''
                
                ## Update the crying field
                #db.child("users").child(uid).update({
                    #"crying": (f'{crying}')
                #})
                
                # Start the swing
                start_swing()
                
                # Cancel the previous timer (if any)
                if swing_timer:
                    swing_timer.cancel()
                
                # Create a new timer to stop the swing after 5 seconds
                swing_timer = threading.Timer(5, stop_swing)
                swing_timer.start()
            
            # If sound goes below threshold, stop the swing and cancel the timer
            if sound <= 400 and swing_timer:
                print('Crying stopped. Stopping swing...')
                crying = False
                cry = 0
                
                data = {"crying":crying}
                db.child("users").child(uid).update(data)
            
                
                
                '''# Sending the data to thingspeak
                conn = urllib2.urlopen(baseURL + '&field4=%0')
                print(conn.read())
                # Closing the connection
                conn.close()'''
                
                # Update the crying field
                #db.child("users").child(uid).update({
                    #"crying": (f'{crying}')
                #})
                
                swing_timer.cancel()
                stop_swing()
                
            time.sleep(0.1)
    except:
        print('Exception in Sound Sensor Module')
                

def start_swing():
    # Start swinging the cradle
    servo.ChangeDutyCycle(10)
    time.sleep(0.4)
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.4)
    servo.ChangeDutyCycle(12.5)
    time.sleep(0.4)
    
def stop_swing():
    # Stop swinging the cradle
    servo.ChangeDutyCycle(0)
    
def main():
    
    webcam_thread = threading.Thread(target=run_webcam)
    sound_thread = threading.Thread(target=run_sound_intensity)
    temperature_thread = threading.Thread(target=run_temperature_humidity)

    webcam_thread.start()
    temperature_thread.start()
    sound_thread.start()
    

    while True:
        time.sleep(1)
        # Sending the data to thingspeak
        conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' % (temp, hum, sound, cry))
        print(conn.read())
        # Closing the connection
        conn.close()

if __name__ == '__main__':
    main()


