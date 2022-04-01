from threading import Thread
import rclpy
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node
from rclpy.action import ActionClient
from green_interfaces.srv import Scan
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Header

import time

coords = [
	("0", (-6.2, -4.6, 0.0),(0.0, 0.9)),
	("5", (0.8, -3.0, 0.0), (0.7, 0.7)),
	("3", (0.8, -4.7, 0.0), (0.0, 1.0)),
	("7", (4.3, -7.4, 0.0), (-0.6, 0.7)),
	("8", (8.0, -8.0, 0.0),  (0.0, 0.9)),
	("4", (3.1, 4.8, 0.0),  (1.0, 0.0)),
	("2", (2.3, 0.7, 0.0),  (0.0, 0.9)),
	("1", (-0.8, 2.6, 0.0), (0.0, 0.9)),
	("6", (-5.9, 4.9, 0.0), (-0.9, 0.0)),
	("9", (4.3, 7.9, 0.0),  (0.6, 0.7)),
	("10", (9.8, -2.7, 0.0),(0.0, 0.9)),
]

class Controller(Node):

	last_qr = None

	def __init__(self):
		super().__init__('green_turtle_controller')

		self.navigation = self.create_publisher(PoseStamped, '/goal_pose', qos_profile_sensor_data)
		self.scaner = self.create_subscription(String, '/scans', self.scan_received, 10)

	def scan_received(self, msg):
		self.get_logger().info(f"QR data= {msg.data}")
		self.last_qr = msg.data

	def start_navigation(self, coord):
		# Transform coordiates from tuple to PoseStamped
		_, pos, orientation = coord
		pose = PoseStamped()
		pose.pose.position.x, pose.pose.position.y, _ = pos
		pose.pose.orientation.z, pose.pose.orientation.w = orientation
		pose.header = Header()
		pose.header.frame_id = "map"
		self.get_logger().info(f"Sending navigation goal for pos {pose}")

		# Send the navigation multiple times. 
		# This helps assure that the goal is actually
		# received by the avigation stack.
		self.navigation.publish(pose)
		time.sleep(3)
		self.navigation.publish(pose)
		time.sleep(3)
		self.navigation.publish(pose)

	def check_qr(self, expected):
		self.get_logger().info(f"checking last_qr={self.last_qr} vs {expected}")
		return self.last_qr == expected
			
def main(args=None):
	rclpy.init(args=args)
	service = Controller()

	# for every QR code
	for coord in coords:

		# move to that QR code
		service.start_navigation(coord)
		
		# wait until the correct QR code is visible
		while not service.check_qr(coord[0]):
			print("waiting")
			rclpy.spin_once(service, timeout_sec=1)
		
		#face the code for 5 seconds
		time.sleep(5)


if __name__ == '__main__':
    main()
