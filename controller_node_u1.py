import rclpy, sys, threading
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose2D
from PyQt5.QtWidgets import (QApplication, QWidget,
    QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QTimer

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pose = [0.0, 0.0, 0.0]
        self.create_subscription(Pose2D, '/robot_pose',
            lambda m: setattr(self, 'pose', [m.x, m.y, m.theta]), 10)

    def send(self, lx=0.0, az=0.0):
        t = Twist()
        t.linear.x = lx
        t.angular.z = az
        self.pub.publish(t)

class ControlWindow(QWidget):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle('Robot Controller')
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Live pose display
        self.lbl = QLabel('x: 0.00   y: 0.00   θ: 0.00')
        self.lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl)

        # Control buttons
        buttons = [
            ('⬆  Forward',  lambda: node.send(lx= 1.0)),
            ('⬇  Backward', lambda: node.send(lx=-1.0)),
            ('⬅  Left',     lambda: node.send(az= 1.0)),
            ('➡  Right',    lambda: node.send(az=-1.0)),
            ('⏹  Stop',     lambda: node.send()),
        ]
        for label, cb in buttons:
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(cb)
            layout.addWidget(btn)

        self.setLayout(layout)

        # Refresh pose label every 100ms
        self.qt_timer = QTimer()
        self.qt_timer.timeout.connect(self.refresh)
        self.qt_timer.start(100)

    def refresh(self):
        x, y, th = self.node.pose
        self.lbl.setText(f'x: {x:.2f}   y: {y:.2f}   θ: {th:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    # ROS spins in background — Qt runs in main thread
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()
    app = QApplication(sys.argv)
    win = ControlWindow(node)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
