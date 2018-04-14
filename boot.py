from network import LoRa, WLAN
from machine import SD
import socket, os

sd = SD()

try:
  os.mount(sd, '/sd')
except:
  pass

# Turn off WiFi to save power
w = WLAN()
w.deinit()

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, public=False)
sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
