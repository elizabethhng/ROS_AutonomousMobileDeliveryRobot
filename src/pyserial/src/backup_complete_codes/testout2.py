import serial
import threading
import time

comPort = "/dev/ttyUSB0"

def TransmitThread():
  while comPort:
    for n in range(ord("A"),ord("Z")+1):
      if comPort:
        comPort.write(chr(n))
        time.sleep(1)

def ReceiveThread():
  while comPort:
    if comPort.inWaiting() > 0:
      c = comPort.read(1)
      print( c )
    else:
      time.sleep(0.1)

def LoopbackTest(comPortName):
  global comPort

  comPort = serial.Serial \
            (
              port=comPortName,
              baudrate=9600,
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              bytesize=serial.EIGHTBITS
            )

  threading.Thread(target=TransmitThread).start()
  threading.Thread(target=ReceiveThread).start()

  try:
    while True:
      time.sleep(1)
  except:
    comPort = None

if __name__ == "__main__":
  LoopbackTest("/dev/ttyUSB0")

