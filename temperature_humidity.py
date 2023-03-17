import grovepi

# Connect the DHT11 Temperature and Humidity sensor to digital port D7
sensor = 7

def get_temperature():
    # Read the temperature from the sensor
    [temp, hum] = grovepi.dht(sensor, 0)
    
    # Return the temperature in Celsius
    return temp

def get_humidity():
    # Read the humidity from the sensor
    [temp, hum] = grovepi.dht(sensor, 0)
    
    # Return the humidity as a percentage
    return hum
