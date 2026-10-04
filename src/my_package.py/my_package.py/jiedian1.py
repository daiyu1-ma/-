import rclpy
from rclpy.node import Node


class Jiedian1(Node):
    def __init__(self):
        super().__init__('jiedian1')
        self.get_logger().info('jiedian1 节点已启动')


def main(args=None):
    rclpy.init(args=args)
    node = Jiedian1()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
