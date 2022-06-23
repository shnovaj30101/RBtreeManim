
from manim import *
from setting import *
from ChildArrow import ChildArrow
import math

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
                left_node_set = set()
                right_node_set = set()
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
                            left_node_set.add(trace_parent_node.parent)
                        elif trace_parent_node.child_type == 'left':
                            right_node_set.add(trace_parent_node.parent)

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
                                parent_left_child_pos = self.parent._get_left_child_pos()
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance, mode = 'right'), right_node_set),
                                    *map(lambda node: node.left_child_arrow.shift_start(RIGHT * move_distance), filter(lambda node: node.left not in right_node_set, right_node_set)),
                                    *map(lambda node: node.left_child_arrow.shift_both(RIGHT * move_distance), filter(lambda node: node.left in right_node_set, right_node_set)),
                                    *map(lambda node: node.parent.right_child_arrow.shift_end(RIGHT * move_distance), filter(lambda node: node.child_type == 'right', right_node_set)),
                                    no_border_cross_subtree_node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance),
                                    no_border_cross_subtree_node.parent.right_child_arrow.shift_end(RIGHT * move_distance),
                                    FadeIn(arrow.arrow),
                                    arrow.shift_both(RIGHT * move_distance),
                                    dummy_circle.move(parent_left_child_pos + RIGHT * move_distance),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                no_border_cross_subtree_node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance)
                                for node in right_node_set:
                                    node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance, mode = 'right')

                        elif no_border_cross_subtree_node_type == 'left':
                            if self.child_type == 'right':
                                parent_right_child_pos = self.parent._get_right_child_pos()
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(RIGHT * move_distance, mode = 'right'), right_node_set),
                                    *map(lambda node: node.left_child_arrow.shift_start(RIGHT * move_distance), filter(lambda node: node.left not in right_node_set, right_node_set)),
                                    *map(lambda node: node.left_child_arrow.shift_both(RIGHT * move_distance), filter(lambda node: node.left in right_node_set, right_node_set)),
                                    *map(lambda node: node.parent.right_child_arrow.shift_end(RIGHT * move_distance), filter(lambda node: node.child_type == 'right', right_node_set)),
                                    FadeIn(arrow.arrow),
                                    dummy_circle.move(parent_right_child_pos),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                for node in right_node_set:
                                    node.tree_vgroup_undisplayed_mobject_shift(RIGHT * move_distance, mode = 'right')

                            elif self.child_type == 'left':
                                pass # impossible
                    elif left_or_right_from_root == 'left':
                        if no_border_cross_subtree_node_type == 'right':
                            if self.child_type == 'right':
                                pass # impossible
                            elif self.child_type == 'left':
                                parent_left_child_pos = self.parent._get_left_child_pos()
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance, mode = 'left'), left_node_set),
                                    *map(lambda node: node.right_child_arrow.shift_start(LEFT * move_distance), filter(lambda node: node.right not in left_node_set, left_node_set)),
                                    *map(lambda node: node.right_child_arrow.shift_both(LEFT * move_distance), filter(lambda node: node.right in left_node_set, left_node_set)),
                                    *map(lambda node: node.parent.left_child_arrow.shift_end(LEFT * move_distance), filter(lambda node: node.child_type == 'left', left_node_set)),
                                    FadeIn(arrow.arrow),
                                    dummy_circle.move(parent_left_child_pos),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                for node in left_node_set:
                                    node.tree_vgroup_undisplayed_mobject_shift(LEFT * move_distance, mode = 'left')

                        elif no_border_cross_subtree_node_type == 'left':
                            if self.child_type == 'right':
                                parent_right_child_pos = self.parent._get_right_child_pos()
                                self.rbtree_demo.play(
                                    *map(lambda node: node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance, mode = 'left'), left_node_set),
                                    *map(lambda node: node.right_child_arrow.shift_start(LEFT * move_distance), filter(lambda node: node.right not in left_node_set, left_node_set)),
                                    *map(lambda node: node.right_child_arrow.shift_both(LEFT * move_distance), filter(lambda node: node.right in left_node_set, left_node_set)),
                                    *map(lambda node: node.parent.left_child_arrow.shift_end(LEFT * move_distance), filter(lambda node: node.child_type == 'left', left_node_set)),
                                    no_border_cross_subtree_node.tree_vgroup_displayed_mobject_animate_shift(LEFT * move_distance),
                                    no_border_cross_subtree_node.parent.left_child_arrow.shift_end(LEFT * move_distance),
                                    FadeIn(arrow.arrow),
                                    arrow.shift_both(LEFT * move_distance),
                                    dummy_circle.move(parent_right_child_pos + LEFT * move_distance),
                                    run_time=RUN_TIME_UNIT)
                                self.rbtree_animation.displayed_object_set.add(arrow)
                                no_border_cross_subtree_node.tree_vgroup_undisplayed_mobject_shift(LEFT * move_distance)
                                for node in left_node_set:
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
            x_dir = HORIZONTAL_NODE_SPACING/2,
            y_dir = -LAYER_HEIGHT,
        )

        self.left_child_arrow = ChildArrow(
            self.rbtree_demo,
            self.rbtree_animation,
            from_node = self,
            x_dir = -HORIZONTAL_NODE_SPACING/2,
            y_dir = -LAYER_HEIGHT,
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
                n.update_position(direction)

        return displayed_mobject_vgroup.animate.shift(direction)

    def __repr__(self):
        return f"RBTreeNode {self.data} {object.__repr__(self)}"

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
                n.update_position(direction)

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

    def set_black(self):
        self.black_num = 1

        if self.color == "GREY":
            return

        self.color = "GREY"
        now_pos = self.circle.get_center()
        self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
        self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
        pre_node = self.node
        self.node = VGroup(self.circle, self.node_data).move_to(now_pos)
        self.rbtree_demo.play(FadeIn(self.node), FadeOut(pre_node), run_time=RUN_TIME_UNIT)

    def set_red(self):
        self.black_num = 0

        if self.color == "RED":
            return

        self.color = "RED"
        now_pos = self.circle.get_center()
        self.node_data = MathTex(str(self.data), font_size=100*NODE_CIRCLE_RADIUS)
        self.circle = Circle(radius=NODE_CIRCLE_RADIUS, color=self.color, fill_opacity=0.5)
        pre_node = self.node
        self.node = VGroup(self.circle, self.node_data).move_to(now_pos)
        self.rbtree_demo.play(FadeIn(self.node), FadeOut(pre_node), run_time=RUN_TIME_UNIT)

    def set_parent(self, target_node):
        self.parent = target_node

    def set_left_child(self, target_node):
        if self.left is not None:
            self.recursive_add_parent_tree_group(remove_items = list(self.left.tree_vgroup) + [self.left_child_arrow])
        self.left = target_node
        self.left_child_arrow.destroy()
        self.left_child_arrow = None

        if target_node is None:
            self.left_child_arrow = ChildArrow(
                self.rbtree_demo,
                self.rbtree_animation,
                from_node = self,
                x_dir = -HORIZONTAL_NODE_SPACING/2,
                y_dir = -LAYER_HEIGHT,
            )
            self.recursive_add_parent_tree_group(add_items = [self.left_child_arrow])
        else:
            target_node.child_type = "left"
            self.left_child_arrow = ChildArrow(
                self.rbtree_demo,
                self.rbtree_animation,
                from_node = self,
                to_node = target_node,
            )
            self.rbtree_demo.add(self.left_child_arrow.arrow)
            self.rbtree_animation.displayed_object_set.add(self.left_child_arrow)
            self.recursive_add_parent_tree_group(add_items = list(self.left.tree_vgroup) + [self.left_child_arrow])

    def set_right_child(self, target_node):
        if self.right is not None:
            self.recursive_add_parent_tree_group(remove_items = list(self.right.tree_vgroup) + [self.right_child_arrow])
        self.right = target_node
        self.right_child_arrow.destroy()
        self.right_child_arrow = None

        if target_node is None:
            self.right_child_arrow = ChildArrow(
                self.rbtree_demo,
                self.rbtree_animation,
                from_node = self,
                x_dir = HORIZONTAL_NODE_SPACING/2,
                y_dir = -LAYER_HEIGHT,
            )
            self.recursive_add_parent_tree_group(add_items = [self.right_child_arrow])
        else:
            target_node.child_type = "right"
            self.right_child_arrow = ChildArrow(
                self.rbtree_demo,
                self.rbtree_animation,
                from_node = self,
                to_node = target_node,
            )
            self.rbtree_demo.add(self.right_child_arrow.arrow)
            self.rbtree_animation.displayed_object_set.add(self.right_child_arrow)
            self.recursive_add_parent_tree_group(add_items = list(self.right.tree_vgroup) + [self.right_child_arrow])


    def rotation_move(self, up):
        down = self
        move_distance = LAYER_HEIGHT
        if up.child_type == "left":
            if down.child_type == "right":
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance, mode = 'right'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance, mode = 'left'),
                    *([down.left_child_arrow.shift_start(DOWN * move_distance)] if down.left else []),
                    up.right_child_arrow.shift_both(UP * move_distance, DOWN * move_distance),
                    *([up.parent.left_child_arrow.shift_end(UP * move_distance)] if up.parent else []),
                    run_time=RUN_TIME_UNIT)
                if not down.left:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.left_child_arrow.arrow.shift(DOWN * move_distance)
                    down.left_child_arrow.update_position(DOWN * move_distance)
                        
                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance, mode = 'right')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance, mode = 'left')

            elif down.child_type == "left":
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance, mode = 'left'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance, mode = 'right'),
                    *([down.right_child_arrow.shift_start(DOWN * move_distance)] if down.right else []),
                    up.left_child_arrow.shift_both(UP * move_distance, DOWN * move_distance),
                    *([up.parent.left_child_arrow.shift_end(UP * move_distance)] if up.parent else []),
                    run_time=RUN_TIME_UNIT)
                if not down.right:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.right_child_arrow.arrow.shift(DOWN * move_distance)
                    down.right_child_arrow.update_position(DOWN * move_distance)
                        
                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance, mode = 'left')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance, mode = 'right')

        elif up.child_type == "right":
            if down.child_type == "right":
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance, mode = 'right'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance, mode = 'left'),
                    *([down.left_child_arrow.shift_start(DOWN * move_distance)] if down.left else []),
                    up.right_child_arrow.shift_both(UP * move_distance, DOWN * move_distance),
                    *([up.parent.right_child_arrow.shift_end(UP * move_distance)] if up.parent else []),
                    run_time=RUN_TIME_UNIT)
                if not down.left:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.left_child_arrow.arrow.shift(DOWN * move_distance)
                    down.left_child_arrow.update_position(DOWN * move_distance)
                        
                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance, mode = 'right')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance, mode = 'left')

            elif down.child_type == "left":
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance, mode = 'left'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance, mode = 'right'),
                    *([down.right_child_arrow.shift_start(DOWN * move_distance)] if down.right else []),
                    up.left_child_arrow.shift_both(UP * move_distance, DOWN * move_distance),
                    *([up.parent.right_child_arrow.shift_end(UP * move_distance)] if up.parent else []),
                    run_time=RUN_TIME_UNIT)
                if not down.right:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.right_child_arrow.arrow.shift(DOWN * move_distance)
                    down.right_child_arrow.update_position(DOWN * move_distance)

                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance, mode = 'left')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance, mode = 'right')

        else:
            if down.child_type == "right":
                down_up_horizontal_distance = (down.circle.get_center() - up.circle.get_center())[0]
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance, mode = 'right'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance + RIGHT * down_up_horizontal_distance, mode = 'left'),
                    *([down.left_child_arrow.shift_both(DOWN * move_distance + RIGHT * down_up_horizontal_distance, RIGHT * down_up_horizontal_distance)] if down.left else []),
                    *([down.left.tree_vgroup_displayed_mobject_animate_shift(RIGHT * down_up_horizontal_distance)] if down.left else []),
                    up.right_child_arrow.shift_both(UP * move_distance + RIGHT * down_up_horizontal_distance, DOWN * move_distance + RIGHT * down_up_horizontal_distance),
                    run_time=RUN_TIME_UNIT)
                if not down.left:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.left_child_arrow.arrow.shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance)
                    down.left_child_arrow.update_position(DOWN * move_distance + RIGHT * down_up_horizontal_distance)
                else:
                    down.left.tree_vgroup_undisplayed_mobject_shift(RIGHT * down_up_horizontal_distance),
                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance, mode = 'right')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance + RIGHT * down_up_horizontal_distance, mode = 'left')
            elif down.child_type == "left":
                down_up_horizontal_distance = (down.circle.get_center() - up.circle.get_center())[0]
                self.rbtree_demo.play(
                    down.tree_vgroup_displayed_mobject_animate_shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance, mode = 'left'),
                    up.tree_vgroup_displayed_mobject_animate_shift(UP * move_distance + RIGHT * down_up_horizontal_distance, mode = 'right'),
                    *([down.right_child_arrow.shift_both(DOWN * move_distance + RIGHT * down_up_horizontal_distance, RIGHT * down_up_horizontal_distance)] if down.right else []),
                    *([down.right.tree_vgroup_displayed_mobject_animate_shift(RIGHT * down_up_horizontal_distance)] if down.right else []),
                    up.left_child_arrow.shift_both(UP * move_distance + RIGHT * down_up_horizontal_distance, DOWN * move_distance + RIGHT * down_up_horizontal_distance),
                    run_time=RUN_TIME_UNIT)
                if not down.right:
                    # because of some manim bugs: change arrow.start, arrow.end not arrow.shift 
                    down.right_child_arrow.arrow.shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance)
                    down.right_child_arrow.update_position(DOWN * move_distance + RIGHT * down_up_horizontal_distance)
                else:
                    down.right.tree_vgroup_undisplayed_mobject_shift(RIGHT * down_up_horizontal_distance),
                down.tree_vgroup_undisplayed_mobject_shift(DOWN * move_distance + RIGHT * down_up_horizontal_distance, mode = 'left')
                up.tree_vgroup_undisplayed_mobject_shift(UP * move_distance + RIGHT * down_up_horizontal_distance, mode = 'right')

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
        x_pos, y_pos, *_ = self.right_child_arrow.to_node_position
        return RIGHT * x_pos + UP * y_pos

    def _get_left_child_pos(self):
        x_pos, y_pos, *_ = self.left_child_arrow.to_node_position
        return RIGHT * x_pos + UP * y_pos

