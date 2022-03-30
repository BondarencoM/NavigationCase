from threading import Thread
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from green_interfaces.srv import Scan
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

import time

class Controller(Node):

	def __init__(self):
		super().__init__('green_turtle_controller')
		self._action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
		self.scaner = self.create_subscription(String, '/scans', self.scan_received, 10)
		self.srv = self.create_service(Scan, '/start', self.send_goal)

		self.get_logger().info("wtf")

	def scan_received(self, msg):
		self.last_qr = msg.data

	def send_goal(self, req, response):
		goal_msg = NavigateToPose.Goal()

		pose = PoseStamped()
		pose.pose.position.x = -7.0
		pose.pose.position.y = -4.5
		pose.pose.position.z = 0.0
		
		goal_msg.pose = pose

		self.get_logger().info("Before waiting")
		self._action_client.wait_for_server()
		self.get_logger().info("After waiting")

		self.movement = self._action_client.send_goal_async(goal_msg)

		self.get_logger().info(f"Scanning")

		while self.last_qr != "0":
			self.get_logger().info("wait for qr")
			
		return response

def main(args=None):
	rclpy.init(args=args)

	service = Controller()
	rclpy.spin(service)

if __name__ == '__main__':
    main()
