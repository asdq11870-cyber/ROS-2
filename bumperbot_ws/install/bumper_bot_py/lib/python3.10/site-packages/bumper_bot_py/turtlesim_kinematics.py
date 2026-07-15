import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class SimpleTurtleSimKinematics(Node):
    def __init__(self):
        super().__init__("Turtle_sim_kinematics")

        self.turtle1_pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.turtle1PoseCallback,10)
        self.turtle2_pose_sub_ = self.create_subscription(Pose, "/turtle2/pose",self.turtle2PoseCallback,10)

        self.last_turtle1_pose_ = Pose()
        self.last_turtle2_pose_ = Pose()

    def turtle1PoseCallback(self, msg):
        self.last_turtle1_pose_ = msg

    def turtle2PoseCallback(self, msg):
        self.last_turtle2_pose_ = msg

        Tx = self.last_turtle2_pose_.x - self.last_turtle1_pose_.x
        Ty = self.last_turtle2_pose_.y - self.last_turtle1_pose_.y

        self.get_logger().info("""\n
                    Translation Vector t1 to t2\n
                    Tx = %.3f 
                    Ty = %.3f"""%(Tx, Ty))

def main():
    rclpy.init()
    node = SimpleTurtleSimKinematics()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()