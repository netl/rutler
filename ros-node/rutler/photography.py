import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy
from std_srvs.srv import Empty

class photographer(Node):
    def __init__(self):  
        super().__init__("photography")
        self.sub = self.create_subscription(Joy, "joy", self.photo,10)
        self.snap = self.create_client(Empty, '/save')
        self.snapRequest = Empty.Request()
        self.cameraServo = self.create_publisher(Float32, '/cameraServo', 10)
        self.prevState = 0

        self.snap.wait_for_service()

    def photo(self, msg):
        #read button
        b = msg.buttons[0]

        #animate servo
        m = Float32()
        m.data = float(-1+b*2)
        self.cameraServo.publish(m)

        #take picture when button is released
        if b == 0 and self.prevState == 1:
            self.get_logger().info("say cheese!")
            r = self.snap.call_async(Empty.Request())

        #update
        self.prevState = b

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(photographer())

if __name__ == '__main__':
    main()
