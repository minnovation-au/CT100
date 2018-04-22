################## Start setup (EDIT START HERE)

SITE = 'SRCL'
key = b'alphaxencryptkeysjtwbutfdchdlcec' # 256 bit (32 bytes) key

################## End setup (EDIT END HERE)

import socket, os, pycom, crypto, socket, gc
from machine import SD, WDT
from network import LoRa, WLAN
from crypto import AES

iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)

gc.enable()
wdt = WDT(timeout=30000)

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

# Turn off WiFi to save power
w = WLAN()
w.deinit()

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915)
sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

sd = SD()

try:
  os.mount(sd, '/sd')
except:
  pass
