import rclpy
from tf_transformations import quaternion_from_euler
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import time

class twistDrive(Node):
    def __init__(self):
        super().__init__("twist_rover")

        #topics
        self.twist_subscriber = self.create_subscription(Twist, '/cmd_vel', self.drive, 10)
        self.steering = self.create_publisher(Float32, "/steering", 10)
        self.accelerator = self.create_publisher(Float32, "/accelerator", 10)

    def drive(self, msg):

        #steering
        steeringMsg = Float32()
        steeringMsg.data = msg.angular.z
        self.steering.publish(steeringMsg)

        #accelerator
        acceleratorMsg = Float32()
        acceleratorMsg.data = msg.linear.x
        self.accelerator.publish(acceleratorMsg)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(twistDrive())

if __name__ == '__main__':
    main()
