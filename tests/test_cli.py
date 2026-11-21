"""命令行测试。"""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from primefactor.cli import main


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class FactorizeCommandTest(unittest.TestCase):
    def test_composite(self):
        code, out, _ = run_cli(["factorize", "360"])
        self.assertEqual(code, 0)
        self.assertIn("360 = 2^3 × 3^2 × 5", out)

    def test_prime(self):
        code, out, _ = run_cli(["factorize", "97"])
        self.assertEqual(code, 0)
        self.assertIn("是否质数：是", out)

    def test_factors_listed(self):
        code, out, _ = run_cli(["factorize", "12"])
        self.assertEqual(code, 0)
        self.assertIn("2 × 2 × 3", out)

    def test_invalid_one(self):
        code, _, err = run_cli(["factorize", "1"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_invalid_number(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                main(["factorize", "abc"])
        self.assertEqual(ctx.exception.code, 2)


class DivisorsCommandTest(unittest.TestCase):
    def test_twelve(self):
        code, out, _ = run_cli(["divisors", "12"])
        self.assertEqual(code, 0)
        self.assertIn("1、2、3、4、6、12", out)

    def test_invalid(self):
        code, _, err = run_cli(["divisors", "1"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)


class SheetCommandTest(unittest.TestCase):
    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "sheet.html")
            code, out, _ = run_cli(["sheet", "--count", "6", "--seed", "1", "-o", target])
            self.assertEqual(code, 0)
            self.assertIn("已写入", out)
            with open(target, encoding="utf-8") as handle:
                html = handle.read()
            self.assertEqual(html.count('class="item"'), 6)

    def test_stdout(self):
        code, out, _ = run_cli(["sheet", "--count", "3", "--seed", "2"])
        self.assertEqual(code, 0)
        self.assertIn("<!DOCTYPE html>", out)

    def test_answers(self):
        code, out, _ = run_cli(["sheet", "--count", "2", "--seed", "3", "--answers"])
        self.assertEqual(code, 0)
        self.assertIn("参考答案", out)
        self.assertIn("<circle", out)

    def test_too_many(self):
        code, _, err = run_cli(["sheet", "--count", "3", "--low", "4", "--high", "6"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_reproducible(self):
        _, first, _ = run_cli(["sheet", "--count", "4", "--seed", "9"])
        _, second, _ = run_cli(["sheet", "--count", "4", "--seed", "9"])
        self.assertEqual(first, second)

    def test_nested_output(self):
        with tempfile.TemporaryDirectory() as folder:
            target = os.path.join(folder, "x", "y", "sheet.html")
            code, _, _ = run_cli(["sheet", "--count", "1", "-o", target])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(target))


class HelpTest(unittest.TestCase):
    def test_help_exits_zero(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
