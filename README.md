# Tensor-backend-calculator
Symbolic Tensor Calculator
This project is a symbolic tensor calculator built with Python and SymPy. Its primary goal is to compute various tensors used in differential geometry and general relativity (including the metric tensor, Christoffel symbols, Riemann tensor, Ricci tensor, Einstein tensor, and Weyl tensor) while applying custom, advanced simplification strategies.

Features
Custom Simplification:
The program extends SymPy’s built-in simplify by adding specialized routines (such as custom replacements for inverse trigonometric functions) tailored to reduce expressions for curvature tensors. For example, it automatically detects and simplifies expressions that follow the FLRW (Friedmann–Lemaître–Robertson–Walker) pattern, setting them to zero when appropriate.

Tensor Computations:
It computes a variety of tensors:

Metric Tensor – The foundation of spacetime geometry.
Christoffel Symbols – Derived from the metric and used to compute covariant derivatives.
Riemann Tensor – Encodes the intrinsic curvature of spacetime.
Ricci Tensor and Scalar Curvature – Used in formulating Einstein’s field equations.
Einstein Tensor – Combines the Ricci tensor and scalar curvature.
Weyl Tensor – Represents the conformal curvature and is automatically simplified based on identified FLRW patterns.
Advanced Logging and Debugging:
Logging is integrated into the custom simplification functions to track when an expression is forced to zero or when specific simplification patterns are recognized.

Fraction & Trigonometric Replacements:
The module provides helper functions to replace certain inverse trigonometric forms (e.g., converting 
1
tan
⁡
(
𝑥
)
tan(x)
1
​
  into 
cot
⁡
(
𝑥
)
cot(x)) and to manage conversion of floats to their fractional representations. These routines help ensure that the symbolic output is as clean and minimal as possible.

How It Works
Custom Simplify Function:
The custom_simplify(expr) function first attempts a general simplification using SymPy’s simplify(). Then, it examines the resulting expression for specific patterns (for example, checking for the combination of sine, cosine, and tangent that typically appears in FLRW models). If such a pattern is detected, the function logs the occurrence and forces the result to zero. It also replaces terms like 
1
/
tan
⁡
(
𝜃
)
1/tan(θ) with 
cot
⁡
(
𝜃
)
cot(θ) to further simplify the expression.

Weyl Tensor Simplification:
The function weyl_simplify(Weyl, n) applies custom simplification rules to the Weyl tensor. For dimensions 
𝑛
≤
3
n≤3 the tensor is automatically set to zero. In four-dimensional space, it specifically looks for FLRW patterns and sets the tensor to zero if those are found. Each nonzero component is processed by the custom_simplify function.

String-Based Replacements:
Helper functions like replace_inverse_trig_in_string(expr_str) use regular expressions to replace inverse trigonometric expressions (and other patterns) within string representations of SymPy expressions, ensuring a cleaner LaTeX output.

Fraction Conversion:
The convert_to_fractions(expr) function converts SymPy expressions into LaTeX strings and then performs additional transformations to display fractions and trigonometric functions in a more conventional mathematical notation.

Requirements
Python 3.11 or later
SymPy
(Optional) A logging setup for debugging and tracking the simplification process

Getting Started
Install Dependencies:

bash
Copy
pip install sympy
Run the Calculator:

Import and use the provided functions in your project to compute the tensors for a given metric. The module is designed to be integrated into a larger application, such as a web-based calculator.

Customization:

You can adjust the simplification routines by modifying the custom functions to suit your specific needs or to handle additional cases.

Contributing
Contributions are welcome! Feel free to open issues or pull requests if you have ideas to improve the simplification algorithms or add new features.
