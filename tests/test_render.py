"""渲染层测试。"""

import unittest

from primefactor.model import build_tree, layout_tree
from primefactor.render import render_worksheet, tree_svg


class TreeSvgTest(unittest.TestCase):
    def test_svg_skeleton(self):
        svg = tree_svg(12)
        self.assertIn("<svg", svg)
        self.assertIn('role="img"', svg)

    def test_circle_count(self):
        nodes = layout_tree(build_tree(12)).nodes
        self.assertEqual(tree_svg(12).count("<circle"), len(nodes))

    def test_edges_present(self):
        self.assertIn("<line", tree_svg(12))

    def test_prime_has_single_circle(self):
        self.assertEqual(tree_svg(97).count("<circle"), 1)

    def test_size_units(self):
        self.assertIn("mm", tree_svg(12))

    def test_custom_width(self):
        self.assertIn('width="120.00mm"', tree_svg(12, 120.0))


class WorksheetTest(unittest.TestCase):
    def test_item_count(self):
        html = render_worksheet([12, 36, 100])
        self.assertEqual(html.count('class="item"'), 3)

    def test_skeleton(self):
        html = render_worksheet([12])
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn('<meta charset="utf-8">', html)

    def test_value_present(self):
        self.assertIn("360", render_worksheet([360]))

    def test_answers_hidden(self):
        html = render_worksheet([12, 36])
        self.assertNotIn("参考答案", html)

    def test_answers_included(self):
        html = render_worksheet([12, 360], include_answers=True)
        self.assertIn("参考答案", html)
        self.assertIn("12 = 2^2 × 3", html)
        self.assertIn("360 = 2^3 × 3^2 × 5", html)
        self.assertIn("<circle", html)

    def test_title_escaped(self):
        html = render_worksheet([12], title="<因数> & 树")
        self.assertIn("&lt;因数&gt; &amp; 树", html)

    def test_empty(self):
        self.assertIn("暂无题目", render_worksheet([]))

    def test_a4_style(self):
        html = render_worksheet([12])
        self.assertIn("size: A4", html)
        self.assertIn("@media print", html)


if __name__ == "__main__":
    unittest.main()
