import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
import math
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist  
import numpy as np 
import cv2
import time



class Scanner(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        #self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)
        #self.color = self.create_client(SetPen, 'turtle1/set_pen')
        self.subscription = self.create_subscription(
        	Image,
        	'/camera/image_raw',
        	self.camera_inputt,
            qos_profile_sensor_data,
            )
    
    detector = cv2.QRCodeDetector()
    
    def camera_inputt(self, message: Image):
        data = np.array(message.data).reshape(message.height, -1, 3)

        qr_text,bbox,straight_qrcode = self.detector.detectAndDecode(data)  
        
        self.get_logger().info(qr_text)

        cv2.imshow('image', data)

        cv2.waitKey(20)


    def timer_callback(self, msg):
        self.turtle_square(msg.sidelength, msg.cw)


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