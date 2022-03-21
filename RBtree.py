from manim import *
import math

class RedNode(Scene):
    def construct(self):
        circle = Circle(radius=0.6, color="RED", fill_opacity=0.5)
        node_data = MathTex("3", font_size=60)
        node = VGroup(circle, node_data)
        self.add(node)

class BlackNode(Scene):
    def construct(self):
        circle = Circle(radius=0.6, color="GREY", fill_opacity=0.5)
        node_data = MathTex("3", font_size=60)
        node = VGroup(circle, node_data)
        self.add(node)

class RBTree_1(Scene):
    def construct(self):
        dummy_circle = Circle(radius=0.7, color="GREEN", fill_opacity=0)
        circle = Circle(radius=0.6, color="GREY", fill_opacity=0.5)
        node_data = MathTex("1", font_size=60)
        node = VGroup(circle, node_data)
        self.play(Create(dummy_circle), run_time=2)
        self.play(Transform(dummy_circle, node), run_time=2)

class RBTree_1_2(Scene):
    def construct(self):
        numberplane = NumberPlane()
        self.add(numberplane)

        dummy_circle = Circle(radius=0.7, color="GREEN", fill_opacity=0)
        circle_1 = Circle(radius=0.6, color="GREY", fill_opacity=0.5)
        node_1_data = MathTex("1", font_size=60)
        node_1 = VGroup(circle_1, node_1_data)
        self.play(Create(dummy_circle), run_time=1)
        self.play(Transform(dummy_circle, node_1), run_time=0.5)

        dummy_circle2 = Circle(radius=0.7, color="GREEN", fill_opacity=0)
        self.play(Create(dummy_circle2), run_time=1)

        start_point_x = 0.7 * math.cos(math.pi * 1/4)
        start_point_y = -0.7 * math.sin(math.pi * 1/4)
        end_point_x = (3 - 0.7) * math.cos(math.pi * 1/4)
        end_point_y = -(3 - 0.7) * math.sin(math.pi * 1/4)

        arrow = Arrow([start_point_x, start_point_y, 0], [end_point_x, end_point_y, 0], color="GREY", buff=0)
        self.play(Create(arrow), run_time=1)
        self.play(dummy_circle2.animate.move_to(RIGHT * 3 * math.cos(math.pi * 1/4) + DOWN * 3 * math.sin(math.pi * 1/4)))

        circle_2 = Circle(radius=0.6, color="RED", fill_opacity=0.5)
        node_2_data = MathTex("2", font_size=60)
        node_2 = VGroup(circle_2, node_2_data).shift(RIGHT * 3 * math.cos(math.pi * 1/4) + DOWN * 3 * math.sin(math.pi * 1/4))
        self.play(Transform(dummy_circle2, node_2), run_time=0.5)

def traversal(node):
    if node is None:
        return

    traversal(node.left)
    print("{} {} {} {} {}".format(
        node.parent.data if node.parent else -1,
        node.data,
        node.black_num,
        node.left.data if node.left else -1,
        node.right.data if node.right else -1,
        ))
    traversal(node.right)

class RBTreeNode:
    def __init__(self, rbtree_demo, rbtree_animation, *, dummy_circle = None, data = -1, is_root = False) -> None:
        self.rbtree_demo = rbtree_demo
        self.rbtree_animation = rbtree_animation
        self.left = None
        self.right = None
        self.parent = None
        self.is_root = is_root
        self.data = data
        if is_root:
            self.black_num = 1
            self.color = "GREY"
        else:
            self.black_num = 0
            self.color = "RED"

        if dummy_circle is None:
            self.circle = Circle(radius=0.6, color=self.color, fill_opacity=0.5)
            self.node_data = MathTex(str(self.data), font_size=60)
            self.node = VGroup(self.circle, self.node_data)
            self.rbtree_demo.play(FadeIn(self.node), run_time=1)
        else:
            self.circle = Circle(radius=0.6, color=self.color, fill_opacity=0.5)
            self.node_data = MathTex(str(self.data), font_size=60)
            self.node = VGroup(self.circle, self.node_data)
            self.rbtree_demo.play(Transform(dummy_circle, self.node), run_time=1)

    def set_data(self, data, dummy_circle = None):
        self.data = data

        if dummy_circle is None:
            self.node_data = MathTex(str(self.data), font_size=60)
            pre_node = self.node
            self.node = VGroup(self.circle, self.node_data)
            self.rbtree_demo.play(FadeIn(self.node), FadeOut(pre_node), run_time=1)
        else:
            self.node_data = MathTex(str(self.data), font_size=60)
            pre_node = self.node
            self.node = VGroup(self.circle, self.node_data)
            self.rbtree_demo.play(Transform(dummy_circle, self.node), FadeOut(pre_node), run_time=1)

    def _get_sibling_node(self):
        pass

    def _get_remote_nephew_node(self):
        pass

    def _get_near_nephew_node(self):
        pass

