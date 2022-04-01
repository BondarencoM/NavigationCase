import rclpy
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
import math
import time
from std_msgs.msg import String
from green_interfaces.srv import Scan
import numpy as np 
import cv2
import time



class Scanner(Node):

    detector = cv2.QRCodeDetector()

    def __init__(self):
        super().__init__('green_scanner')
        self.subscription = self.create_subscription(
        	Image,
        	'/camera/image_raw',
        	self.camera_input,
            qos_profile_sensor_data,
            )
        self.srv = self.create_publisher(String, '/scans', 10)

    srv:Publisher

    def camera_input(self, message: Image):
        self.get_logger().info("Received camera input")

        # Transforming flat array into shape (height, width, RGB)
        data = np.array(message.data).reshape(message.height, -1, 3)

        # Transforming the image to HSV to increase brightness
        # This helps with some QR codes that are too dark
        hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] += 60
        data = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Try to detect a QR code
        try:
            qr_text,bbox,straight_qrcode = self.detector.detectAndDecode(data)  
        except cv2.error:
            self.get_logger().warn("Something went wrong with cv2")
            qr_text = ""

        # Publish the value of the QR code 
        # or an empty string if no QR code is detected
        s = String()
        s.data = qr_text
        self.srv.publish(s)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = Scanner()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()