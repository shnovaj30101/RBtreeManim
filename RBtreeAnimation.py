from manim import *
from setting import *
from RBtreeNode import RBTreeNode
import math

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

class DummyCircle:
    def __init__(self, rbtree_demo, rbtree_animation, *, start_node):
        self.rbtree_demo = rbtree_demo
        self.rbtree_animation = rbtree_animation
        self.circle = Circle(radius=DUMMY_CIRCLE_RADIUS, color="GREEN", fill_opacity=0).move_to(self.rbtree_animation.start_coor)
        self.rbtree_demo.play(Create(self.circle), run_time=RUN_TIME_UNIT)

    def move(self, coor):
        return self.circle.animate.move_to(coor)
        

class RBTreeAnimation:
    def __init__(self, rbtree_demo, *, start_coor = ORIGIN) -> None:
        self.rbtree_demo = rbtree_demo
        self.start_coor = start_coor
        self.displayed_object_set = set()
        self.data_node_map = dict()
        self.root = RBTreeNode(rbtree_demo, self, is_root=True)
        self.dummy_circle = None

    def insert(self, insert_data):
        self.dummy_circle = DummyCircle(self.rbtree_demo, self, start_node = self.root)
        now_node = self.root

        if now_node.data == -1:
            now_node.set_data(insert_data, self.dummy_circle)
            return

        while True:
            if now_node.data > insert_data:
                if now_node.left is None:
                    now_node.left = RBTreeNode(
                        self.rbtree_demo,
                        self,
                        data = insert_data,
                        dummy_circle = self.dummy_circle,
                        parent = now_node,
                        child_type = 'left',
                    )
                    self._solve_red_collision(now_node.left)
                    break

                now_node = now_node.left
                self.rbtree_demo.play(self.dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)

            else:
                if now_node.right is None:
                    now_node.right = RBTreeNode(
                        self.rbtree_demo,
                        self,
                        data = insert_data,
                        dummy_circle = self.dummy_circle,
                        parent = now_node,
                        child_type = 'right',
                    )
                    self._solve_red_collision(now_node.right)
                    break

                now_node = now_node.right
                self.rbtree_demo.play(self.dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)


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
            now_node.set_black()
            return

        parent_node = now_node.parent
        if now_node.black_num or parent_node.black_num:
            return

        grandparent_node = parent_node.parent
        if now_node == parent_node.left and parent_node == grandparent_node.left:
            if grandparent_node.right and not grandparent_node.right.black_num: # R/R/B\R
                parent_node.set_black()
                grandparent_node.set_red()
                grandparent_node.right.set_black()
                self._solve_red_collision(grandparent_node)

            else: # R/R/B\B
                self._rotation(parent_node, grandparent_node)
                parent_node.set_black()
                grandparent_node.set_red()

        elif now_node == parent_node.left and parent_node == grandparent_node.right:
            if grandparent_node.left and not grandparent_node.left.black_num: # R/R\B/R
                parent_node.set_black()
                grandparent_node.set_red()
                grandparent_node.left.set_black()
                self._solve_red_collision(grandparent_node)

            else: # R/R\B/B
                self._rotation(now_node, parent_node)
                self._rotation(now_node, grandparent_node)
                now_node.set_black()
                grandparent_node.set_red()

        elif now_node == parent_node.right and parent_node == grandparent_node.left:
            if grandparent_node.right and not grandparent_node.right.black_num: # R\R/B\R
                parent_node.set_black()
                grandparent_node.set_red()
                grandparent_node.right.set_black()
                self._solve_red_collision(grandparent_node)

            else: # R\R/B\B
                self._rotation(now_node, parent_node)
                self._rotation(now_node, grandparent_node)
                now_node.set_black()
                grandparent_node.set_red()

        elif now_node == parent_node.right and parent_node == grandparent_node.right:
            if grandparent_node.left and not grandparent_node.left.black_num: # R\R\B/R
                parent_node.set_black()
                grandparent_node.set_red()
                grandparent_node.left.set_black()
                self._solve_red_collision(grandparent_node)

            else: # R\R\B/B
                self._rotation(parent_node, grandparent_node)
                parent_node.set_black()
                grandparent_node.set_red()

    def _rotation(self, up, down):
        down_parent = down.parent
        if up == down.left:
            pre_up_right = up.right
            down.set_left_child(pre_up_right)
            up.set_parent(None)
            up.set_right_child(down)
            up.set_parent(down_parent)
            up.recursive_add_parent_tree_group(add_items = list(up.tree_vgroup))
            if down.parent is None:
                up.child_type = ''
                pass
            elif down.parent.left == down:
                down.parent.set_left_child(up)
            else:
                down.parent.set_right_child(up)

            down.set_parent(up)
            if pre_up_right is not None:
                pre_up_right.set_parent(down)

            up.is_root = down.is_root

            if up.is_root:
                self.root = up

            down.is_root = 0

        elif up == down.right:
            pre_up_left = up.left
            down.set_right_child(pre_up_left)
            up.set_parent(None)
            up.set_left_child(down)
            up.set_parent(down_parent)
            up.recursive_add_parent_tree_group(add_items = list(up.tree_vgroup))
            if down.parent is None:
                up.child_type = ''
                pass
            elif down.parent.left == down:
                down.parent.set_left_child(up)
            else:
                down.parent.set_right_child(up)

            down.set_parent(up)
            if pre_up_left is not None:
                pre_up_left.set_parent(down)

            up.is_root = down.is_root

            if up.is_root:
                self.root = up

            down.is_root = 0

        down.rotation_move(up)

