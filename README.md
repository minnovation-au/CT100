# CT100

Smart CT Firmware for Landfill Counter.

To be used with Pycom LoPy4 chipset in AlphaX CT range of devices.
Watches for a High Signal on Pin 10, sends a signal via LoRa
then goes into power save mode for use on Solar Powered installations.


#V1.1
LoRa reply no longer waits with Delay. Instead uses Chrono() to
Set wait period. When Chrono() is greater then 10 seconds it resends
the original message.
