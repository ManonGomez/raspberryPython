import RPi.GPIO as GPIO
import time
from pi74HC595 import pi74HC595
from ADCDevice import *
import random

adc = ADCDevice() 
VCC = 5
R_DIV = 10000

GPIO.setwarnings(False)                       
GPIO.setmode (GPIO.BOARD)

shift_register = pi74HC595()

pinNine = 38
pinTen = 40
GPIO.setup(pinNine, GPIO.OUT)            
GPIO.setup(pinTen, GPIO.OUT)

DS: int = 29 
ST: int = 31
SH: int = 33

pins=[11, 12, 13]


def setup():
    global adc
    if(adc.detectI2C(0x48)): 
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)):
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
        
    global pwmRed, pwmGreen, pwmBlue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(pins, GPIO.HIGH)
    pwmRed = GPIO.PWM(pins[0], 2000)
    pwmGreen = GPIO.PWM(pins[1], 2000)
    pwmBlue = GPIO.PWM(pins[2], 2000)
    pwmRed.start(0)
    pwmGreen.start(0)
    pwmBlue.start(0)
         
def loop():
     while True:
        r=random.randint(0,100)
        g=random.randint(0,100)
        b=random.randint(0,100)
        setColor(r,g,b)
        print('r=%d, g=%d, b=%d' %(r, g, b))
        time.sleep(1)
        fsrADC = adc.analogRead(1)
        fsrV = fsrADC * VCC / 255.0   
        if fsrV <= 0.37  :
            shift_register.set_by_list([0, 1, 1, 1, 1, 1, 1, 1])
            print("700 ml ou plus")
        elif 0.38 <= fsrV <= 0.43 :
            shift_register.set_by_list([0, 0, 1, 1, 1, 1, 1, 1])
            print("600 ml")
        elif 0.44 <= fsrV <= 0.47 :
            shift_register.set_by_list([0, 0, 0, 1, 1, 1, 1, 1])
            print("500 ml")
        else:
            print("...")
        time.sleep(0.2)    
    
    

def setColor(r_val, g_val, b_val):
    pwmRed.ChangeDutyCycle(r_val)
    pwmGreen.ChangeDutyCycle(g_val)
    pwmBlue.ChangeDutyCycle(b_val)

def clean():
    shift_register.clear()
    GPIO.output(pinNine, GPIO.LOW)
    GPIO.output(pinTen, GPIO.LOW)
         
def destroy():
    adc.close()
    pwmRed.stop()
    pwmGreen.stop()
    pwmBlue.stop()
    GPIO.cleanup()
     
if __name__ == '__main__': 
    print ('Program is starting ... ')
    try:
        clean()
        setup()
        loop()
    except KeyboardInterrupt: 
        clean()
        destroy()