import rclpy
from rclpy.node import Node
from green_interfaces.srv import Scan

class ScannerController(Node):

	def __init__(self):
		super().__init__('service')
		self.srv = self.create_service(Scan, 'scan', self.callback)
	
	
	def callback(self, request, response):
		self.get_logger().info('Request\na: %d' % (request.id))
		response.data = "aaa"
		return response
		
def main(args=None):
    rclpy.init(args=args)

    service = ScannerController()

    rclpy.spin(service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
