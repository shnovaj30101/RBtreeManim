
from manim import *
from setting import *
import math

class ChildArrow:
    def __init__(self, 
            rbtree_demo,
            rbtree_animation, *,
            from_node,
            to_node = None,
            x_dir = HORIZONTAL_NODE_SPACING/2,
            y_dir = -LAYER_HEIGHT,
        ):
        self.rbtree_demo = rbtree_demo
        self.rbtree_animation = rbtree_animation
        self.from_node = from_node

        if to_node is None:
            self.from_node_position = self.from_node.circle.get_center()
            self.to_node_position = self.from_node_position + RIGHT * x_dir + UP * y_dir
        else:
            self.from_node_position = self.from_node.circle.get_center()
            self.to_node_position = to_node.circle.get_center()

        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5

        self.arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

    def __repr__(self):
        return f"ChildArrow {self.from_node.data} {object.__repr__(self)}"

    def shift_start(self, direction):
        self.from_node_position += direction
        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5
        new_arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def move_start(self, position):
        self.from_node_position = position
        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5
        new_arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def shift_end(self, direction):
        self.to_node_position += direction
        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5
        new_arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def move_end(self, position):
        self.to_node_position = position
        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5
        new_arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def shift_both(self, start_direction, end_direction = None):
        if end_direction is None:
            end_direction = start_direction
        self.from_node_position += start_direction
        self.to_node_position += end_direction
        x_dir = (self.to_node_position - self.from_node_position)[0]
        y_dir = (self.to_node_position - self.from_node_position)[1]
        hypotenuse = (x_dir**2 + y_dir**2)**0.5
        new_arrow = Arrow(
            start = [
                self.from_node_position[0] + NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.from_node_position[1] + NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            end = [
                self.to_node_position[0] - NODE_CIRCLE_RADIUS * x_dir / hypotenuse,
                self.to_node_position[1] - NODE_CIRCLE_RADIUS * y_dir / hypotenuse,
                0],
            buff=0,
            stroke_width = LINE_WIDTH,
            tip_length = TIP_LENGTH,
        )

        output_transform = ReplacementTransform(self.arrow, new_arrow)
        self.arrow = new_arrow

        return output_transform

    def destroy(self):
        if self in self.rbtree_animation.displayed_object_set:
            self.rbtree_animation.displayed_object_set.remove(self)
        self.rbtree_demo.remove(self.arrow)

    def update_position(self, direction):
        self.arrow.start += direction
        self.arrow.end += direction
        self.from_node_position += direction
        self.to_node_position += direction

