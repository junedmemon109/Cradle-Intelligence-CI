import grovepi

# Connect the microphone to analog port A2
mic = 2

def get_sound_intensity():
    # Read the sound intensity from the microphone
    sound = grovepi.analogRead(mic)

    # Return the sound intensity as a value between 0 and 1023
    return sound

