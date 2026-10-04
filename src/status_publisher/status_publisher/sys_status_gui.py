import datetime
import sys

import rclpy
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from rclpy.node import Node

from status_interfaces.msg import SystemStatus


def format_bytes(num_bytes):
    size = float(num_bytes)
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if abs(size) < 1024.0:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} PB'


class SysStatusSubscriber(Node):
    def __init__(self):
        super().__init__('sys_status_gui')
        self.latest_msg = None
        self.create_subscription(
            SystemStatus, 'sys_status', self._callback, 10)

    def _callback(self, msg):
        self.latest_msg = msg


class StatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('System Status')
        self.resize(360, 280)

        layout = QVBoxLayout()
        self.time_label = QLabel('时间: --')
        self.hostname_label = QLabel('主机名: --')
        self.cpu_label = QLabel('CPU 使用率: --')
        self.memory_percent_label = QLabel('内存使用率: --')
        self.memory_total_label = QLabel('内存总大小: --')
        self.memory_available_label = QLabel('剩余内存: --')
        self.net_sent_label = QLabel('网络发送: --')
        self.net_recv_label = QLabel('网络接收: --')

        for label in (
            self.time_label,
            self.hostname_label,
            self.cpu_label,
            self.memory_percent_label,
            self.memory_total_label,
            self.memory_available_label,
            self.net_sent_label,
            self.net_recv_label,
        ):
            layout.addWidget(label)
        self.setLayout(layout)

    def update_status(self, msg):
        if msg is None:
            return
        time_text = datetime.datetime.fromtimestamp(
            msg.stamp.sec).strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.setText(f'时间: {time_text}')
        self.hostname_label.setText(f'主机名: {msg.hostname}')
        self.cpu_label.setText(f'CPU 使用率: {msg.cpu_percent:.1f} %')
        self.memory_percent_label.setText(
            f'内存使用率: {msg.memory_percent:.1f} %')
        self.memory_total_label.setText(
            f'内存总大小: {format_bytes(msg.memory_total)}')
        self.memory_available_label.setText(
            f'剩余内存: {format_bytes(msg.memory_available)}')
        self.net_sent_label.setText(
            f'网络发送: {format_bytes(msg.net_sent)}')
        self.net_recv_label.setText(
            f'网络接收: {format_bytes(msg.net_recv)}')


def main(args=None):
    rclpy.init(args=args)
    node = SysStatusSubscriber()

    app = QApplication(sys.argv)
    window = StatusWindow()
    window.show()

    # 用 QTimer 周期性非阻塞处理 ROS2 回调，避免阻塞 Qt 事件循环
    timer = QTimer()
    timer.timeout.connect(
        lambda: (
            rclpy.spin_once(node, timeout_sec=0.0),
            window.update_status(node.latest_msg),
        ))
    timer.start(100)

    try:
        exit_code = app.exec_()
    finally:
        timer.stop()
        node.destroy_node()
        rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
