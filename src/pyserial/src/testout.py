import serial
import threading
import time
import roslib
import rospy
from std_msgs.msg import String

comPort = "/dev/ttyUSB0"

def callback(data):
    rospy.loginfo("Data Transmitting %s", data.data)
    comPort.write(data.data)
################################################

def TransmitThread():
#  while comPort:
      if comPort:        
	rospy.Subscriber("/say_hello", String, callback)


def ReceiveThread():
  while comPort:
    if comPort.inWaiting() > 0:
      c = comPort.read(2)
      rospy.loginfo("Data Receiving %s", c)
      pub.publish(String(c))
      rospy.sleep(1.0)
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
  rospy.init_node('txrx')
  pub = rospy.Publisher('receiving', String, queue_size=10)
  LoopbackTest(comPort)
  rospy.spin()

