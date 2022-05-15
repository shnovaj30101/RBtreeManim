from multiprocessing.pool import RUN
from shutil import move
from manim import *
import math

NODE_CIRCLE_RADIUS = 0.3
DUMMY_CIRCLE_RADIUS = 0.35
HORIZONTAL_NODE_SPACING = 1.5
RUN_TIME_UNIT = 0.1 
INIT_ARROW_LENGTH = HORIZONTAL_NODE_SPACING/2*(2**0.5) - 2*NODE_CIRCLE_RADIUS
LINE_WIDTH = 3
TIP_LENGTH = 0.2

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
    def __init__(self,
            rbtree_demo,
            rbtree_animation, *,
            dummy_circle = None,
            data = -1,
            parent = None,
            child_type = '',
            is_root = False) -> None:
        self.rbtree_demo = rbtree_demo
        self.rbtree_animation = rbtree_animation
        self.left = None
        self.right = None
        self.parent = parent
        self.child_type = child_type
        self.is_root = is_root
        self.data = data
        self.tree_vgroup = set()
        self.rbtree_animation.data_node_map[data] = self
        if is_root:
            self.black_num = 1
            self.color = "GREY"
        else:
            self.black_num = 0
            self.color = "RED"

        if self.parent is None:
            self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
            self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
            self.node = VGroup(self.circle, self.node_data).move_to(self.rbtree_animation.start_coor)

            self.recursive_add_parent_tree_group(add_items=[self])

        else:
            self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
            self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
            if self.child_type == 'left':
                self.node = VGroup(self.circle, self.node_data).move_to(self.parent._get_left_child_pos())
                arrow = self.parent.left_child_arrow

            elif self.child_type == 'right':
                self.node = VGroup(self.circle, self.node_data).move_to(self.parent._get_right_child_pos())
                arrow = self.parent.right_child_arrow

            self.recursive_add_parent_tree_group(add_items=[self])

        if self.parent is None:
            if dummy_circle is None:
                self.rbtree_demo.play(FadeIn(self.node), run_time=RUN_TIME_UNIT)
                self.rbtree_animation.displayed_object_set.add(self)
            else:
                self.rbtree_demo.play(ReplacementTransform(dummy_circle.circle, self.node), run_time=RUN_TIME_UNIT)
                self.rbtree_animation.displayed_object_set.add(self)
        else:
            if dummy_circle is None:
                self.rbtree_demo.play(
                    FadeIn(arrow.arrow), run_time=RUN_TIME_UNIT)
                self.rbtree_animation.displayed_object_set.add(arrow)
            else:
                move_distance = HORIZONTAL_NODE_SPACING/2
                left_or_right_from_root = \
                    'right' if parent.circle.get_center()[0] > self.rbtree_animation.root.circle.get_center()[0] else 'left'

                no_border_cross = True
                left_node_list = []
                right_node_list = []
                no_border_cross_subtree_node = self
                no_border_cross_subtree_node_type = None

                trace_parent_node = self
                while trace_parent_node != self.rbtree_animation.root:

                    if no_border_cross:
                        if trace_parent_node.child_type == 'right' and \
                            round(trace_parent_node.parent.circle.get_center()[0], 5) >= round(self.circle.get_center()[0], 5):
                            no_border_cross = False
                            no_border_cross_subtree_node_type = 'right'

                        elif trace_parent_node.child_type == 'left' and \
                            round(trace_parent_node.parent.circle.get_center()[0], 5) <= round(self.circle.get_center()[0], 5):
                            no_border_cross = False
                            no_border_cross_subtree_node_type = 'left'
                        else:
                            no_border_cross_subtree_node = trace_parent_node.parent

                    if not no_border_cross:
                        if trace_parent_node.child_type == 'right':
                            left_node_list.append(trace_parent_node.parent)
                        elif trace_parent_node.child_type == 'left':
                            right_node_list.append(trace_parent_node.parent)

                    trace_parent_node = trace_parent_node.parent

                if no_border_cross:
                    if self.child_type == 'right':
                        self.rbtree_demo.play(
                            dummy_circle.move(self.parent._get_right_child_pos()),
                            FadeIn(arrow.arrow), run_time=RUN_TIME_UNIT)
                        self.rbtree_animation.displayed_object_set.add(arrow)
                    elif self.child_type == 'left':
                        self.rbtree_demo.play(
                            dummy_circle.move(self.parent._get_left_child_pos()),
                            FadeIn(arrow.arrow), run_time=RUN_TIME_UNIT)
                        self.rbtree_animation.displayed_object_set.add(arrow)

                else:
                    if left_or_right_from_root == 'right':
                        if no_border_cross_subtree_node_type == 'right':
                            if self.child_type == 'right':
                                pass # impossible
                            elif self.child_type == 'left':
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance, mode = 'right'), right_node_list),
                                    *map(lambda node: node.left_child_arrow.shift_start(RIGHT * move_distance), right_node_list),
                                    *map(lambda node: node.parent.right_child_arrow.shift_end(RIGHT * move_distance), filter(lambda node: node.child_type == 'right', right_node_list)),
                                    no_border_cross_subtree_node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance),
                                    no_border_cross_subtree_node.parent.right_child_arrow.shift_end(RIGHT * move_distance),
                                    FadeIn(arrow.arrow),
                                    arrow.arrow.animate.shift(RIGHT * move_distance),
                                    dummy_circle.move(self.parent._get_left_child_pos() + RIGHT * move_distance),
                                    run_time=RUN_TIME_UNIT)
                                # because of some manim bugs: arrow.shift not change arrow.start, arrow.end
                                arrow.arrow.start += RIGHT * move_distance
                                arrow.arrow.end += RIGHT * move_distance
                                ###################################################
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                no_border_cross_subtree_node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance)
                                for node in right_node_list:
                                    node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance, mode = 'right')

                        elif no_border_cross_subtree_node_type == 'left':
                            if self.child_type == 'right':
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance, mode = 'right'), right_node_list),
                                    *map(lambda node: node.left_child_arrow.shift_start(RIGHT * move_distance), right_node_list),
                                    *map(lambda node: node.parent.right_child_arrow.shift_end(RIGHT * move_distance), filter(lambda node: node.child_type == 'right', right_node_list)),
                                    FadeIn(arrow.arrow),
                                    dummy_circle.move(self.parent._get_right_child_pos()),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                for node in right_node_list:
                                    node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance, mode = 'right')

                            elif self.child_type == 'left':
                                pass # impossible
                    elif left_or_right_from_root == 'left':
                        if no_border_cross_subtree_node_type == 'right':
                            if self.child_type == 'right':
                                pass # impossible
                            elif self.child_type == 'left':
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance, mode = 'left'), left_node_list),
                                    *map(lambda node: node.right_child_arrow.shift_start(LEFT * move_distance), left_node_list),
                                    *map(lambda node: node.parent.left_child_arrow.shift_end(LEFT * move_distance), filter(lambda node: node.child_type == 'left', left_node_list)),
                                    FadeIn(arrow.arrow),
                                    dummy_circle.move(self.parent._get_left_child_pos()),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                for node in left_node_list:
                                    node.tree_vgroup_undisplayed_mobject_shift(LEFT * move_distance, mode = 'left')

                        elif no_border_cross_subtree_node_type == 'left':
                            if self.child_type == 'right':
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance, mode = 'left'), left_node_list),
                                    *map(lambda node: node.right_child_arrow.shift_start(LEFT * move_distance), left_node_list),
                                    *map(lambda node: node.parent.left_child_arrow.shift_end(LEFT * move_distance), filter(lambda node: node.child_type == 'left', left_node_list)),
                                    no_border_cross_subtree_node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance),
                                    no_border_cross_subtree_node.parent.left_child_arrow.shift_end(LEFT * move_distance),
                                    FadeIn(arrow.arrow),
                                    arrow.arrow.animate.shift(LEFT * move_distance),
                                    dummy_circle.move(self.parent._get_right_child_pos() + LEFT * move_distance),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                # because of some manim bugs: arrow.shift not change arrow.start, arrow.end
                                arrow.arrow.start += LEFT * move_distance
                                arrow.arrow.end += LEFT * move_distance
                                ###################################################
                                no_border_cross_subtree_node.tree_vgroup_undisplayed_mobject_shift(LEFT * move_distance)
                                for node in left_node_list:
                                    node.tree_vgroup_undisplayed_mobject_shift(LEFT * move_distance, mode = 'left')

                            elif self.child_type == 'left':
                                pass # impossible

            if dummy_circle is None:
                self.rbtree_demo.play(FadeIn(self.node), run_time=RUN_TIME_UNIT)
                self.rbtree_animation.displayed_object_set.add(self)
            else:
                self.rbtree_demo.play(ReplacementTransform(dummy_circle.circle, self.node), run_time=RUN_TIME_UNIT)
                self.rbtree_animation.displayed_object_set.add(self)

        self.right_child_arrow = ChildArrow(
            self.rbtree_demo,
            self.rbtree_animation,
            from_node = self,
            x_dir = 1,
            y_dir = -1,
        )

        self.left_child_arrow = ChildArrow(
            self.rbtree_demo,
            self.rbtree_animation,
            from_node = self,
            x_dir = -1,
            y_dir = -1,
        )
        self.recursive_add_parent_tree_group(add_items=[self.left_child_arrow, self.right_child_arrow])

    def tree_vgroup_displayed_mobject_animate_shift(self, direction, mode='all'):
        if mode == 'left':
            if self.left:
                tree_vgroup_list = list(self.left.tree_vgroup) + [self, self.left_child_arrow]
            else:
                tree_vgroup_list = [self, self.left_child_arrow]
        elif mode == 'right':
            if self.right:
                tree_vgroup_list = list(self.right.tree_vgroup) + [self, self.right_child_arrow]
            else:
                tree_vgroup_list = [self, self.right_child_arrow]
        else:
            tree_vgroup_list = list(self.tree_vgroup)

        displayed_mobject_set = set(tree_vgroup_list) & self.rbtree_animation.displayed_object_set
        displayed_mobject_vgroup = VGroup()

        for n in displayed_mobject_set:
            if isinstance(n, RBTreeNode):
                displayed_mobject_vgroup.add(n.circle)
                displayed_mobject_vgroup.add(n.node_data)
            elif isinstance(n, ChildArrow):
                displayed_mobject_vgroup.add(n.arrow)

        # because of some manim bugs: arrow.shift not change arrow.start, arrow.end
        for n in displayed_mobject_vgroup:
            if isinstance(n, Arrow):
                n.start += direction
                n.end += direction
        ###################################################

        return displayed_mobject_vgroup.animate.shift(direction)

    def tree_vgroup_undisplayed_mobject_shift(self, direction, mode='all'):
        if mode == 'left':
            if self.left:
                tree_vgroup_list = list(self.left.tree_vgroup) + [self, self.left_child_arrow]
            else:
                tree_vgroup_list = [self, self.left_child_arrow]
        elif mode == 'right':
            if self.right:
                tree_vgroup_list = list(self.right.tree_vgroup) + [self, self.right_child_arrow]
            else:
                tree_vgroup_list = [self, self.right_child_arrow]
        else:
            tree_vgroup_list = list(self.tree_vgroup)

        undisplayed_mobject_set = set(tree_vgroup_list) - self.rbtree_animation.displayed_object_set
        undisplayed_mobject_vgroup = VGroup()

        for n in undisplayed_mobject_set:
            if isinstance(n, RBTreeNode):
                undisplayed_mobject_vgroup.add(n.circle)
                undisplayed_mobject_vgroup.add(n.node_data)
            elif isinstance(n, ChildArrow):
                undisplayed_mobject_vgroup.add(n.arrow)

        # because of some manim bugs: arrow.shift not change arrow.start, arrow.end
        for n in undisplayed_mobject_vgroup:
            if isinstance(n, Arrow):
                n.start += direction
                n.end += direction
        ###################################################
        undisplayed_mobject_vgroup.shift(direction)

    def set_data(self, data, dummy_circle = None):
        self.data = data

        if dummy_circle is None:
            now_pos = self.circle.get_center()
            self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
            self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
            pre_node = self.node
            self.node = VGroup(self.circle, self.node_data).move_to(now_pos)
            self.rbtree_demo.play(FadeIn(self.node), FadeOut(pre_node), run_time=RUN_TIME_UNIT)
        else:
            now_pos = self.circle.get_center()
            self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
            self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
            pre_node = self.node
            self.node = VGroup(self.circle, self.node_data).move_to(now_pos)
            self.rbtree_demo.play(ReplacementTransform(dummy_circle.circle, self.node), FadeOut(pre_node), run_time=RUN_TIME_UNIT)
            self.rbtree_animation.displayed_object_set.add(self)

    def recursive_add_parent_tree_group(self, *, add_items = [], remove_items = []):
        for item in remove_items:
            self.tree_vgroup.remove(item)
        for item in add_items:
                self.tree_vgroup.add(item)

        if self.parent is not None:
            self.parent.recursive_add_parent_tree_group(add_items = add_items, remove_items = remove_items)

    def _get_sibling_node(self):
        pass

    def _get_remote_nephew_node(self):
        pass

    def _get_near_nephew_node(self):
        pass

    def _get_right_child_pos(self):
        arrow_x_dir = self.right_child_arrow.x_direction
        arrow_y_dir = self.right_child_arrow.y_direction
        hypotenuse = (arrow_x_dir**2+arrow_y_dir**2)**0.5

        x_pos = self.circle.get_center()[0] + arrow_x_dir + 2 * self.circle.radius * arrow_x_dir / hypotenuse
        y_pos = self.circle.get_center()[1] + arrow_y_dir + 2 * self.circle.radius * arrow_y_dir / hypotenuse
        return RIGHT * x_pos + UP * y_pos

    def _get_left_child_pos(self):
        arrow_x_dir = self.left_child_arrow.x_direction
        arrow_y_dir = self.left_child_arrow.y_direction
        hypotenuse = (arrow_x_dir**2+arrow_y_dir**2)**0.5

        x_pos = self.circle.get_center()[0] + arrow_x_dir + 2 * self.circle.radius * arrow_x_dir / hypotenuse
        y_pos = self.circle.get_center()[1] + arrow_y_dir + 2 * self.circle.radius * arrow_y_dir / hypotenuse
        return RIGHT * x_pos + UP * y_pos

