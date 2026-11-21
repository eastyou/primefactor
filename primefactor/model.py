"""质因数分解、因数树与练习纸题目生成。"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


class FactorError(ValueError):
    """数值或参数不合法。"""


def check_number(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise FactorError("必须输入整数")
    if n < 2:
        raise FactorError("数值必须大于等于 2")
    return n


def is_prime(n: int) -> bool:
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return False
    return True


def smallest_prime_factor(n: int) -> int:
    check_number(n)
    if n % 2 == 0:
        return 2
    limit = int(math.isqrt(n))
    for divisor in range(3, limit + 1, 2):
        if n % divisor == 0:
            return divisor
    return n


def factorize(n: int) -> List[int]:
    """返回升序的质因数列表，含重复项。"""
    value = check_number(n)
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors.append(divisor)
            value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def format_factorization(n: int) -> str:
    """例如 360 -> 2^3 × 3^2 × 5。"""
    counts: Dict[int, int] = {}
    for factor in factorize(n):
        counts[factor] = counts.get(factor, 0) + 1
    parts = []
    for factor in sorted(counts):
        exponent = counts[factor]
        parts.append(str(factor) if exponent == 1 else "%d^%d" % (factor, exponent))
    return " × ".join(parts)


def divisors(n: int) -> List[int]:
    value = check_number(n)
    result = set()
    limit = int(math.isqrt(value))
    for divisor in range(1, limit + 1):
        if value % divisor == 0:
            result.add(divisor)
            result.add(value // divisor)
    return sorted(result)


def greatest_common_divisor(a: int, b: int) -> int:
    return math.gcd(check_number(a), check_number(b))


def least_common_multiple(a: int, b: int) -> int:
    return a // greatest_common_divisor(a, b) * b


@dataclass
class TreeNode:
    """因数树节点。"""

    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_tree(n: int) -> TreeNode:
    """按“最小质因数 × 商”递归构建因数树。"""
    value = check_number(n)
    if is_prime(value):
        return TreeNode(value)
    factor = smallest_prime_factor(value)
    return TreeNode(value, build_tree(factor), build_tree(value // factor))


@dataclass(frozen=True)
class Layout:
    """布局结果：节点与边，坐标以叶子间距 1 为单位。"""

    nodes: Tuple[Tuple[int, float, int], ...]
    edges: Tuple[Tuple[float, int, float, int], ...]
    width: float
    depth: int


def layout_tree(root: TreeNode) -> Layout:
    """计算树形布局，父节点位于两个子节点中点。"""
    nodes: List[Tuple[int, float, int]] = []
    edges: List[Tuple[float, int, float, int]] = []
    cursor = [0.0]

    def place(node: TreeNode, depth: int) -> float:
        if node.is_leaf():
            x = cursor[0]
            cursor[0] += 1.0
            nodes.append((node.value, x, depth))
            return x
        left_x = place(node.left, depth + 1)
        right_x = place(node.right, depth + 1)
        x = (left_x + right_x) / 2.0
        nodes.append((node.value, x, depth))
        edges.append((x, depth, left_x, depth + 1))
        edges.append((x, depth, right_x, depth + 1))
        return x

    place(root, 0)
    width = cursor[0]
    depth = max(item[2] for item in nodes)
    return Layout(tuple(nodes), tuple(edges), width, depth)


def build_worksheet(
    count: int,
    low: int = 4,
    high: int = 200,
    seed: Optional[int] = None,
) -> List[int]:
    """只抽取合数，保证每道题都能画因数树。"""
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise FactorError("题目数量必须是正整数")
    if isinstance(low, bool) or isinstance(high, bool) or not isinstance(low, int) or not isinstance(high, int):
        raise FactorError("数值范围必须是整数")
    if low < 4:
        raise FactorError("最小值不能小于 4，否则没有合数")
    if high < low:
        raise FactorError("最大值不能小于最小值")
    composites = [value for value in range(low, high + 1) if not is_prime(value)]
    if count > len(composites):
        raise FactorError("范围内只有 %d 个合数，无法生成 %d 道题" % (len(composites), count))
    rng = random.Random(seed)
    return rng.sample(composites, count)


def parse_factorization(text: str) -> List[int]:
    """解析 2*2*3、2^2×3 这类写法，返回展开后的因数列表。"""
    if not isinstance(text, str) or not text.strip():
        raise FactorError("答案不能为空")
    cleaned = text.strip().replace("×", "*").replace("x", "*").replace("X", "*")
    cleaned = cleaned.replace("·", "*").replace(" ", "")
    parts = [part for part in cleaned.split("*") if part]
    if not parts:
        raise FactorError("答案格式不正确")
    factors: List[int] = []
    for part in parts:
        if "^" in part:
            pieces = part.split("^")
            if len(pieces) != 2 or not pieces[0].isdigit() or not pieces[1].isdigit():
                raise FactorError("指数格式不正确：%s" % part)
            base, exponent = int(pieces[0]), int(pieces[1])
            if exponent < 1 or exponent > 30:
                raise FactorError("指数超出范围：%s" % part)
            factors.extend([base] * exponent)
        else:
            if not part.isdigit():
                raise FactorError("因数必须是整数：%s" % part)
            factors.append(int(part))
    return factors


def check_answer(n: int, text: str) -> bool:
    """判断答案是否把 n 完整分解成质因数。"""
    try:
        factors = parse_factorization(text)
    except FactorError:
        return False
    product = 1
    for factor in factors:
        if not is_prime(factor):
            return False
        product *= factor
    return product == n
