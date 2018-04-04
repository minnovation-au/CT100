import machine
from machine import deepsleep, Pin, Timer
import utime, ubinascii, socket, pycom
from network import LoRa

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)
chrono = Timer.Chrono()
chrono.start()
data = '0'

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, public=False)
sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
utime.sleep_ms(100)

loramac = ubinascii.hexlify(lora.mac())

def LoRaSend(y,val):
    sl.setblocking(True)
    sl.send(loramac+str(y)+val) # Send on LoRa Network & wait Reply
    sl.setblocking(False)
    chrono.reset()
    print("Waiting for Reply")
    while (sl.recv(17) != loramac+str(y)):
        if (chrono.read() > 10):
            print('Resubmit Packet')
            pycom.rgbled(0x7f0000) # Turn on Red LED
            sl.setblocking(True)
            sl.send(loramac+str(y)+val)
            sl.setblocking(False)
            chrono.reset()
print("Sending Packet")
LoRaSend(1,'{"val":1}')

while (pin() == 1):
    print("Waiting to Reset")
    utime.sleep_ms(1000)

print("Going to Sleep")
machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
machine.deepsleep()
