#!/usr/bin/env python3
"""
Scan a Python project for imports and generate a PEP-621 pyproject.toml
Usage:
  python generate_pyproject.py --path /path/to/repo --python ">=3.8" --pin loose --output pyproject.toml
Pin options:
  none  -> no versions
  loose -> use recommended loose constraints (>=)
  exact -> pin exact versions (you can edit mapping_versions in the script)
"""
import ast
import argparse
import os
from collections import defaultdict

# Mapping from top-level import name to PyPI package name and recommended loose version (optional)
mapping = {
    "streamlit": ("streamlit", ">=1.20.0,<1.50.0"),
    "pandas": ("pandas", ">=2.0.0"),
    "tiktoken": ("tiktoken", ">=0.4.0"),
    "requests": ("requests", ">=2.28.0"),
    "openai": ("openai", ">=0.27.0"),
    "sentence_transformers": ("sentence-transformers", ">=2.2.2"),
    "sentence": ("sentence-transformers", ">=2.2.2"),  # sometimes used
    "langchain": ("langchain", ">=0.0.300"),
    "langchain_community": ("langchain-community", ">=0.0.10"),
    "langchain_openai": ("langchain-openai", ">=0.0.8"),
    "langgraph": ("langgraph", ">=0.1.0"),
    "qdrant_client": ("qdrant-client", ">=1.7.0"),
    "qdrant": ("qdrant-client", ">=1.7.0"),
    "matplotlib": ("matplotlib", ">=3.7.0"),
    "dotenv": ("python-dotenv", ">=1.0.0"),
    "sklearn": ("scikit-learn", ">=1.0.0"),
    "PIL": ("Pillow", ">=9.0.0"),
    "numpy": ("numpy", ">=1.24.0"),
    "torch": ("torch", ">=2.0.0"),
    "transformers": ("transformers", ">=4.0.0"),
}

# If you want exact pins, modify this dict with exact versions
mapping_exact = {k: v for k, v in mapping.items()}

def find_py_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip virtualenvs and common build dirs
        if any(skip in dirpath for skip in ("/.venv", "/venv", "/.git", "/__pycache__", "/.mypy_cache")):
            continue
        for f in filenames:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)

def collect_imports(py_files):
    imports = set()
    for path in py_files:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                src = fh.read()
            tree = ast.parse(src, path)
        except Exception:
            # skip files that can't be parsed
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    root = n.name.split(".")[0]
                    imports.add(root)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split(".")[0]
                    imports.add(root)
    return imports

def map_to_pypi(imports):
    deps = {}
    unknown = set()
    for imp in sorted(imports):
        if imp in mapping:
            pkg, ver = mapping[imp]
            deps[pkg] = ver
        else:
            # heuristics: convert underscores to hyphens (common packaging pattern)
            candidate = imp.replace("_", "-")
            # ignore stdlib modules and local package names heuristic:
            # If the name is very short or looks like stdlib, skip (you can adjust)
            if imp in ("os","sys","ast","math","json","re","pathlib","typing","datetime","itertools","functools","logging","http","unittest","subprocess"):
                continue
            # treat as unknown third-party
            deps[candidate] = None
            unknown.add(imp)
    return deps, unknown

def build_pyproject(deps, python_requires=">=3.8", pin="loose"):
    # build dependencies lines
    dep_lines = []
    for pkg in sorted(deps.keys()):
        ver = deps[pkg]
        if pin == "none":
            dep_lines.append(f'  "{pkg}"')
        elif pin == "loose":
            if ver:
                dep_lines.append(f'  "{pkg}{ver}"')
            else:
                dep_lines.append(f'  "{pkg}"')
        elif pin == "exact":
            # use mapping_exact if available else no version
            ver = mapping_exact.get(pkg, (pkg, None))[1]
            if ver:
                dep_lines.append(f'  "{pkg}{ver}"')
            else:
                dep_lines.append(f'  "{pkg}"')
    deps_text = ",\n".join(dep_lines)
    content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "generated-project"
version = "0.1.0"
description = "Auto-generated pyproject from imports"
readme = "README.md"
license = {{ text = "MIT" }}
requires-python = "{python_requires}"

dependencies = [
{deps_text}
]

[project.optional-dependencies]
dev = [
  "pytest>=7.0.0",
  "black>=23.0.0",
  "ruff>=0.10.0",
]
"""
    return content

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=".", help="Path to repository root")
    p.add_argument("--python", default=">=3.8", help="requires-python string")
    p.add_argument("--pin", choices=("none", "loose", "exact"), default="loose")
    p.add_argument("--output", default="pyproject.toml")
    args = p.parse_args()

    py_files = list(find_py_files(args.path))
    print(f"Scanning {len(py_files)} .py files...")
    imports = collect_imports(py_files)
    print(f"Found {len(imports)} top-level imports.")
    deps, unknown = map_to_pypi(imports)
    # show summary
    print("Mapped dependencies (guessed):")
    for pkg, ver in sorted(deps.items()):
        print(f"  {pkg}: {ver or '(no version)'}")
    if unknown:
        print("\nUnknown original imports mapped to package names (review these):")
        for u in sorted(unknown):
            print(" ", u)
    content = build_pyproject(deps, python_requires=args.python, pin=args.pin)
    with open(args.output, "w", encoding="utf-8") as out:
        out.write(content)
    print(f"\nWrote {args.output}. Please review it before installing/locking.")

if __name__ == "__main__":
    main()
