import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import math as m

class TurtlesimRotation(Node):
    def __init__(self):
        super().__init__("Turtlesim_rotation")

        self.turtle1_pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1PoseCallback,10)
        self.turtle2_pose_sub_ = self.create_subscription(Pose, "/turtle2/pose", self.turtle2PoseCallback,10)

        self.last_turtle1_pose_ = Pose()
        self.last_turtle2_pose_ = Pose()

    def turtle1PoseCallback(self, pose):
        self.last_turtle1_pose_ = pose

    def turtle2PoseCallback(self, pose):
        self.last_turtle2_pose_ = pose

        dx = self.last_turtle2_pose_.x - self.last_turtle1_pose_.x
        dy = self.last_turtle2_pose_.y - self.last_turtle1_pose_.y

        angle = self.last_turtle2_pose_.theta - self.last_turtle1_pose_.theta
        angle_deg = m.degrees(angle)
        sin = m.sin(angle)
        cos = m.cos(angle)


        self.get_logger().info("""\n
                               dx = %.2f\n
                               dy = %.2f\n
                               theta(rad) = %.2f\n
                               theta(deg) = %.2f\n
                               matrix = \n
                               | %.2f  %.2f |\n
                               | %.2f  %.2f |\n
                               """%(dx,dy,angle,angle_deg,cos,-sin,sin,cos))


def main():
    rclpy.init()
    node = TurtlesimRotation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()