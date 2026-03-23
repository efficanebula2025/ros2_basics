import rclpy, math
from rclpy.node import Node
from geometry_msgs.msg import Pose2D, Twist

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # Publisher
        self.pose_pub = self.create_publisher(Pose2D, '/robot_pose', 10)

        # Subscriber
        self.create_subscription(Twist, '/cmd_vel', self.vel_callback, 10)

        # Timer
        self.timer = self.create_timer(0.1, self.update_state)

    def vel_callback(self, msg):
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def update_state(self):
        dt = 0.1

        # Kinematic equations — this is what moves the robot
        self.x     += self.linear_vel * math.cos(self.theta) * dt
        self.y     += self.linear_vel * math.sin(self.theta) * dt
        self.theta += self.angular_vel * dt

        # Publish updated pose
        msg = Pose2D()
        msg.x = self.x
        msg.y = self.y
        msg.theta = self.theta
        self.pose_pub.publish(msg)

        self.get_logger().info(
            f'x:{self.x:.2f}  y:{self.y:.2f}  θ:{self.theta:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
