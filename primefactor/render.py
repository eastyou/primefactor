"""因数树 SVG 与练习纸渲染。"""

from __future__ import annotations

import html
from typing import Sequence

from .model import build_tree, format_factorization, layout_tree

STYLE = """
@page { size: A4 portrait; margin: 14mm 12mm; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  color: #1b2430;
  font-size: 11pt;
  line-height: 1.5;
}
h1 { font-size: 20pt; margin: 0 0 2mm; }
.sub { color: #6b7280; font-size: 10pt; margin: 0 0 6mm; }
ol.items { margin: 0; padding-left: 7mm; }
li.item { margin-bottom: 6mm; page-break-inside: avoid; }
.head { font-size: 13pt; margin-bottom: 1mm; }
.head .value { font-family: "SFMono-Regular", Consolas, monospace; font-weight: 600; }
.blank { display: inline-block; min-width: 60mm; border-bottom: 0.8pt solid #1b2430; height: 1.1em; }
.hint { color: #6b7280; font-size: 9.5pt; }
.answers { page-break-before: always; }
.answers h2 { font-size: 15pt; margin: 0 0 4mm; }
.answers ol { padding-left: 7mm; }
.answers li { margin-bottom: 5mm; page-break-inside: avoid; }
.answers .eq { font-family: "SFMono-Regular", Consolas, monospace; font-size: 12pt; color: #0f4c81; }
svg { display: block; margin: 1mm 0 0 2mm; }
.note { color: #6b7280; font-size: 9.5pt; }
@media print { li.item, .answers li { break-inside: avoid; } }
"""


def _escape(text: str) -> str:
    return html.escape(str(text), quote=True)


def tree_svg(n: int, width_mm: float = 150.0) -> str:
    """把 n 的因数树画成 SVG。"""
    layout = layout_tree(build_tree(n))
    margin = 8.0
    usable = width_mm - margin * 2
    span = max(layout.width - 1.0, 1.0)
    step_x = usable / span
    step_y = 16.0
    height = margin * 2 + layout.depth * step_y + 8.0
    radius = 6.4

    def pos(x: float, depth: int) -> tuple:
        return (margin + x * step_x, margin + depth * step_y + radius)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
        'viewBox="0 0 %.2f %.2f" role="img" aria-label="%d 的因数树">'
        % (width_mm, height, width_mm, height, n)
    ]
    for x1, y1, x2, y2 in layout.edges:
        px1, py1 = pos(x1, y1)
        px2, py2 = pos(x2, y2)
        parts.append(
            '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#64748b" stroke-width="0.5"/>'
            % (px1, py1, px2, py2)
        )
    for value, x, depth in layout.nodes:
        cx, cy = pos(x, depth)
        parts.append(
            '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#eef6ff" stroke="#0f4c81" stroke-width="0.4"/>'
            % (cx, cy, radius)
        )
        parts.append(
            '<text x="%.2f" y="%.2f" text-anchor="middle" dominant-baseline="middle" '
            'font-size="3.4" fill="#12212f">%d</text>' % (cx, cy, value)
        )
    parts.append("</svg>")
    return "".join(parts)


def render_worksheet(
    numbers: Sequence[int],
    title: str = "质因数分解练习",
    include_answers: bool = False,
) -> str:
    """生成练习纸；答案页给出分解式与因数树。"""
    safe_title = _escape(title)
    items = []
    for index, number in enumerate(numbers, start=1):
        items.append(
            '<li class="item"><div class="head">%d. <span class="value">%d</span> = '
            '<span class="blank"></span></div>'
            '<div class="hint">写成质因数相乘的形式，能用指数就写指数。</div></li>'
            % (index, number)
        )
    body = "".join(items) or '<p class="note">暂无题目。</p>'
    parts = [
        "<!DOCTYPE html>",
        '<html lang="zh-CN">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>%s</title>" % safe_title,
        "<style>%s</style>" % STYLE,
        "</head>",
        "<body>",
        "<h1>%s</h1>" % safe_title,
        '<p class="sub">姓名：__________　班级：__________　日期：__________</p>',
        '<ol class="items">%s</ol>' % body,
    ]
    if include_answers:
        answers = []
        for index, number in enumerate(numbers, start=1):
            answers.append(
                "<li><div>%d. <span class=\"eq\">%d = %s</span></div>%s</li>"
                % (index, number, _escape(format_factorization(number)), tree_svg(number))
            )
        parts.extend(
            [
                '<section class="answers">',
                "<h2>参考答案与因数树</h2>",
                "<ol>%s</ol>" % "".join(answers),
                "</section>",
            ]
        )
    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)
