##################################
### DO NOT EDIT THIS FILE      ###
###                            ###
### CT100 main.py V0.2         ###
### Created By Simon Maselli   ###
### 24 July 2017               ###
###                            ###
### Copyright Minnovation 2017 ###
##################################

import socket, pycom, crypto, gc, machine, utime, ubinascii, ustruct, configs, ch1
from machine import SD, WDT, deepsleep, Pin, Timer
from network import LoRa, WLAN
from crypto import AES

### Turn off LED & Wifi to save power
w = WLAN()
w.deinit() ##Switch Off WLAN
pycom.heartbeat(False)

iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)
gc.enable()
wdt = WDT(timeout=10000)

### Get Device UniqueID
def mac():
    mac=ubinascii.hexlify(machine.unique_id(),':').decode()
    mac=mac.replace(":","")
    return(mac)
print(mac())

### Measure Battery Voltage (only called if battery powered)
def getVoltage():
    volts = 0
    adc = machine.ADC()
    volt = adc.channel(pin='P13')
    for i in range (0,999):
        volts += volt()
    volts = round(volts/i*(1100/4095)/(1026/4200)/1000,3)
    print("Voltage: "+str(volts)+" VDC")
    return(volts)

### Indicate that system is ok and data sent
def indicate():
    ind = machine.Pin('P21', mode=machine.Pin.OUT)
    ind.value(1)
    pycom.rgbled(0x00007f) # Turn on Blue LED
    utime.sleep_ms(1200)
    ind.value(0)
    pycom.rgbled(0) # Turn on Blue LED

### Encrypt data function to send via LPWAN
def encrypt(send_pkg):
    cipher = AES(configs.key, AES.MODE_CFB, iv)
    send_pkg = iv + cipher.encrypt(send_pkg)
    return(send_pkg)

### Send data via LPWAN
def LoRaSend(string):
    sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sl.setblocking(True)
    sl.send(encrypt(configs.SITE+mac()+'&'+string)) # Send on LoRa Network
    sl.setblocking(False)
    print('Sent: '+string)

### Establish Connection and Prepare to Send Package
lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, power_mode=LoRa.TX_ONLY)
string = '{"val":'+str(ch1.getData())+',"volt":'+str(getVoltage())+',"msgID":'+str(lora.stats()[8])+'}'
LoRaSend(string)
lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, power_mode=LoRa.SLEEP)
indicate() #Data Sent Successfully

### Cleanup and Enter Hibernation
print('Entering Hibernation')
wdt.feed()
wdt = WDT(timeout=3610000)
gc.collect()
machine.deepsleep(3600000)