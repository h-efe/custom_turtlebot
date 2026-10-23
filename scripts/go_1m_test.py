#!/usr/bin/env python3
import math
import sys
import time

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node

TARGET_M = 1.0
CRUISE_MPS = 0.10
CREEP_MPS = 0.05
CREEP_ZONE_M = 0.15
TIMEOUT_S = 30.0


class OneMeterTest(Node):
    def __init__(self):
        super().__init__("one_meter_test")
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Odometry, "/odom/unfiltered", self.odom_cb, 10)
        self.x0 = None
        self.x = self.y = None
        self.start_t = None
        self.done = False
        self.timer = self.create_timer(0.05, self.step)

    def odom_cb(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        if self.x0 is None:
            self.x0, self.y0 = self.x, self.y

    def distance(self):
        return math.hypot(self.x - self.x0, self.y - self.y0)

    def send(self, v):
        t = Twist()
        t.linear.x = v
        self.pub.publish(t)

    def stop(self):
        for _ in range(20):
            self.send(0.0)
            time.sleep(0.02)

    def step(self):
        if self.done:
            return
        if self.x0 is None:
            if self.start_t is None:
                self.start_t = time.time()
            if time.time() - self.start_t > 5.0:
                print("HATA: 5 sn icinde /odom/unfiltered gelmedi, durduruluyor.")
                self.finish()
            return
        if self.start_t is None:
            self.start_t = time.time()
            print("Baslangic alindi, ileri gidiliyor...")
        d = self.distance()
        if d >= TARGET_M:
            self.finish(d)
            return
        if time.time() - self.start_t > TIMEOUT_S:
            print(f"ZAMAN ASIMI ({TIMEOUT_S}s), durduruluyor. Odometre mesafesi: {d:.3f} m")
            self.finish(d)
            return
        v = CREEP_MPS if (TARGET_M - d) < CREEP_ZONE_M else CRUISE_MPS
        self.send(v)

    def finish(self, d=None):
        self.done = True
        self.timer.cancel()
        self.stop()
        if d is None and self.x0 is not None:
            d = self.distance()
        if d is not None:
            print("")
            print(f"Odometre (Euclid) mesafe : {d:.3f} m")
            print(f"Hedef                    : {TARGET_M:.3f} m")
            print("Simdi mezuru ile gercek mesafeyi olc ve buraya yaz.")
        print(f"Son odom konumu  x={self.x} y={self.y}" if self.x is not None else "")


def main():
    rclpy.init()
    node = OneMeterTest()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.05)
    except KeyboardInterrupt:
        print("\nCtrl+C: durduruluyor.")
        node.stop()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    sys.exit(main())
