#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuCovariance(Node):
    def __init__(self):
        super().__init__('imu_covariance')
        self.pub = self.create_publisher(Imu, '/imu/data', 10)
        self.create_subscription(Imu, '/imu/out', self.cb, 10)

    def cb(self, msg):
        msg.orientation_covariance = [-1.0] + [0.0] * 8
        msg.angular_velocity_covariance = [4.0e-8, 0.0, 0.0, 0.0, 4.0e-8, 0.0, 0.0, 0.0, 4.0e-8]
        msg.linear_acceleration_covariance = [2.89e-4, 0.0, 0.0, 0.0, 2.89e-4, 0.0, 0.0, 0.0, 2.89e-4]
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = ImuCovariance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()