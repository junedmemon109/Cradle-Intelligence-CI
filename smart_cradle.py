import time
import threading
from temperature_humidity import get_temperature, get_humidity
from webcam import start_webcam
from sound_intensity import get_sound_intensity
import RPi.GPIO as GPIO

# Set up the servo motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 50)
servo.start(0)

def run_temperature_humidity():
    try:
        while True:
            temp = get_temperature()
            hum = get_humidity()
            print(f'Temp: {temp} C, Hum: {hum}%')
            time.sleep(5)
    except:
        print('Exception in DHT11 Temperature and Humidity Sensor Module!')

def run_webcam():
    start_webcam()

def run_sound_intensity():
    try:
        # Initialize the timer
        swing_timer = None
        
        while True:
            sound = get_sound_intensity()
            print(f'Sound Intensity: {sound}')

            if sound > 700 and sound < 2000:
                print('Crying detected! Starting swing...')
                
                # Start the swing
                start_swing()
                
                # Cancel the previous timer (if any)
                if swing_timer:
                    swing_timer.cancel()
                
                # Create a new timer to stop the swing after 5 seconds
                swing_timer = threading.Timer(5.0, stop_swing)
                swing_timer.start()
            
            # If sound goes below threshold, stop the swing and cancel the timer
            if sound <= 700 and swing_timer:
                print('Crying stopped. Stopping swing...')
                swing_timer.cancel()
                stop_swing()
                
            time.sleep(0.1)
    except:
        print('Exception in sound sensor module!')
                

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
    sound_thread.start()
    temperature_thread.start()
    
    

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
