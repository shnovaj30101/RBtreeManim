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

    def insert(self, insert_data):
        dummy_circle = DummyCircle(self.rbtree_demo, self, start_node = self.root)
        now_node = self.root

        if now_node.data == -1:
            now_node.set_data(insert_data, dummy_circle)
            return

        while True:
            if now_node.data > insert_data:
                if now_node.left is None:
                    now_node.left = RBTreeNode(
                        self.rbtree_demo,
                        self,
                        data = insert_data,
                        dummy_circle = dummy_circle,
                        parent = now_node,
                        child_type = 'left',
                    )
                    self._solve_red_collision(now_node.left)
                    break

                now_node = now_node.left
                self.rbtree_demo.play(dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)

            else:
                if now_node.right is None:
                    now_node.right = RBTreeNode(
                        self.rbtree_demo,
                        self,
                        data = insert_data,
                        dummy_circle = dummy_circle,
                        parent = now_node,
                        child_type = 'right',
                    )
                    self._solve_red_collision(now_node.right)
                    break

                now_node = now_node.right
                self.rbtree_demo.play(dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)


    def delete(self, delete_data):
        dummy_circle = DummyCircle(self.rbtree_demo, self, start_node = self.root)
        now_node = self.root

        if now_node.data == -1:
            self.rbtree_demo.play(FadeOut(dummy_circle.circle), run_time=RUN_TIME_UNIT)
            self.rbtree_demo.remove(dummy_circle.circle)

            return False

        while True:
            if now_node is None:
                self.rbtree_demo.play(FadeOut(dummy_circle.circle), run_time=RUN_TIME_UNIT)
                self.rbtree_demo.remove(dummy_circle.circle)
                return False
            elif now_node.data > delete_data:
                if now_node.left is None:
                    self.rbtree_demo.play(FadeOut(dummy_circle.circle), run_time=RUN_TIME_UNIT)
                    self.rbtree_demo.remove(dummy_circle.circle)
                    return False
                now_node = now_node.left
                self.rbtree_demo.play(dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)
            elif now_node.data < delete_data:
                if now_node.right is None:
                    self.rbtree_demo.play(FadeOut(dummy_circle.circle), run_time=RUN_TIME_UNIT)
                    self.rbtree_demo.remove(dummy_circle.circle)
                    return False
                now_node = now_node.right
                self.rbtree_demo.play(dummy_circle.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)
            else:
                break

        target_node = now_node
        replace_node = None

        dummy_circle2 = DummyCircle(self.rbtree_demo, self, start_node = now_node)
        if now_node.left is not None:
            now_node = now_node.left
            self.rbtree_demo.play(dummy_circle2.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)
            while now_node.right is not None:
                now_node = now_node.right
                self.rbtree_demo.play(dummy_circle2.move(now_node.circle.get_center()), run_time=RUN_TIME_UNIT)
            replace_node = now_node
        else:
            replace_node = now_node

        target_node.data, replace_node.data = replace_node.data, target_node.data
        self.rbtree_demo.play(Transform(replace_node.node_data, target_node.node_data), Transform(target_node.node_data, replace_node.node_data), FadeOut(dummy_circle.circle), FadeOut(dummy_circle2.circle), run_time=RUN_TIME_UNIT)
        self.rbtree_demo.remove(dummy_circle.circle)
        self.rbtree_demo.remove(dummy_circle2.circle)

        if replace_node.black_num == 0:
            # 1. replace node is red
            replace_node.destroy()
            return True

        elif replace_node.left or replace_node.right:
            # 2. replace node have child
            replace_node.destroy()
            return True
        else:
            # 2.5. replace is only root node
            if replace_node == self.root:
                replace_node.destroy()
                return True

            # 3. BBB
            # 4. BRB
            # 5. BBR
            self._delete_node_handle(replace_node)
            replace_node.destroy()
            return True


    def _delete_node_handle(self, node):
        if node.parent is None:
            return

        parent = node.parent
        sibling = self._get_sibling_node(node)

        if sibling.black_num == 1 and parent.black_num == 1:
            self._BBB_delete_node_handle(node)
        elif sibling.black_num == 1 and parent.black_num == 0:
            self._BRB_delete_node_handle(node)
        elif sibling.black_num == 0 and parent.black_num == 1:
            self._BBR_delete_node_handle(node)

    def _BBB_delete_node_handle(self, node):
        parent = node.parent
        sibling = self._get_sibling_node(node)
        remote_nephew = self._get_remote_nephew_node(node)
        near_nephew = self._get_near_nephew_node(node)

        if remote_nephew and remote_nephew.black_num == 0:
            self._rotation(sibling, parent)
            remote_nephew.set_black()

        elif near_nephew and near_nephew.black_num == 0:
            self._rotation(near_nephew, sibling)
            near_nephew.set_black()
            sibling.set_red()
            self._rotation(near_nephew, parent)
            sibling.set_black()

        else:
            sibling.set_red()
            self._delete_node_handle(parent)

    def _BRB_delete_node_handle(self, node):
        parent = node.parent
        sibling = self._get_sibling_node(node)
        remote_nephew = self._get_remote_nephew_node(node)
        near_nephew = self._get_near_nephew_node(node)

        if remote_nephew and remote_nephew.black_num == 0:
            self._rotation(sibling, parent)
            parent.set_black()
            sibling.set_red()
            remote_nephew.set_black()

        elif near_nephew and near_nephew.black_num == 0:
            self._rotation(near_nephew, sibling)
            near_nephew.set_black()
            sibling.set_red()
            self._rotation(near_nephew, parent)
            parent.set_black()
            near_nephew.set_red()
            sibling.set_black()

        else:
            parent.set_black()
            sibling.set_red()

    def _BBR_delete_node_handle(self, node):
        parent = node.parent
        sibling = self._get_sibling_node(node)
        self._rotation(sibling, parent)
        parent.set_red()
        sibling.set_black()
        self._BRB_delete_node_handle(node)

    def _get_sibling_node(self, node):
        if node.parent is None:
            return None

        if node.parent.left == node:
            return node.parent.right

        else:
            return node.parent.left

    def _get_remote_nephew_node(self, node):
        sibling = self._get_sibling_node(node)
        if sibling is None:
            return None

        if sibling.data > node.data:
            return sibling.right
        else:
            return sibling.left

    def _get_near_nephew_node(self, node):
        sibling = self._get_sibling_node(node)
        if sibling is None:
            return None

        if sibling.data > node.data:
            return sibling.left
        else:
            return sibling.right

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

