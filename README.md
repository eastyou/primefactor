# primefactor

[![CI](https://github.com/eastyou/primefactor/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/primefactor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

质因数分解、因数列表与可打印的因数树练习纸。

## 特性

- 试除法分解，输出升序质因数与指数形式
- 递归构建“最小质因数 × 商”的因数树，SVG 自动布局
- 答案页同时给出分解式与完整树形图
- 练习纸只抽取合数，同页不重复
- 纯标准库，零依赖，跨平台

## 安装

```bash
python -m pip install -e .
```

## 用法

```bash
primefactor factorize 360
primefactor divisors 12
primefactor sheet --count 8 --low 4 --high 200 --seed 5 --answers -o sheet.html
```

输出示例：

```text
$ primefactor factorize 360
360 = 2^3 × 3^2 × 5
质因数：2 × 2 × 2 × 3 × 3 × 5
是否质数：否
```

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `--count` | 题目数量 | 8 |
| `--low` / `--high` | 合数范围 | 4 / 200 |
| `--seed` | 随机种子 | 无 |
| `--answers` | 追加答案与因数树 | 关闭 |

## 示例

[examples/primefactor.html](examples/primefactor.html) 是 8 道分解题，答案页带因数树。

## 测试

```bash
python -m unittest discover -s tests -v
```

## 协议

MIT © 2026 eastyou
