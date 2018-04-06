import machine, utime, ubinascii, socket, pycom
from machine import deepsleep, Pin, Timer
from network import LoRa

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)
chrono = Timer.Chrono()
chrono.start()

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, public=False)
sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
utime.sleep_ms(100)

def mac():
    mac=ubinascii.hexlify(machine.unique_id(),':').decode()
    mac=mac.replace(":","")
    return(mac)

def LoRaSend(y,val):
    sl.setblocking(True)
    sl.send(mac()+y+val) # Send on LoRa Network & wait Reply
    sl.setblocking(False)
    chrono.reset()
    while (sl.recv(13).decode('utf-8') != mac()+y):
        if (chrono.read() > 10):
            print('Resubmit Packet')
            pycom.rgbled(0x7f0000) # Turn on Red LED
            sl.setblocking(True)
            sl.send(mac()+y+val)
            sl.setblocking(False)
            chrono.reset()
LoRaSend('1','{"val":1}')

while (pin() == 1):
    utime.sleep_ms(1000)

pycom.rgbled(0) # Turn OFF LED
machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
machine.deepsleep()
