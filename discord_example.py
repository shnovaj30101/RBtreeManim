from manim import *

class MobjectApplyFunctionExample(Scene):
     def construct(self):
        triangle= Triangle(fill_color=BLUE, fill_opacity=1).set_color_by_gradient([RED, BLUE,GREEN, PURPLE])
        circle = Circle(fill_color=GREEN_C, fill_opacity=1, stroke_color=GREEN)
        self.add(circle)
        #Each x_coordinate in the screen turns into the output of the function, thus structure of shape changes as well
        self.play(circle.animate.apply_function(lambda x: np.sin(x)))
        self.wait()
        self.play(circle.animate.apply_function(lambda x: x-2))
        self.wait()
        self.remove(circle)
        self.add(triangle)
        self.play(triangle.animate.apply_function(lambda x: x ** 3))
        self.wait()
        self.play(triangle.animate.apply_function(lambda x: 2*x))#Scales by 2
        self.wait()

