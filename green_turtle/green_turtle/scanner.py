import rclpy
from rclpy.node import Node
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

        self.srv = self.create_service(Scan, 'scan', self.scan_last_message)
    
    def camera_inputt(self, message: Image):
        self.last_message = message

    def scan_last_message(self, request, response: Scan.Response):
        self.get_logger().info("scanning request")
        data = np.array(self.last_message.data).reshape(self.last_message.height, -1, 3)

        qr_text,bbox,straight_qrcode = self.detector.detectAndDecode(data)  
        response.data = qr_text
        self.get_logger().info(f"Detected QR code: {qr_text}")
        return response


    # def navigation(self, qr_text):
    #     for i in range(10):

    #         qr_number = 

    #         goal = PoseStamped()
    #         goal.
    #         goal.header.stamp.sec = i
    #         goal.header.frame_id = 'map'

    #         goal.pose.position.x = 
    #         goal.pose.position.y = 
    #         goal.pose.position.z = 
    #         goal.pose.orientation.w = 

    #         if (qr_text == qr_number):
    #             time.sleep(5)
        






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