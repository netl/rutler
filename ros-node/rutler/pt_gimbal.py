from tf_transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
from geometry_msgs.msg import PoseStamped, Pose
from std_msgs.msg import Float32
import rclpy
from rclpy.node import Node

class panTilt(Node):
    def __init__(self):
        super().__init__('pan_tilt')
        self.sub = self.create_subscription(PoseStamped, 'look_at', self.handlePose, 10)
        self.panPublisher = self.create_publisher(Float32, 'rover/channel_3', 10)
        self.tiltPublisher = self.create_publisher(Float32, 'rover/channel_4', 10)

        self.realPose = Pose()
        self.posePublisher = self.create_publisher(PoseStamped, 'pt_camera', 10)
        self.timer = self.create_timer(0.1, self.poseUpdater)
        
    def poseUpdater(self):
        p = PoseStamped()
        p.pose = self.realPose
        self.posePublisher.publish(p)

    def handlePose(self, msg):
        
        #turn quaternion in to array, because dunno
        a = (
            msg.pose.orientation.x,
            msg.pose.orientation.y,
            msg.pose.orientation.z,
            msg.pose.orientation.w)
        b = (
            self.realPose.orientation.x,
            self.realPose.orientation.y,
            self.realPose.orientation.z,
            self.realPose.orientation.w)

        newTilt, newPan, newRoll = euler_from_quaternion(a)
        tilt, pan, roll = euler_from_quaternion(b)
       
        #do the work
        t = Float32()
        t.data = max(-3.1415/2, min(tilt+newTilt, 3.1415/2)) #clamp to servo limits
        p = Float32()
        p.data = max(-3.1415/2, min(pan+newPan, 3.1415/2)) #clamp to servo limits
        result = quaternion_from_euler(t.data, p.data, 0) 

        #wrangle shit back into place
        self.realPose.orientation.x = result[0]
        self.realPose.orientation.y = result[1]
        self.realPose.orientation.z = result[2]
        self.realPose.orientation.w = result[3]

        t.data = t.data/(3.1415/2)
        p.data = p.data/(3.1415/2)
        self.tiltPublisher.publish(t)
        self.panPublisher.publish(p)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(panTilt())

if __name__ == '__main__':
    main()
