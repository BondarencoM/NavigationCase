import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from green_interfaces.srv import Scan
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class Controller(Node):

	def __init__(self):
		super().__init__('green_turtle_controller')
		self._action_client = ActionClient(self, NavigateToPose, '/navigate_to_pose')
		self.scaner = self.create_client(Scan, '/scan')

	def send_goal(self):
		goal_msg = NavigateToPose.Goal()

		pose = PoseStamped()
		pose.pose.position.x = -7.0
		pose.pose.position.y = -4.5
		pose.pose.position.z = 0.0
		
		goal_msg.pose = pose
		self.get_logger().info("Before waiting")
		self._action_client.wait_for_server()
		self.get_logger().info("After waiting")


		self._action_client.send_goal_async(goal_msg)

		resp = ""
		while resp != "5":
			req = Scan.Request()
			req.id = 1
			resp = self.scaner.call(req)
			self.get_logger().info(f"Scanned {resp}")

def main(args=None):
	rclpy.init(args=args)

	service = Controller()
	service.send_goal()	
	rclpy.spin(service)


if __name__ == '__main__':
    main()
