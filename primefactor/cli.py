"""命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .model import (
    FactorError,
    build_worksheet,
    check_number,
    divisors,
    factorize,
    format_factorization,
    is_prime,
)
from .render import render_worksheet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="primefactor",
        description="质因数分解、因数树与可打印练习纸",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    factor_parser = subparsers.add_parser("factorize", help="分解一个整数")
    factor_parser.add_argument("number", type=int)

    divisor_parser = subparsers.add_parser("divisors", help="列出全部因数")
    divisor_parser.add_argument("number", type=int)

    sheet_parser = subparsers.add_parser("sheet", help="生成练习纸 HTML")
    sheet_parser.add_argument("--count", type=int, default=8, help="题目数量，默认 8")
    sheet_parser.add_argument("--low", type=int, default=4, help="最小值，默认 4")
    sheet_parser.add_argument("--high", type=int, default=200, help="最大值，默认 200")
    sheet_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    sheet_parser.add_argument("--title", default="质因数分解练习", help="练习纸标题")
    sheet_parser.add_argument("--answers", action="store_true", help="追加答案与因数树")
    sheet_parser.add_argument("-o", "--output", default=None, help="输出文件")
    return parser


def _write_output(html_text: str, output: Optional[str]) -> None:
    if not output:
        print(html_text)
        return
    path = Path(output)
    if path.parent and str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    print("已写入 %s" % path)


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "factorize":
            number = check_number(args.number)
            factors = factorize(number)
            print("%d = %s" % (number, format_factorization(number)))
            print("质因数：%s" % " × ".join(str(factor) for factor in factors))
            print("是否质数：%s" % ("是" if is_prime(number) else "否"))
            return 0
        if args.command == "divisors":
            number = check_number(args.number)
            values = divisors(number)
            print("%d 的因数（%d 个）：%s" % (number, len(values), "、".join(str(v) for v in values)))
            return 0
        numbers = build_worksheet(args.count, args.low, args.high, args.seed)
        _write_output(
            render_worksheet(numbers, args.title, include_answers=args.answers),
            args.output,
        )
        return 0
    except FactorError as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2
    except OSError as exc:
        print("写入失败：%s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
