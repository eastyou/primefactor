"""primefactor：质因数分解与因数树。"""

from .model import (
    FactorError,
    Layout,
    TreeNode,
    build_tree,
    build_worksheet,
    check_answer,
    check_number,
    divisors,
    factorize,
    format_factorization,
    greatest_common_divisor,
    is_prime,
    layout_tree,
    least_common_multiple,
    parse_factorization,
    smallest_prime_factor,
)
from .render import render_worksheet, tree_svg

__all__ = [
    "FactorError",
    "Layout",
    "TreeNode",
    "build_tree",
    "build_worksheet",
    "check_answer",
    "check_number",
    "divisors",
    "factorize",
    "format_factorization",
    "greatest_common_divisor",
    "is_prime",
    "layout_tree",
    "least_common_multiple",
    "parse_factorization",
    "render_worksheet",
    "smallest_prime_factor",
    "tree_svg",
]

__version__ = "0.1.0"
