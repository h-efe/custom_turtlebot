import math, time, rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class Track(Node):
    def __init__(self):
        super().__init__("odom_track")
        self.create_subscription(Odometry, "/odom/unfiltered", self.cb, 10)
        self.x0 = None; self.last = None; self.path = 0.0; self.t = time.time()
    def cb(self, m):
        x, y = m.pose.pose.position.x, m.pose.pose.position.y
        if self.x0 is None:
            self.x0, self.y0 = x, y; self.last = (x, y); return
        self.path += math.hypot(x - self.last[0], y - self.last[1]); self.last = (x, y)
        if time.time() - self.t > 0.5:
            self.t = time.time()
            print(f"baslangica uzaklik: {math.hypot(x-self.x0, y-self.y0):.3f} m   toplam yol: {self.path:.3f} m", flush=True)

rclpy.init(); n = Track()
try:
    rclpy.spin(n)
except KeyboardInterrupt:
    print(f"\nSON -> baslangica uzaklik: {math.hypot(n.last[0]-n.x0, n.last[1]-n.y0):.3f} m   toplam yol: {n.path:.3f} m")
