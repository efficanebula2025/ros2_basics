import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Publisher — broadcasts pose to /robot_pose
        self.pose_pub = self.create_publisher(Pose2D, '/robot_pose', 10)

        # Timer at 10 Hz
        self.timer = self.create_timer(0.1, self.update_state)

    def update_state(self):
        msg = Pose2D()
        msg.x = self.x
        msg.y = self.y
        msg.theta = self.theta
        self.pose_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
