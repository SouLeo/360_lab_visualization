cmake_minimum_required(VERSION 2.8.3)
project(vr_ui)

find_package(catkin REQUIRED COMPONENTS message_generation geometry_msgs sensor_msgs look_at_pose rviz_textured_sphere rviz_plugin_osvr rospy std_msgs roscpp std_srvs)

# video_stream_opencv 

catkin_package(CATKIN_DEPENDS roscpp message_runtime rospy sensor_msgs INCLUDE_DIRS)

include_directories(${catkin_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})

#############
## Install ##
#############

catkin_install_python(PROGRAMS nodes/test_rotate_cam
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
