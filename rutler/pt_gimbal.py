from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32
import rclpy
from rclpy.node import Node

class panTilt(Node):
    def __init__(self):
        super().__init__('pan_tilt')
        self.sub = self.create_subscription(PoseStamped, 'pt_camera', self.handlePose, 10)
        self.panPublisher = self.create_publisher(Float32, 'rover/channel_3', 10)
        self.tiltPublisher = self.create_publisher(Float32, 'rover/channel_4', 10)

    def handlePose(self, msg):
        q = msg.pose.orientation
        tilt, pan, roll = euler_from_quaternion([q.x,q.y,q.z,q.w])
        t = Float32()
        t.data = tilt
        p = Float32()
        p.data = pan
        self.tiltPublisher.publish(t)
        self.panPublisher.publish(p)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(panTilt())

if __name__ == '__main__':
    main()
