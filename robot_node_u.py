import rclpy
from rclpy.node import Node

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')

        # Robot state — single source of truth
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Timer fires every 0.1 seconds (10 Hz)
        self.timer = self.create_timer(0.1, self.update_state)

    def update_state(self):
        self.get_logger().info(
            f'State → x:{self.x:.2f}  y:{self.y:.2f}  θ:{self.theta:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
