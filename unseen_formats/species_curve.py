from manim import *
import numpy as np

class SpeciesAccumulationCurve(Scene):
    """
    An animation showing a species accumulation curve fitted to a set of points,
    with the uncertainty of the fit shown as a shaded range.
    """
    def construct(self):
        # 1. Title
        title = Text("Species Accumulation Curve", font_size=48).to_edge(UP)
        self.play(Write(title))

        # 2. Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 25, 5],
            axis_config={"color": BLUE},
            x_axis_config={"name": "Samples"},
            y_axis_config={"name": "Number of Species"}
        ).add_coordinates()
        self.play(Create(axes))

        # 3. Data points
        data_points = [
            (1, 3), (2, 6), (3, 8), (4, 10), (5, 12),
            (6, 14), (7, 15), (8, 16), (9, 17)
        ]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in data_points])
        
        # Animate the introduction of the data points one by one
        for dot in dots:
            self.play(FadeIn(dot), run_time=0.2)
        self.wait(1)

        # 4. Curve fitting function (logarithmic growth)
        def fit_func(x):
            return 8 * np.log(x + 1)

        # 5. The central fitted curve
        fitted_curve = axes.plot(fit_func, color=GREEN, x_range=[0, 9, 0.1])
        curve_label = axes.get_graph_label(fitted_curve, label="Fitted Curve", x_val=6)

        # 6. Uncertainty range
        def upper_bound(x):
            return fit_func(x) + 2.0

        def lower_bound(x):
            return fit_func(x) - 2.0

        upper_curve = axes.plot(upper_bound, color=RED, stroke_width=2, x_range=[0, 9, 0.1])
        lower_curve = axes.plot(lower_bound, color=RED, stroke_width=2, x_range=[0, 9, 0.1])

        uncertainty_area = axes.get_area(
            graph=upper_curve,
            x_range=(0.01, 9), # Start from 0.01 to avoid log(0) issues
            bounded_graph=lower_curve,
            color=RED,
            opacity=0.4
        )
        uncertainty_label = Text("Uncertainty Range", font_size=32).next_to(uncertainty_area, RIGHT)

        # 7. Animation sequence
        self.play(Create(fitted_curve), Write(curve_label), run_time=2)
        self.wait(0.5)
        self.play(
            Create(upper_curve),
            Create(lower_curve),
            run_time=1.5
        )
        self.play(FadeIn(uncertainty_area))
        self.play(Write(uncertainty_label))

        self.wait(3)
        