import machine
from machine import deepsleep, Pin
import utime, ubinascii, socket, pycom
from network import LoRa

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Green

pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)
data = '0'

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, public=False)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
utime.sleep_ms(100)

loramac = ubinascii.hexlify(lora.mac())

while (data != loramac):

    s.setblocking(True)
    s.send(loramac+b'1'+b'{"val":1}')
    utime.sleep_ms(100)
    # wait for reply message
    s.setblocking(False)
    data = s.recv(64)

while (pin() == 1):
    print("Waiting to Reset")
    utime.sleep_ms(1000)

print("Going to Sleep")
machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
machine.deepsleep()
#utime.sleep_ms(1000)
