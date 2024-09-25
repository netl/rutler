import rclpy
from tf_transformations import quaternion_from_euler
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import PoseStamped, Quaternion

class joystickDrive(Node):
    def __init__(self):
        super().__init__("joystick_rover")

        #joystick
        self.sub = self.create_subscription(Joy, "joy", self.joystickCallback,10)

        #camera topic
        self.camera = self.create_publisher(PoseStamped, "pt_camera", 10)

    def joystickCallback(self, msg):

        #camera
        p = PoseStamped()
        f = Quaternion()
        f.x, f.y, f.z, f.w = quaternion_from_euler(msg.axes[3],msg.axes[4],0)
        p.pose.orientation = f
        self.camera.publish(p)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(joystickDrive())

if __name__ == '__main__':
    main()
