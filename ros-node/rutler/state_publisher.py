from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion, Twist
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from tf_transformations import quaternion_from_euler

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        #info for dead reckoning
        self.twist_subscriber = self.create_subscription(Twist, '/cmd_vel', self.updateTwist, 10)

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        loop_rate = self.create_rate(30)

        #variables
        x = 0
        y = 0
        rotation = 0
        self.velocity = 0
        self.angularVelocity = 0
        prevClock = self.get_clock().now().nanoseconds

        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'axis'
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['swivel', 'tilt', 'periscope']
                joint_state.position = [rotation, 0, 1]

                #time delta in nanoseconds
                t = now.nanoseconds - prevClock
                prevClock = now.nanoseconds

                #dead reckoning
                rotation += self.angularVelocity*self.velocity*t
                x += self.velocity*sin(rotation)*t
                y += self.velocity*cos(rotation)*t


                # update transform
                odom_trans.header.stamp = now.to_msg()
                odom_trans.transform.translation.x = x
                odom_trans.transform.translation.y = y
                odom_trans.transform.translation.z = 0.
                q = quaternion_from_euler(0,0,float(rotation))
                odom_trans.transform.rotation.x = q[0]
                odom_trans.transform.rotation.y = q[1]
                odom_trans.transform.rotation.z = q[2]
                odom_trans.transform.rotation.w = q[3]

                # send the joint state and transform
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)

                # This will adjust as needed per iteration
                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

    def updateTwist(self, msg):
        self.velocity = msg.linear.x
        self.angularVelocity = msg.angular.z
        self.get_logger().info(f"{self.velocity},{self.angularVelocity}")

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()
