import math, rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class Track(Node):
    def __init__(self):
        super().__init__("joint_track")
        self.create_subscription(JointState, "/joint_states", self.cb, 10)
        self.start = None; self.last = None
    def cb(self, m):
        pos = dict(zip(m.name, m.position))
        if not all(k in pos for k in ("left_wheel_joint", "right_wheel_joint")): return
        self.last = pos
        if self.start is None: self.start = pos
    def report(self):
        if not self.start or not self.last:
            print("joint verisi yok"); return
        for k in ("left_wheel_joint", "right_wheel_joint"):
            print(f"{k}: {(self.last[k]-self.start[k])/(2*math.pi):.3f} tur")

rclpy.init(); n = Track()
try:
    rclpy.spin(n)
except KeyboardInterrupt:
    n.report()
