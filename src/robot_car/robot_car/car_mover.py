import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import time

class SimpleMover(Node):
    def __init__(self):
        super().__init__('simple_mover')
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.listener_callback, 10)
        self.br = TransformBroadcaster(self)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.timer = self.create_timer(0.1, self.broadcast_transform)

    def listener_callback(self, msg):
        self.x += msg.linear.x * 0.1
        self.theta += msg.angular.z * 0.1

    def broadcast_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        # You can add rotation with quaternion here
        self.br.sendTransform(t)

rclpy.init()
node = SimpleMover()
rclpy.spin(node)
