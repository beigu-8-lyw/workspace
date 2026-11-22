#!/usr/bin/env python3
"""仓库卫生检查：阻止中间产物、密钥与超大文件进入版本库。

在 CI 和本地 pre-commit 中运行：
    python scripts/check_repo.py

退出码 0 = 干净，1 = 发现违规。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# --- 规则 1：禁止入库的文件名（精确匹配） ---
FORBIDDEN_NAMES = {
    ".env",
    ".DS_Store",
    "Thumbs.db",
    "req_pdf.txt",          # PDF 解析的中间产物
    "credentials.json",
}

# --- 规则 2：禁止入库的路径片段 ---
FORBIDDEN_PARTS = {
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    "htmlcov",
}

# --- 规则 3：禁止入库的后缀（密钥、压缩包、演示视频） ---
FORBIDDEN_SUFFIXES = {
    ".pem", ".key", ".p12", ".pfx",
    ".zip", ".7z", ".rar",
    ".mp4", ".mov", ".avi", ".mkv",
}

# --- 规则 4：单个文件体积上限 ---
MAX_BYTES = 10 * 1024 * 1024  # 10 MB

# --- 规则 5：高置信度密钥特征（宁可误报，不可漏报） ---
SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub Token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("OpenAI-style Key", re.compile(r"sk-[A-Za-z0-9]{32,}")),
    ("私钥文件头", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("Slack Token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
]

# 自身与示例文件会包含上述字符串，跳过扫描
SKIP_SCAN = {"scripts/check_repo.py", ".env.example", ".gitignore"}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".json", ".yml", ".yaml", ".md",
                 ".txt", ".sql", ".env", ".sh", ".java", ".go", ".vue"}


def tracked_files(staged: bool = False) -> list[Path]:
    """返回待检查的文件列表。

    staged=True 时检查暂存区（供 pre-commit 钩子使用），否则检查已跟踪文件。
    """
    cmd = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
        if staged
        else ["git", "ls-files", "-z"]
    )
    try:
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ 无法执行 git 命令，请在仓库根目录运行本脚本", file=sys.stderr)
        sys.exit(2)
    return [Path(p) for p in out.decode("utf-8").split("\0") if p]


def check_name(path: Path) -> str | None:
    if path.name in FORBIDDEN_NAMES:
        return f"禁止入库的文件名：{path}"
    for part in path.parts[:-1]:
        if part in FORBIDDEN_PARTS:
            return f"禁止入库的目录：{path}"
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return f"禁止入库的文件类型：{path}"
    return None


def check_size(path: Path) -> str | None:
    try:
        size = path.stat().st_size
    except OSError:
        return None
    if size > MAX_BYTES:
        mb = size / 1024 / 1024
        return f"文件过大（{mb:.1f} MB > 10 MB）：{path}，请改用 Git LFS 或挂 Release 附件"
    return None


def check_secrets(path: Path) -> list[str]:
    key = path.as_posix()
    if key in SKIP_SCAN or path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                hits.append(f"疑似{label}：{path}:{lineno}")
    return hits


def main() -> int:
    staged = "--staged" in sys.argv[1:]
    files = tracked_files(staged=staged)
    if not files:
        print("✓ 无待检查文件")
        return 0

    problems: list[str] = []
    for path in files:
        for fn in (check_name, check_size):
            if msg := fn(path):
                problems.append(msg)
        problems.extend(check_secrets(path))

    if problems:
        print(f"✗ 发现 {len(problems)} 处违规：\n", file=sys.stderr)
        for msg in problems:
            print(f"  - {msg}", file=sys.stderr)
        print("\n处理方式：git rm --cached <文件>，并补进 .gitignore", file=sys.stderr)
        return 1

    print(f"✓ 检查通过：{len(files)} 个受控文件，无中间产物、密钥或超大文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
