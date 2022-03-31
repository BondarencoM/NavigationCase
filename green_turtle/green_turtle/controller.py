from threading import Thread
import rclpy
from rclpy.impl import rcutils_logger
from rclpy.node import Node
from rclpy.action import ActionClient
from green_interfaces.srv import Scan
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

import time

coords = [
	("0", (-6.26329, -4.64111, 0.0), (0.0, 0.0, 0.00848949, 0.999964), 0.0169792),
	("1", (-0.841427, 2.67423, 0.0), (0.0, 0.0, 0.0137728, 0.999905), 0.0275465),
	("2", (2.30796, 0.747669, 0.0),  (0.0, 0.0, 0.0122631, 0.999925), 0.0245268),
	("3", (1.05082, -4.55658, 0.0),  (0.0, 0.0, 0.000976583, 1), 0.00195317),
	("4", (3.16242, 4.8034, 0.0),    (0.0, 0.0, 1, 0.000397207), 3.1408),
	("5", (0.878812, -3.00759, 0.0), (0.0, 0.0, 0.701042, 0.71312), 1.55372),
	("6", (-5.962, 4.91293, 0.0),    (0.0, 0.0, -0.999708, 0.0241475), -3.09329),
	("7", (4.36006, -7.47229, 0.0),  (0.0, 0.0, -0.696966, 0.717104), -1.54232),
	("8", (8.05787, -8.03957, 0.0),  (0.0, 0.0, -0.0153137, 0.999883), -0.0306286),
	("9", (4.3872, 7.97167, 0.0),    (0.0, 0.0, 0.642645, 0.766164), 1.39589),
	("10", (9.80156, -2.75549, 0.0),  (0.0, 0.0, -0.00746938, 0.999972),-0.0149389),
]

class Controller(Node):

	last_qr = None

	def __init__(self):
		super().__init__('green_turtle_controller')
		self.navigation = self.create_publisher(PoseStamped, '/goal_pose', 10)
		self.scaner = self.create_subscription(String, '/scans', self.scan_received, 10)
		# self._actionclient = ActionClient(self, NavigateToPose, '/navigate_to_pose')
		# self.srv = self.create_service(Scan, '/start', self.send_goal)

	def scan_received(self, msg):
		self.get_logger().info(f"QR data= {msg.data}")
		self.last_qr = msg.data

	def start_navigation(self, coord):
		_, pos, orientation, _ = coord


		pose = PoseStamped()
		pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = pos
		pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w = orientation
		pose.header.frame_id = 'map'

		self.get_logger().info(f"Sending navigation goar for pos {pose}")

		# self.navigation.publish(pose)
		goal = NavigateToPose.Goal()
		goal.pose = pose
		
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
			rclpy.spin_once(service, timeout_sec=1)
		time.sleep(10)


if __name__ == '__main__':
    main()
