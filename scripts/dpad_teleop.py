#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

LINEAR_SPEED = 0.29
ANGULAR_SCALE = 0.75
DEADMAN_BUTTON = 4
DPAD_DOWN = 1
DPAD_UP = 3
RIGHT_STICK_X_AXIS = 4

class DpadTeleop(Node):
    def __init__(self):
        super().__init__('dpad_teleop')
        self.create_subscription(Joy, 'joy', self.joy_cb, 10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def joy_cb(self, msg: Joy):
        twist = Twist()
        if msg.buttons[DEADMAN_BUTTON]:
            if msg.buttons[DPAD_UP]:
                twist.linear.x = LINEAR_SPEED
            elif msg.buttons[DPAD_DOWN]:
                twist.linear.x = -LINEAR_SPEED
            twist.angular.z = msg.axes[RIGHT_STICK_X_AXIS] * ANGULAR_SCALE
        self.pub.publish(twist)

def main():
    rclpy.init()
    node = DpadTeleop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
