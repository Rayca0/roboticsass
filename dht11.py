import time
import board
import adafruit_dht
from pyfirmata import Arduino, util
import csv
from picamera import PiCamera
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO


# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D18, use_pulseio=False)
board=Arduino('/dev/ttyACM0')
led=12

it=util.Iterator(board)
it.start()
board.analog[0].enable_reporting()

#set the GPIO as an output for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH)

#write the header for the csv files outside the while loop to avoid writting header again in the csv every update
header1=['Count:','Humidity:']
header2=['Count:','Temperature:']
header3=['Count:','Soil_moisture:']

with open('/home/pi/Desktop/robotics/Robotics/Humidity_level.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header1)

with open('/home/pi/Desktop/robotics/Robotics/Temperature_change.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header2)
        
with open('/home/pi/Desktop/robotics/Robotics/Soil_moisture_level.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header3)

#set up the threshold for the water pump/activate the replay
threshold=0.25

camera = PiCamera() #define camera

count=0
while True:
    global Moisture
    Moisture=board.analog[0].read() #define moisture as the sensor reading
    if Moisture<threshold: #setup the condition for relay to be activated
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.OUT)
        GPIO.output(17,GPIO.LOW)
        sleep(0.5)
        GPIO.output(17,GPIO.HIGH)

    try:
        temperature_c = dhtDevice.temperature #define temperature as sensor readings
        humidity = dhtDevice.humidity #define humidity as sensor readings
        print("Count: {} Humidity: {}%   Temp: {:.1f} C  Moisture: {}".format(count,humidity,temperature_c, Moisture))
        count+=1 #print to make sure the valid output
        
        
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error         
    
    #updates the sensor readings to the csv files every loop
    data1=[count, humidity]
    data2=[count, temperature_c]
    data3=[count, Moisture]

    with open('/home/pi/Desktop/robotics/Robotics/Humidity_level.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(data1)
    
    with open('/home/pi/Desktop/robotics/Robotics/Temperature_change.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(data2)
        
    with open('/home/pi/Desktop/robotics/Robotics/Soil_moisture_level.csv','a',encoding='UTF8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(data3) 
    
    #pi camera and updates sleeps for 2 hours after one loop otherwise there is too much data to memorise and analyse
    camera.capture('/home/pi/Desktop/image.jpg')
    sleep(7200)
        