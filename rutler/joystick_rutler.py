import rclpy
from tf_transformations import quaternion_from_euler
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import PoseStamped, Quaternion
import time

class joystickDrive(Node):
    def __init__(self):
        super().__init__("joystick_rover")

        #joystick
        self.sub = self.create_subscription(Joy, "joy", self.joystickCallback,10)

        #camera topic
        self.camera = self.create_publisher(PoseStamped, "/look_at", 10)

        self.rateClock = time.time()

    def joystickCallback(self, msg):
        t = time.time()
        td = t-self.rateClock
        self.rateClock = t

        #camera
        p = PoseStamped()
        f = Quaternion()
        f.x, f.y, f.z, f.w = quaternion_from_euler(td*msg.axes[3]*3.1415,td*msg.axes[4]*3.1415,0)
        p.pose.orientation = f
        self.camera.publish(p)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(joystickDrive())

if __name__ == '__main__':
    main()
