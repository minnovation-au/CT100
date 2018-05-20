################## Start setup (EDIT START HERE)

SITE = 'SRCL'
key = b'alphaxencryptkeysjtwbutfdchdlcec' # 256 bit (32 bytes) key

################## End setup (EDIT END HERE)

import socket, os, pycom, crypto, socket, gc, machine
from machine import SD, WDT
from network import LoRa, WLAN
from crypto import AES

print(machine.wake_reason())

iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)

gc.enable()
wdt = WDT(timeout=4000000)

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

# Turn off WiFi to save power
w = WLAN()
w.deinit()

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, power_mode=LoRa.TX_ONLY)
sl = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

import machine, utime, ubinascii, pycom
from machine import deepsleep, Pin, Timer

chrono = Timer.Chrono()
chrono.start()

pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

def aggregate():
    try:
        pycom.nvs_set('val', int(pycom.nvs_get('val'))+1)
    except:
        pycom.nvs_set('val', 0)
    print('Deepsleep Remaining: '+str(machine.remaining_sleep_time()))
    print('New Aggregate: '+str(pycom.nvs_get('val')))
    print('Current Message ID: '+str(pycom.nvs_get('msgID')))

def ammend_to_file():
    try:
        f = open('/flash/log.txt', 'r')
        lines = f.readlines()
        f.close()
        lines=lines[1:]
        print(lines[-20:-1])
        f = open('/flash/log.txt', 'w')
        for a in range (0,999):
            try:
                f.write(lines[a])
            except:
                f.write('\n')
        f.close()
    except:
        pass
    f = open('/flash/log.txt', 'a')
    f.write(str(pycom.nvs_get('msgID')))
    f.write(',')
    f.write(str(pycom.nvs_get('val')))
    f.write('\n')
    f.close()

def mac():
    mac=ubinascii.hexlify(machine.unique_id(),':').decode()
    mac=mac.replace(":","")
    return(mac)
print(mac())

def encrypt(send_pkg):
    cipher = AES(key, AES.MODE_CFB, iv)
    send_pkg = iv + cipher.encrypt(send_pkg)
    return(send_pkg)

def decrypt(recv_pkg):
    cipher = AES(key, AES.MODE_CFB, recv_pkg[:16]) # on the decryption side
    recv_pkg = cipher.decrypt(recv_pkg[16:])
    return(recv_pkg)

def LoRaSend(val):
    sl.setblocking(True)
    sl.send(encrypt(SITE+mac()+'&'+val)) # Send on LoRa Network & wait Reply
    sl.setblocking(False)
    #chrono.reset()
    #recv_pkg=''
    #while (recv_pkg != mac()):
        #recv_pkg = sl.recv(48)
        #if (len(recv_pkg) > 2):
            #recv_pkg = decrypt(recv_pkg).decode('utf-8')
        #if (chrono.read_ms() > 2000):
            #print('Packet Dropped')
            #machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
            #machine.deepsleep(600000)
            #return
    #print('Send Success')
    ammend_to_file()
    pycom.nvs_set('val', 0)
    try:
        pycom.nvs_set('msgID', int(pycom.nvs_get('msgID'))+1)
    except:
        pycom.nvs_set('msgID', 0)

def paused():
    while (pin() == 1):
        utime.sleep_ms(100)

pycom.rgbled(0) # Turn OFF LED

if machine.wake_reason()[0] == 1:
    aggregate()
    print('Aggregate MSGID: '+str(pycom.nvs_get('msgID'))+'   Aggregate Value: '+str(pycom.nvs_get('val')))
    paused()
    wdt.feed()
    machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
    machine.deepsleep(machine.remaining_sleep_time())
else:
    print('Send: {"val":'+str(pycom.nvs_get('val'))+',"msgID":'+str(pycom.nvs_get('msgID'))+'}')
    LoRaSend('{"val":'+str(pycom.nvs_get('val'))+',"msgID":'+str(pycom.nvs_get('msgID'))+'}')
    wdt.feed()
    machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
    machine.deepsleep(3600000)
