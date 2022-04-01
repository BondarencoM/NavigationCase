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
	("0", (-6.2, -4.6, 0.0),(0.008, 0.999)),
	("5", (0.8, -3.0, 0.0), (0.701, 0.713)),
	("3", (0.8, -4.7, 0.0), (0.0, 1.0)),
	("7", (4.3, -7.4, 0.0), (-0.696, 0.717)),
	("8", (8.0, -8.0, 0.0),  (-0.0153, 0.999)),
	("4", (3.1, 4.8, 0.0),  (1, 0.000)),
	("2", (2.3, 0.7, 0.0),  (0.0122, 0.999)),
	("1", (-0.8, 2.6, 0.0), (0.0137, 0.999)),
	("6", (-5.9, 4.9, 0.0), (-0.999, 0.0241)),
	("9", (4.3, 7.9, 0.0),  (0.642, 0.7661)),
	("10", (9.8, -2.7, 0.0),(-0.007, 0.999)),
]

class Controller(Node):

	last_qr = None

	def __init__(self):
		super().__init__('green_turtle_controller')

		self.navigation = self.create_publisher(PoseStamped, '/goal_pose', qos_profile_sensor_data)
		self.scaner = self.create_subscription(String, '/scans', self.scan_received, 10)
		self._actionclient = ActionClient(self, NavigateToPose, '/navigate_to_pose', )
		# # self.srv = self.create_service(Scan, '/start', self.send_goal)

	def scan_received(self, msg):
		self.get_logger().info(f"QR data= {msg.data}")
		self.last_qr = msg.data

	def start_navigation(self, coord):
		_, pos, orientation = coord


		pose = PoseStamped()
		pose.pose.position.x, pose.pose.position.y, _ = pos
		pose.pose.orientation.z, pose.pose.orientation.w = orientation
		pose.header = Header()
		pose.header.frame_id = "odom"
		self.get_logger().info(f"Sending navigation goal for pos {pose}")

		# self.navigation.publish(pose)
		goal = NavigateToPose.Goal()
		goal.pose = pose
		
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

	for coord in coords:
		service.start_navigation(coord)
		
		while not service.check_qr(coord[0]):
			print("waiting")
			time.sleep(1)
			rclpy.spin_once(service, timeout_sec=1)

		time.sleep(10)


if __name__ == '__main__':
    main()
