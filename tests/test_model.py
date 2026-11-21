"""模型层测试。"""

import unittest

from primefactor.model import (
    FactorError,
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


class CheckNumberTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(check_number(12), 12)

    def test_two_is_valid(self):
        self.assertEqual(check_number(2), 2)

    def test_one_rejected(self):
        with self.assertRaises(FactorError):
            check_number(1)

    def test_zero_rejected(self):
        with self.assertRaises(FactorError):
            check_number(0)

    def test_bool_rejected(self):
        with self.assertRaises(FactorError):
            check_number(True)

    def test_string_rejected(self):
        with self.assertRaises(FactorError):
            check_number("12")


class PrimeTest(unittest.TestCase):
    def test_small_primes(self):
        for value in (2, 3, 5, 7, 11, 13):
            self.assertTrue(is_prime(value), value)

    def test_composites(self):
        for value in (4, 6, 8, 9, 15, 100):
            self.assertFalse(is_prime(value), value)

    def test_large_prime(self):
        self.assertTrue(is_prime(9973))

    def test_large_composite(self):
        self.assertFalse(is_prime(9999))

    def test_one_not_prime(self):
        self.assertFalse(is_prime(1))

    def test_zero_not_prime(self):
        self.assertFalse(is_prime(0))

    def test_negative_not_prime(self):
        self.assertFalse(is_prime(-7))

    def test_smallest_factor(self):
        self.assertEqual(smallest_prime_factor(15), 3)
        self.assertEqual(smallest_prime_factor(14), 2)
        self.assertEqual(smallest_prime_factor(97), 97)

    def test_smallest_factor_rejects_one(self):
        with self.assertRaises(FactorError):
            smallest_prime_factor(1)


class FactorizeTest(unittest.TestCase):
    def test_two(self):
        self.assertEqual(factorize(2), [2])

    def test_four(self):
        self.assertEqual(factorize(4), [2, 2])

    def test_twelve(self):
        self.assertEqual(factorize(12), [2, 2, 3])

    def test_360(self):
        self.assertEqual(factorize(360), [2, 2, 2, 3, 3, 5])

    def test_prime(self):
        self.assertEqual(factorize(97), [97])

    def test_hundred(self):
        self.assertEqual(factorize(100), [2, 2, 5, 5])

    def test_power_of_two(self):
        self.assertEqual(factorize(1024), [2] * 10)

    def test_product_matches(self):
        for value in range(2, 200):
            product = 1
            for factor in factorize(value):
                self.assertTrue(is_prime(factor))
                product *= factor
            self.assertEqual(product, value)

    def test_invalid(self):
        with self.assertRaises(FactorError):
            factorize(1)


class FormatTest(unittest.TestCase):
    def test_prime(self):
        self.assertEqual(format_factorization(97), "97")

    def test_power(self):
        self.assertEqual(format_factorization(8), "2^3")

    def test_mixed(self):
        self.assertEqual(format_factorization(12), "2^2 × 3")

    def test_360(self):
        self.assertEqual(format_factorization(360), "2^3 × 3^2 × 5")

    def test_100(self):
        self.assertEqual(format_factorization(100), "2^2 × 5^2")


class DivisorTest(unittest.TestCase):
    def test_twelve(self):
        self.assertEqual(divisors(12), [1, 2, 3, 4, 6, 12])

    def test_prime(self):
        self.assertEqual(divisors(13), [1, 13])

    def test_square(self):
        self.assertEqual(divisors(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])

    def test_invalid(self):
        with self.assertRaises(FactorError):
            divisors(1)

    def test_gcd(self):
        self.assertEqual(greatest_common_divisor(12, 18), 6)

    def test_lcm(self):
        self.assertEqual(least_common_multiple(4, 6), 12)

    def test_gcd_coprime(self):
        self.assertEqual(greatest_common_divisor(8, 9), 1)

    def test_lcm_multiple(self):
        self.assertEqual(least_common_multiple(3, 9), 9)


class TreeTest(unittest.TestCase):
    def test_prime_is_leaf(self):
        node = build_tree(13)
        self.assertTrue(node.is_leaf())
        self.assertEqual(node.value, 13)

    def test_composite_has_children(self):
        node = build_tree(12)
        self.assertFalse(node.is_leaf())
        self.assertEqual(node.left.value, 2)
        self.assertEqual(node.right.value, 6)

    def test_all_values_are_divisors(self):
        root = build_tree(360)
        values = set()

        def walk(node):
            values.add(node.value)
            if node.left is not None:
                walk(node.left)
            if node.right is not None:
                walk(node.right)

        walk(root)
        self.assertTrue(values.issubset(set(divisors(360))))

    def test_layout_node_count(self):
        layout = layout_tree(build_tree(360))
        self.assertEqual(len(layout.nodes), 11)

    def test_layout_leaf_count(self):
        layout = layout_tree(build_tree(360))
        self.assertEqual(layout.width, 6.0)

    def test_layout_edges(self):
        layout = layout_tree(build_tree(12))
        self.assertEqual(len(layout.edges), 4)

    def test_layout_depth(self):
        layout = layout_tree(build_tree(16))
        self.assertGreaterEqual(layout.depth, 2)

    def test_leaf_layout(self):
        layout = layout_tree(build_tree(7))
        self.assertEqual(len(layout.nodes), 1)
        self.assertEqual(len(layout.edges), 0)


class WorksheetTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(build_worksheet(8, seed=1)), 8)

    def test_unique(self):
        numbers = build_worksheet(10, seed=2)
        self.assertEqual(len(set(numbers)), 10)

    def test_only_composites(self):
        for number in build_worksheet(8, low=4, high=50, seed=3):
            self.assertFalse(is_prime(number))

    def test_in_range(self):
        for number in build_worksheet(6, low=10, high=20, seed=4):
            self.assertGreaterEqual(number, 10)
            self.assertLessEqual(number, 20)

    def test_deterministic(self):
        self.assertEqual(build_worksheet(8, seed=5), build_worksheet(8, seed=5))

    def test_different_seed(self):
        self.assertNotEqual(build_worksheet(8, seed=5), build_worksheet(8, seed=6))

    def test_too_many(self):
        with self.assertRaises(FactorError):
            build_worksheet(3, low=4, high=6)

    def test_zero(self):
        with self.assertRaises(FactorError):
            build_worksheet(0)

    def test_low_below_four(self):
        with self.assertRaises(FactorError):
            build_worksheet(3, low=2, high=10)

    def test_reversed_range(self):
        with self.assertRaises(FactorError):
            build_worksheet(3, low=20, high=10)


class ParseTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(parse_factorization("2*2*3"), [2, 2, 3])

    def test_times_symbol(self):
        self.assertEqual(parse_factorization("2×2×3"), [2, 2, 3])

    def test_power(self):
        self.assertEqual(parse_factorization("2^2*3"), [2, 2, 3])

    def test_spaces(self):
        self.assertEqual(parse_factorization(" 2 * 2 * 3 "), [2, 2, 3])

    def test_x_letter(self):
        self.assertEqual(parse_factorization("2 x 3"), [2, 3])

    def test_empty(self):
        with self.assertRaises(FactorError):
            parse_factorization("  ")

    def test_bad_exponent(self):
        with self.assertRaises(FactorError):
            parse_factorization("2^a")

    def test_zero_exponent(self):
        with self.assertRaises(FactorError):
            parse_factorization("2^0")

    def test_non_integer(self):
        with self.assertRaises(FactorError):
            parse_factorization("2*three")


class CheckAnswerTest(unittest.TestCase):
    def test_plain(self):
        self.assertTrue(check_answer(12, "2*2*3"))

    def test_power(self):
        self.assertTrue(check_answer(12, "2^2*3"))

    def test_repeated_factors(self):
        self.assertTrue(check_answer(8, "2*2*2"))

    def test_wrong_product(self):
        self.assertFalse(check_answer(12, "2*2*2"))

    def test_non_prime_factor(self):
        self.assertFalse(check_answer(12, "4*3"))

    def test_factor_one(self):
        self.assertFalse(check_answer(12, "1*2*2*3"))

    def test_garbage(self):
        self.assertFalse(check_answer(12, "abc"))

    def test_empty(self):
        self.assertFalse(check_answer(12, " "))


if __name__ == "__main__":
    unittest.main()
