import serial
import threading
import time
import roslib
import rospy
from std_msgs.msg import String

comPort = "/dev/ttyUSB0"

def TransmitThread():
  while comPort:
    for n in range(ord("A"),ord("Z")+1):
      if comPort:
        sub = rospy.Subscriber('/teleop_turtle', String)
        comPort.write(chr(n))
        time.sleep(1)

def ReceiveThread():
  while comPort:
    if comPort.inWaiting() > 0:
      c = comPort.read(2)
      rospy.loginfo(c)
      pub.publish(String(c))
      rospy.sleep(1.0)
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
  pub = rospy.Publisher('chatter', String)
  rospy.init_node('talker')
  LoopbackTest("/dev/ttyUSB0")

