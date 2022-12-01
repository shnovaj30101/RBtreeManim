
from manim import *
from setting import *
from RBtreeAnimation import RBTreeAnimation
import math

class RBTreeDemo(Scene):
    def construct(self):
        # 這邊去註解可以在背景加入網格線
        # numberplane = NumberPlane()
        # self.add(numberplane)

        # start_coor 可以改變跟節點的初始位置
        # 設定方法為 x * UP + y * RIGHT，x 和 y 可以自由設定，最後跟節點必會位於網格線上的座標 (x,y)
        rbtree_animation = RBTreeAnimation(self, start_coor = UP*2)

        # 可使用 rbtree_animation.insert() 或是 rbtree_animation.delete()
        # 來指定要插入什麼資料以及刪除什麼資料

        ### normal demo

        # rbtree_animation.insert(6)
        # rbtree_animation.insert(1)
        # rbtree_animation.insert(5)
        # rbtree_animation.insert(2)
        # rbtree_animation.insert(8)
        # rbtree_animation.insert(9)
        # rbtree_animation.insert(7)
        # rbtree_animation.insert(5.5)
        # rbtree_animation.insert(3)
        # rbtree_animation.insert(10)
        # rbtree_animation.insert(8.5)
        # rbtree_animation.insert(0.5)
        # rbtree_animation.insert(7.5)
        # rbtree_animation.insert(0.75)
        # rbtree_animation.insert(6.5)
        # rbtree_animation.insert(0.6)
        # rbtree_animation.insert(0.65)
        # rbtree_animation.insert(5.3)
        # rbtree_animation.insert(5.8)
        # rbtree_animation.insert(0.3)
        # rbtree_animation.insert(0.8)
        # rbtree_animation.insert(7.8)
        # rbtree_animation.insert(4)
        # self.wait()

        ### delete_test: 1 -> 2 -> -2

        # rbtree_animation.insert(1)
        # rbtree_animation.insert(2)
        # rbtree_animation.delete(2)
        # self.wait()

        ### delete_test: 2 -> 1 -> -1

        # rbtree_animation.insert(2)
        # rbtree_animation.insert(1)
        # rbtree_animation.delete(1)
        # self.wait()

        ### delete_test: 1 -> 2 -> -2 -> -1

        # rbtree_animation.insert(1)
        # rbtree_animation.insert(2)
        # rbtree_animation.delete(2)
        # rbtree_animation.delete(1)
        # self.wait()

        ### delete_test: 2 -> 1 -> -1 -> -2

        # rbtree_animation.insert(2)
        # rbtree_animation.insert(1)
        # rbtree_animation.delete(1)
        # rbtree_animation.delete(2)
        # self.wait()

        ### delete_test: 1 -> 2 -> -1

        rbtree_animation.insert(1)
        rbtree_animation.insert(2)
        rbtree_animation.delete(1)
        self.wait()

        ### delete_test: 2 -> 1 -> -2

        # rbtree_animation.insert(2)
        # rbtree_animation.insert(1)
        # rbtree_animation.delete(2)
        # self.wait()