class DummyCircle:
    def __init__(self, rbtree_demo, rbtree_animation):
        self.rbtree_demo = rbtree_demo
        self.rbtree_animation = rbtree_animation
        self.circle = Circle(radius=0.7, color="GREEN", fill_opacity=0)
        self.rbtree_demo.play(Create(dummy_circle), run_time=1)

class RBTreeAnimation:
    def __init__(self, rbtree_demo) -> None:
        self.rbtree_demo = rbtree_demo
        self.root = RBTreeNode(rbtree_demo, self, is_root=True)
        self.dummy_circle = None

    def insert(self, insert_data, now_node = None):
        if now_node is None:
            now_node = self.root

        if now_node.data == -1:
            dummy_circle = DummyCircle(self.rbtree_demo, self)
            now_node.set_data(insert_data, dummy_circle)
            self._solve_red_collision(now_node)

        elif now_node.data > insert_data:
            if now_node.left is None:
                now_node.left = RBTreeNode(self.rbtree_demo, self)
                now_node.left.parent = now_node
            self.insert(insert_data, now_node.left)

        else:
            if now_node.right is None:
                now_node.right = RBTreeNode(self.rbtree_demo, self)
                now_node.right.parent = now_node
            self.insert(insert_data, now_node.right)

    def delete(self):
        pass

    def _delete_node_handle(self):
        pass

    def _BBB_delete_node_handle(self):
        pass

    def _BRB_delete_node_handle(self):
        pass

    def _BBR_delete_node_handle(self):
        pass

    def _solve_red_collision(self, now_node = None):
        if now_node is None:
            now_node = self.root
        if now_node.is_root:
            now_node.black_num = 1
            return

        parent_node = now_node.parent
        if now_node.black_num or parent_node.black_num:
            return

        grandparent_node = parent_node.parent
        if now_node == parent_node.left and parent_node == grandparent_node.left:
            if grandparent_node.right and not grandparent_node.right.black_num: # R/R/B\R
                parent_node.black_num += 1
                grandparent_node.black_num = 0
                grandparent_node.left.black_num += 1
                self._solve_red_collision(grandparent_node)

            else: # R/R/B\B
                self._rotation(parent_node, grandparent_node)
                parent_node.black_num += 1
                grandparent_node.black_num = 0

        elif now_node == parent_node.left and parent_node == grandparent_node.right:
            if grandparent_node.left and not grandparent_node.left.black_num: # R/R\B/R
                parent_node.black_num += 1
                grandparent_node.black_num = 0
                grandparent_node.left.black_num += 1
                self._solve_red_collision(grandparent_node)

            else: # R/R\B/B
                self._rotation(now_node, parent_node)
                self._rotation(now_node, grandparent_node)
                now_node.black_num += 1
                grandparent_node.black_num = 0

        elif now_node == parent_node.right and parent_node == grandparent_node.left:
            if grandparent_node.right and not grandparent_node.right.black_num: # R\R/B\R
                parent_node.black_num += 1
                grandparent_node.black_num = 0
                grandparent_node.right.black_num += 1
                self._solve_red_collision(grandparent_node)

            else: # R\R/B\B
                self._rotation(now_node, parent_node)
                self._rotation(now_node, grandparent_node)
                now_node.black_num += 1
                grandparent_node.black_num = 0

        elif now_node == parent_node.right and parent_node == grandparent_node.right:
            if grandparent_node.left and not grandparent_node.left.black_num: # R\R\B/R
                parent_node.black_num += 1
                grandparent_node.black_num = 0
                grandparent_node.left.black_num += 1
                self._solve_red_collision(grandparent_node)

            else: # R\R\B/B
                self._rotation(parent_node, grandparent_node)
                parent_node.black_num += 1
                grandparent_node.black_num = 0

    def _rotation(self, up, down):
        if up == down.left:
            up.parent = down.parent
            if up.parent is None:
                pass
            elif up.parent.left == down:
                up.parent.left = up
            else:
                up.parent.right = up
            down.parent = up
            down.left = up.right
            if up.right is not None:
                up.right.parent = down
            up.right = down
            up.is_root = down.is_root

            if up.is_root:
                self.root = up

            down.is_root = 0

        elif up == down.right:
            up.parent = down.parent
            if up.parent is None:
                pass
            elif up.parent.left == down:
                up.parent.left = up
            else:
                up.parent.right = up
            down.parent = up
            down.right = up.left
            if up.left is not None:
                up.left.parent = down
            up.left = down
            up.is_root = down.is_root

            if up.is_root:
                self.root = up

            down.is_root = 0

class RBTreeDemo(Scene):
    def construct(self):
        numberplane = NumberPlane()
        self.add(numberplane)

        rbtree_animation = RBTreeAnimation(self)
        rbtree_animation.insert(1)
        # rbtree_animation.insert(5)
        # rbtree_animation.insert(2)
        # rbtree_animation.insert(8)
        # rbtree_animation.insert(9)
        # rbtree_animation.insert(7)
        # rbtree_animation.insert(6)
        # rbtree_animation.insert(3)
        # rbtree_animation.insert(4)
        # rbtree_animation.insert(10)

        traversal(rbtree_animation.root)




