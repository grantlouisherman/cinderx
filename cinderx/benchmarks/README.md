# CinderX Benchmarks

Benchmarks for measuring CinderX JIT performance on real-world Python workloads.

## Quick Start

```bash
uv venv
uv pip install setuptools
uv pip install -e . --no-build-isolation --reinstall
uv run python benchmarks/runner.py
uv run python benchmarks/runner.py --iterations 10
```

This runs all benchmarks whose dependencies are available, skipping the rest with
a helpful message about what to install. Lightweight benchmarks run with 3 iterations
by default — use `--iterations N` for more.

## Lightweight Benchmarks

These benchmarks have no extra dependencies beyond cinderx itself:

```bash
uv run python benchmarks/binary_trees.py 5
uv run python benchmarks/fannkuch.py 3
uv run python benchmarks/nbody.py 3
uv run python benchmarks/richards.py 3
uv run python benchmarks/spectral_norm.py 3
```

The numeric argument controls the number of iterations (higher = longer run).

## JIT Compilation Time Benchmark

Measures how long the JIT takes to compile functions (not runtime performance):

```bash
uv run python -m cinderx.benchmarks.compile_time
```

## Heavyweight Benchmarks

These require additional dependencies to be installed.

### Full Suite (fastmark)

The `fastmark` benchmark runs the full pyperformance suite with CinderX:

```bash
uv pip install -r benchmarks/requirements-fastmark.txt
uv run python benchmarks/fastmark.py --cinderx
```

Options:
- `--scale N` — work scale factor (default 100, lower = faster)
- `--json output.json` — save results as JSON
- `--cinderx` — enable the CinderX JIT
- `benchmarks...` — run only specific benchmarks (e.g. `richards chaos`)

## Running Without CinderX JIT

To get a baseline comparison without JIT compilation, disable it via environment variable:

```bash
# With JIT (default)
uv run python benchmarks/runner.py

# Without JIT (baseline)
CINDERJIT_DISABLE=1 uv run python benchmarks/runner.py
```

## Benchmark Descriptions

| Benchmark | Description |
|-----------|-------------|
| `binary_trees` | Allocation-heavy workload building and traversing complete binary trees |
| `fannkuch` | Combinatorial puzzle exercising array permutations and reversals |
| `nbody` | N-body gravitational simulation with tight floating-point loops |
| `richards` | Operating system task scheduler simulation (object-oriented workload) |
| `spectral_norm` | Numerical computation of the spectral norm of a matrix |
| `compile_time` | Measures JIT compilation speed (not runtime performance) |
| `fastmark` | Full pyperformance suite (~60 benchmarks) with CinderX integration |

## Listing Available Benchmarks

```bash
uv run python benchmarks/runner.py --list
```
