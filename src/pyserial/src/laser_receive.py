import serial
import threading
import time
import roslib
import rospy
import struct
from std_msgs.msg import String

comPort = "/dev/ttyUSB0"

def TwistConvertPublish(c):
	print (c)
	pub.publish(c)
	

def ReceiveThread():
	while comPort:
		try:
			if comPort.inWaiting() ==11:
				rospy.loginfo("bytes to read %d", comPort.inWaiting())
				c = comPort.read(11)
				TwistConvertPublish(c)
				rospy.loginfo("Data Receiving %s", c)
				rospy.sleep(0.1)

		except comPort.inWaiting()!=11:
			comPort.flush()
			rospy.loginfo("Port Flushed",comPort.inWaiting)

		

def LoopbackTest(comPortName):
  global comPort

  comPort = serial.Serial \
            (
              port=comPortName,
              baudrate=115200,
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              bytesize=serial.EIGHTBITS
            )

  threading.Thread(target=ReceiveThread).start()

  try:
    while True:
      time.sleep(1)
  except:
    comPort = None

if __name__ == "__main__":
  rospy.init_node('txrx2')
  pub = rospy.Publisher('/laser_colour', String, queue_size=100)
  LoopbackTest(comPort)
  rospy.spin()

