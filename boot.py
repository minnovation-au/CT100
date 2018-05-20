################## Start setup (EDIT START HERE)

#SITE = 'SRCL'
#key = b'alphaxencryptkeysjtwbutfdchdlcec' # 256 bit (32 bytes) key

################## End setup (EDIT END HERE)

#import socket, os, pycom, crypto, socket, gc
#from machine import SD, WDT
#from crypto import AES

#iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)

#gc.enable()
#wdt = WDT(timeout=30000)

#pycom.heartbeat(False)
#pycom.rgbled(0x007f00) # Turn on Green LED

################# WLAN ###################
# Turn off WiFi to save power
from network import WLAN
w = WLAN()
w.deinit()

################# SIGFOX ###################
#from network import Sigfox
#sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
#ss = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
#ss.setblocking(True)

################# LORA #####################
#from network import LoRa
#lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915)
#sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#sl.setblocking(False)

sd = SD()

try:
  os.mount(sd, '/sd')
except:
  pass
