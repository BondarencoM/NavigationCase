import sys
from time import sleep
import rclpy as rospy
from rclpy.node import Node
import rclpy.qos as QOS
from rclpy.qos import QoSProfile
# from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

from threading import Thread

# from PIL import Image, ImageTk
# import tkinter as tk

from inputs import devices, Keyboard

class image_converter(Node):

    def __init__(self):
        super().__init__('VideoNode')
        self.get_logger().info("Created node")
        self.bridge = CvBridge()
        self.cv_image = np.zeros((200,200,3))
        self.qr = cv2.QRCodeDetector()
        
        self.image_sub = self.create_subscription(Image, "/camera/image_raw", self.callback, QoSProfile(reliability=QOS.ReliabilityPolicy.BEST_EFFORT, durability=QOS.DurabilityPolicy.VOLATILE, history=QOS.HistoryPolicy.SYSTEM_DEFAULT))
        # self.vel_pub = self.create_publisher(Twist, "/cmd_vel", QoSProfile(reliability=QOS.ReliabilityPolicy.RELIABLE, durability=QOS.DurabilityPolicy.VOLATILE, history=QOS.HistoryPolicy.SYSTEM_DEFAULT))

    def callback(self,data):
        try:
            # self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.cv_image = cv2.resize(self.bridge.imgmsg_to_cv2(data, "bgr8"), None, fx=0.8, fy=0.8)
            data,_,_ = self.qr.detectAndDecode(self.cv_image)
            if len(data)>0:
                self.get_logger().info(f"Decoded Data : {data}")
        except CvBridgeError as e:
            self.get_logger().error(e)

        # cv2.imshow("POV", self.cv_image)
        # cv2.imshow("Image window", self.cv_image)
        # cv2.waitKey(3)

def video(node):
    while True:
        cv2.imshow("Image window", node.cv_image)
        cv2.waitKey(5)

def main(args = None):
    rospy.init()
    ic = image_converter()

    # video_shower = VideoShow(ic.cv_image, ic).start()

    Thread(target=rospy.spin, args=[ic]).start()
    vidthread = Thread(target=video, args=[ic], daemon=True).start()

    cmd_vel = ic.create_publisher(Twist, "/cmd_vel", QoSProfile(reliability=QOS.ReliabilityPolicy.RELIABLE, durability=QOS.DurabilityPolicy.VOLATILE, history=QOS.HistoryPolicy.SYSTEM_DEFAULT))
    speed = Twist()
    # win= tk.Tk()

    # label = tk.Label(win)
    # label.grid(row=0, column=0)

    kb:Keyboard = devices.keyboards[0]

    # Define function to show frame
    def show_frames():
        # cv2.imshow("POV", ic.cv_image)
        # cv2.waitKey(3)

        # # Get the latest frame and convert into Image
        # cv2image= ic.cv_image
        # img = Image.fromarray(cv2image)

        # # Convert image to PhotoImage
        # imgtk = ImageTk.PhotoImage(image = img)
        # label.imgtk = imgtk
        # label.configure(image=imgtk)

        events = kb.read()
        if events:
            for event in events:
                if event.ev_type == 'Key' and event.state != 2:
                    ic.get_logger().info(f"Key event: {event.ev_type}, {event.code}, {event.state}")
                    if event.code == 'KEY_ESC' and event.state == 1:
                        return 1
                    elif event.state == 1:
                        if event.code == 'KEY_UP':
                            speed.linear.x = 0.5
                        if event.code == 'KEY_DOWN':
                            speed.linear.x = -0.5
                        if event.code == 'KEY_LEFT':
                            speed.angular.z = 0.5
                        if event.code == 'KEY_RIGHT':
                            speed.angular.z = -0.5
                    elif event.state == 0:
                        if event.code == 'KEY_UP':
                            speed.linear.x = 0.0
                        if event.code == 'KEY_DOWN':
                            speed.linear.x = 0.0
                        if event.code == 'KEY_LEFT':
                            speed.angular.z = 0.0
                        if event.code == 'KEY_RIGHT':
                            speed.angular.z = 0.0

        # Repeat after an interval to capture continiously
        cmd_vel.publish(speed)
        # label.after(20, show_frames)
        
    done = False
    while not done:
        done = show_frames()
    
    
    cv2.destroyAllWindows()
    ic.destroy_node()
    rospy.shutdown()

if __name__ == '__main__':
        main(sys.argv)