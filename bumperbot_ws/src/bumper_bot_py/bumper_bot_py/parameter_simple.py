import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter

class SimpleParameterNode(Node):
    def __init__(self):
        super().__init__("simple_parameter")

        self.declare_parameter("simple_int_param",28)
        self.declare_parameter("simple_string_param","butt_fat")

        self.add_on_set_parameters_callback(self.paramChangeCallbacks)

    def paramChangeCallbacks(self, params):
        result = SetParametersResult()

        for param in params:
            if param.name == "simple_int_param" and param.get_type() == Parameter.Type.INTEGER:
                self.get_logger().info("simple_int_param has been changed to %d"%param.value)
                result.successful = True
            if param.name == "simple_string_param" and param.get_type() == Parameter.Type.STRING:
                self.get_logger().info("simple_string_param has been changed to %s"%param.value)
                result.successful = True

        return result
            
def main():
    rclpy.init()
    simple_parameter = SimpleParameterNode()
    rclpy.spin(simple_parameter)
    simple_parameter.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()