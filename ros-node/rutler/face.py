import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Quaternion
from cv_bridge import CvBridge
from tf_transformations import quaternion_from_euler
import cv2
import time
from math import sqrt

class faceFinder(Node):
    def __init__(self):
        super().__init__("face_seeker")
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self.face_cascade = cv2.CascadeClassifier('/home/netl/ros2_ws/src/rutler/resource/haarcascade_frontalface_default.xml')

        self.sub = self.create_subscription(Image, '/image_raw', self.processFrame,10)
        self.lookAt = self.create_publisher(PoseStamped, '/look_at', 10)
        self.outImage = self.create_publisher(Image, '/image_debug', 10)

        self.br = CvBridge()

        self.declare_parameter('frame_rate', 5)
        self.nextFrame = 0

    def processFrame(self,data):

        #limit frame rate
        t = time.time()
        if t-self.nextFrame < 0: 
            return
        self.nextFrame = t + 1/self.get_parameter(f"frame_rate").get_parameter_value().integer_value
        
        # get frame
        img = self.br.imgmsg_to_cv2(data)

        # get faces
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # find nearest to center of view
        height, width = img.shape[:2]
        center = (int(width/2),int(height/2))
        nearest = (center[0], center[1], 100000) 
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
            cx = x+w/2
            cy = y+h/2
            distance = sqrt(pow(abs(cx-center[0]),2) + pow(abs(cy-center[1]),2))
            if distance < nearest[2]:
                nearest = (int(cx), int(cy), int(distance))

        p = PoseStamped()
        if len(faces)>0:
            cv2.line(img, center, nearest[:2], (0,0,255), 3)

            # calculate view offset
            pan = 2*(center[0]-nearest[0])/width
            tilt = 1.5*(center[1]-nearest[1])/height

            # send pose
            result = quaternion_from_euler(pan,tilt,0)
            p.pose.orientation.x = result[0]
            p.pose.orientation.y = result[1]
            p.pose.orientation.z = result[2]
            p.pose.orientation.w = result[3]

        self.lookAt.publish(p)

        # debug
        imageMessage = self.br.cv2_to_imgmsg(img)
        self.outImage.publish(imageMessage)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(faceFinder())

if __name__ == '__main__':
    main()
