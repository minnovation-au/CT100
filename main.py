import machine, utime, ubinascii, socket, pycom, os
from machine import deepsleep, Pin, Timer, SD, RTC
from network import LoRa

rtc = RTC()
#rtc.init((2018, 4, 14, 16, 59, 0, 0, 0))
print(machine.wake_reason()[0])

dateTime = str(utime.gmtime()[0])+"/"+str(utime.gmtime()[1])+"/"+str(utime.gmtime()[2])+" "+str(utime.gmtime()[3])+":00:00"

pycom.heartbeat(False)
pycom.rgbled(0x007f00) # Turn on Green LED

pin = Pin('P10', mode=Pin.IN, pull=Pin.PULL_DOWN)
chrono = Timer.Chrono()
chrono.start()
status=False
lines=""
val=""

def mac():
    mac=ubinascii.hexlify(machine.unique_id(),':').decode()
    mac=mac.replace(":","")
    return(mac)

def LoRaSend(y,val):
    sl.setblocking(True)
    sl.send(mac()+y+val) # Send on LoRa Network & wait Reply
    print(mac()+y+val)
    sl.setblocking(False)
    chrono.reset()
    c=0
    while (sl.recv(13).decode('utf-8') != mac()+y):
        if (chrono.read_ms() > 2000):
            print('Resubmit Packet')
            sl.setblocking(True)
            sl.send(mac()+y+val)
            sl.setblocking(False)
            chrono.reset()
            pycom.rgbled(0x00007f)
            c = c+1
            if (c == 10):
                print('Packet Dropped')
                return(False)
    return(True)

def openLog():
    f = open('/sd/syslog.bin')
    lines = f.readlines()
    f.close()
    return(lines)

print (openLog()[0].split(',')[0])
print (openLog()[0].split(',')[1])
print (openLog())

if openLog()[0].split(',')[0] == dateTime:
  lines = openLog()[1:]
  if machine.wake_reason()[0] == 1:
      val = int(openLog()[0].split(',')[1])+1
  else:
      try:
          val = int(openLog()[0].split(',')[1])
      except:
          val=0
  print(openLog()[0].split(',')[2].strip('\n'))
  if str(openLog()[0].split(',')[2].strip('\n')) == 'False':
      try:
          status = LoRaSend('1','{"val":'+str(openLog()[1].split(',')[1])+',"timestamp":"'+str(openLog()[1].split(',')[0])+'"}')
      except:
          pycom.rgbled(0x007f00)
          status = False
else:
    lines = openLog()[:-1]
    if machine.wake_reason()[0] == 1:
        val = 1
    else:
        val = 0
    status = LoRaSend('1','{"val":'+str(openLog()[1].split(',')[1].strip('\n'))+',"timestamp":"'+str(openLog()[1].split(',')[0])+'"}')

def writeLog(lines,val,status):
    f = open('/sd/syslog.bin','w')
    f.write(str(dateTime))
    f.write(',')
    f.write(str(val))
    f.write(',')
    f.write(str(status))
    f.write('\n')
    for x in range(0,10):
      try:
        f.write(lines[x])
      except:
        f.write('\n')
    f.close()

writeLog(lines,val,status)

#print(LoRaSend('1','{"val":1}'))

b=0
while (pin() == 1):
    if b==30:
        pycom.rgbled(0x00007f)
        utime.sleep_ms(10)
        pycom.rgbled(0)
        b=0
        print('waiting for pressure')
    utime.sleep_ms(100)
    b=b+1


pycom.rgbled(0) # Turn OFF LED
machine.pin_deepsleep_wakeup(pins=['P10'], mode=machine.WAKEUP_ANY_HIGH )
machine.deepsleep(3590000)
