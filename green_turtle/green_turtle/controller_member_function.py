# from values.srv import Value
# import sys

# import rclpy
# from rclpy.node import Node

# class ScannerControllerAsync(Node):

#     def __init__(self):
#     	super().__init__('client_async')
# 	self.cli = self.create_client(Scan, 'scan')
# 	while not self.cli.wait_for_service(timeout.sec=1.0):
# 		self.get_logger().info('service not avaiable, waiting again...')
# 	self.req = Scan.Request()
	
#     def send_request(self):
#     	self.req.a = bool(sys.argv[1])
#     	self.future = self.cli.call_async(self.req)
    	
# def main(args=None):
# 	rclpy.init(args=args)
	
# 	client = client_async()
# 	client.send_request()
	
# 	while rclpy.ok():
# 	   rclpy.spin_once(client)
# 	   if client.future.done():
# 	   	try:
# 	   		response = client_future.result()
# 	   	except Exception as e:
# 	   		client.get_logger().info(
# 	   			'Service call failed %r' % (e,))
# 	   	else:
# 	   		client.get_logger().info(
# 	   		'Result of Scan: for %d' %
# 	   		(response))
# 	   	break
	   	
# 	client.destroy_node()
# 	rclpy.shutdown()
	
#  if __name__ == '__main__':
#     main()