class ChildArrow:
    def __init__(self, 
            rbtree_demo,
            rbtree_animation, *,
            from_node,
            x_dir,
            y_dir, 
            length = INIT_ARROW_LENGTH,
        ):
        self.from_node = from_node
        self.x_direction = length * x_dir/(x_dir**2+y_dir**2)**0.5
        self.y_direction = length * y_dir/(x_dir**2+y_dir**2)**0.5
        hypotenuse = (self.x_direction**2 + self.y_direction**2)**0.5

        from_node_x_coor, from_node_y_coor, *_ = self.from_node.circle.get_center()
        radius = self.from_node.circle.radius
        self.arrow = Arrow(
            start = [
                from_node_x_coor + radius * self.x_direction / hypotenuse,
                from_node_y_coor + radius * self.y_direction / hypotenuse,
                0],
            end = [
                from_node_x_coor + radius * self.x_direction / hypotenuse + self.x_direction,
                from_node_y_coor + radius * self.y_direction / hypotenuse + self.y_direction,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

    def shift_start(self, direction):
        self.x_direction -= direction[0]
        self.y_direction -= direction[1]

        new_arrow = Arrow(
            self.arrow.start + direction,
            self.arrow.end,
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def move_start(self, position):
        self.x_direction = self.arrow.end[0] - position[0]
        self.y_direction = self.arrow.end[1] - position[1]

        new_arrow = Arrow(
            position,
            self.arrow.end,
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def shift_end(self, direction):
        self.x_direction += direction[0]
        self.y_direction += direction[1]

        new_arrow = Arrow(
            self.arrow.start,
            self.arrow.end + direction,
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def move_end(self, position):
        self.x_direction = position[0] - self.arrow.start[0]
        self.y_direction = position[1] - self.arrow.start[1]

        new_arrow = Arrow(
            self.arrow.start,
            position,
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )
        self.arrow.target.put_start_and_end_on(self.arrow.start, position)

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

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

            else: # R/R\B/B V
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
        rbtree_animation.insert(3)
        rbtree_animation.insert(10)
        rbtree_animation.insert(5.5)
        rbtree_animation.insert(8.5)
        rbtree_animation.insert(0.5)
        rbtree_animation.insert(7.5)
        rbtree_animation.insert(0.75)
        rbtree_animation.insert(6.5)
        # rbtree_animation.insert(0.6)
        # rbtree_animation.insert(0.65)
        # rbtree_animation.insert(5.3)
        # rbtree_animation.insert(5.8)
        self.wait()
