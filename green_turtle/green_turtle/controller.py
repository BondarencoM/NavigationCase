import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from green_interfaces.srv import Scan
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped

class ScannerController(Node):

	def __init__(self):
		super().__init__('service')
		self.srv = self.create_service(Scan, 'scan', self.callback)
		self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

	def send_goal(self):
		goal_msg = NavigateToPose.Goal()

		pose = PoseStamped()
		pose.pose.position.x = 5
		pose.pose.position.y = 5
		pose.pose.position.z = 0
		
		goal_msg.pose = pose

		self._action_client.wait_for_server()

		return self._action_client.send_goal_async(goal_msg)
	
	
	def callback(self, request, response):
		self.get_logger().info('Request\na: %d' % (request.id))
		response.data = "aaa"
		return response
		
def main(args=None):
	rclpy.init(args=args)

	service = ScannerController()

	rclpy.spin(service)
	service.send_goal()
	rclpy.shutdown()


if __name__ == '__main__':
    main()
