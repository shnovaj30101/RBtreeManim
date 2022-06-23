
from manim import *
from setting import *
from RBtreeAnimation import RBTreeAnimation
import math

class RBTreeDemo(Scene):
    def construct(self):
        # numberplane = NumberPlane()
        # self.add(numberplane)

        rbtree_animation = RBTreeAnimation(self, start_coor = UP*2)
        rbtree_animation.insert(6)
        rbtree_animation.insert(1)
        rbtree_animation.insert(5)
        rbtree_animation.insert(2)
        rbtree_animation.insert(8)
        rbtree_animation.insert(9)
        rbtree_animation.insert(7)
        rbtree_animation.insert(5.5)
        rbtree_animation.insert(3)
        rbtree_animation.insert(10)
        rbtree_animation.insert(8.5)
        rbtree_animation.insert(0.5)
        rbtree_animation.insert(7.5)
        rbtree_animation.insert(0.75)
        rbtree_animation.insert(6.5)
        rbtree_animation.insert(0.6)
        rbtree_animation.insert(0.65)
        rbtree_animation.insert(5.3)
        rbtree_animation.insert(5.8)
        rbtree_animation.insert(0.3)
        rbtree_animation.insert(0.8)
        rbtree_animation.insert(7.8)
        self.wait()
