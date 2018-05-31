#!/usr/bin/env python

import rospy
import cv2
import glob
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, Joy, Temperature, CompressedImage
from std_msgs.msg import String

class Room(object):
    def __init__(self, name, doorways):
        self.name = name
        self.doorways = doorways #TODO: make (x,y) tuple, use these to create graph edges with other room node
        self.images = load_images('/home/nrgadmin/.ros/test/*.jpg', '/home/nrgadmin/.ros/test2/*.jpg')

class Image(object):
    def __init__(self, coord):
        self.coord = coord
        self.interactive_objects = []
        
        self.image_front = None
        self.image_rear = None

    def set_image_front(self, image_front):
        self.image_front = image_front

    def set_image_rear(self, image_rear):
        self.image_rear = image_rear

#TODO: Encapsulate load_images() into class function
def load_images(front_file_path, rear_file_path):
    bridge = CvBridge()
    image_list = []

    front_files = glob.glob(front_file_path)
    rear_files = glob.glob(rear_file_path)

    index = 0

    for current_image in front_files:
        image = cv2.imread(current_image)
        ros_image = bridge.cv2_to_imgmsg(image, encoding = 'passthrough')
        #TODO: parse coordinate locations from recorded rosbag file /pose
        front_image = Image((0,0))
        front_image.set_image_front(ros_image)
        image_list.append(front_image)
    for current_image in rear_files:
        image = cv2.imread(current_image)
        ros_image = bridge.cv2_to_imgmsg(image, encoding = 'passthrough')
        image_list[index].set_image_rear(ros_image)
        index = index + 1
    return image_list

def move_to_next_point_cb(data):
    #TODO: NN search for next position (but do outside of callback)
    rospy.loginfo('New direction selected')
    return data.data

def main():
    rospy.init_node('rosbag_playback')
    doorways = [(0,0), (0,1)] # fake tuple for doorway locations
    high_bay = Room('high_bay', doorways) 
    print 'hi'

    direction_sub = rospy.Subscriber('direction', String, move_to_next_point_cb)
    
    front_image_pub = rospy.Publisher('/front_camera/image_raw', Image, queue_size=10) 
    rear_image_pub = rospy.Publisher('/rear_camera/image_raw', Image, queue_size=10)

#    while not rospy.is_shutdown():
#        front_image_pub.publish(high_bay.images[0].image_front)
#        rear_image_pub.publish(high_bay.images[0].image_rear)
#
#    rospy.spin()

    #TODO: 
    # 3. publish to /front_camera/image_raw and /rear_camera/image_raw on arrow key press into rviz

if __name__ == '__main__':
    main()
