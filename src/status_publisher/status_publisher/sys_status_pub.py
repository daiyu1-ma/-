import platform

import psutil
import rclpy
from rclpy.node import Node

from status_interfaces.msg import SystemStatus


class SysStatusPubNode(Node):
    def __init__(self):
        super().__init__('sys_status_pub')
        self._publisher = self.create_publisher(SystemStatus, 'sys_status', 10)
        # cpu_percent 首次调用返回 0.0，先触发一次以保证后续读数有效
        psutil.cpu_percent(interval=None)
        self._timer = self.create_timer(1.0, self._timer_callback)
        self.get_logger().info(
            'sys_status_pub has been started, publishing on /sys_status')

    def _timer_callback(self):
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()

        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.hostname = platform.node()
        msg.cpu_percent = psutil.cpu_percent(interval=None)
        msg.memory_percent = memory.percent
        msg.memory_total = float(memory.total)
        msg.memory_available = float(memory.available)
        msg.net_sent = float(network.bytes_sent)
        msg.net_recv = float(network.bytes_recv)

        self._publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SysStatusPubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
