import rclpy
from rclpy.node import Node


class Wuren2Node(Node):
    def __init__(self):
        super().__init__('wuren2')
        self.get_logger().info('wuren2 node has been started.')


def main(args=None):
    rclpy.init(args=args)
    node = Wuren2Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
