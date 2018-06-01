#!/usr/bin/env python

import rospy
import cv2
import glob
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image as ImageMsg
from std_msgs.msg import String, Int32

class Room(object):
    def __init__(self, name, doorways):
        self.name = name
        self.doorways = doorways #TODO: make (x,y) tuple, use these to create graph edges with other room node
        self.images = self.load_images('/home/nrgadmin/.ros/test/*.jpg', '/home/nrgadmin/.ros/test2/*.jpg')

    def load_images(self, front_file_path, rear_file_path):
        bridge = CvBridge()
        image_list = []

        front_files = glob.glob(front_file_path)
        rear_files = glob.glob(rear_file_path)

        index = 0

        for current_image in front_files:
            image = cv2.imread(current_image)
            ros_image = bridge.cv2_to_imgmsg(image, encoding = 'rgb8')
            #TODO: parse coordinate locations from recorded rosbag file /pose
            front_image = Image((0,0))
            front_image.set_image_front(ros_image)
            image_list.append(front_image)
        for current_image in rear_files:
            image = cv2.imread(current_image)
            ros_image = bridge.cv2_to_imgmsg(image, encoding = 'rgb8')
            image_list[index].set_image_rear(ros_image)
            index = index + 1
        return image_list

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

class UserInput(object):
    def __init__(self):
        self.direction = 0 # initial the frame, but change to coor position search.
        self.direction_sub = rospy.Subscriber('direction', Int32, self.move_to_next_point_cb)

    def move_to_next_point_cb(self, data):
        #TODO: NN search for next position (but do outside of callback)
        rospy.loginfo('New direction selected')
        self.set_direction(data.data)
    
    def set_direction(self, direction):
        self.direction = direction

def main():
    rospy.init_node('rosbag_playback')
    doorways = [(0,0), (0,1)] # fake tuple for doorway locations
    high_bay = Room('high_bay', doorways) 

    user_input = UserInput()    

    front_image_pub = rospy.Publisher('/front_camera/image_raw', ImageMsg, queue_size=10) 
    rear_image_pub = rospy.Publisher('/rear_camera/image_raw', ImageMsg, queue_size=10)

    print 'initializations complete'

    while not rospy.is_shutdown():
        front_image_pub.publish(high_bay.images[user_input.direction].image_front)
        rear_image_pub.publish(high_bay.images[user_input.direction].image_rear)

    rospy.spin()

if __name__ == '__main__':
    main()
