import rclpy, threading
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class VizNode(Node):
    def __init__(self):
        super().__init__('viz_node')
        self.x = 0.0
        self.y = 0.0
        self.trail_x = []
        self.trail_y = []
        self.create_subscription(Pose2D, '/robot_pose', self.cb, 10)

    def cb(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.trail_x.append(msg.x)
        self.trail_y.append(msg.y)

def main(args=None):
    rclpy.init(args=args)
    node = VizNode()

    # Spin ROS in background so matplotlib can run in main thread
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Robot Position')

    trail_line, = ax.plot([], [], 'b-', alpha=0.4, lw=1)
    robot_dot,  = ax.plot([], [], 'ro', ms=12)

    def animate(_):
        trail_line.set_data(node.trail_x, node.trail_y)
        robot_dot.set_data([node.x], [node.y])
        return trail_line, robot_dot

    ani = FuncAnimation(fig, animate, interval=100)
    plt.show()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
