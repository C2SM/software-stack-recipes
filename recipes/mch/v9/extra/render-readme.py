#!/usr/bin/python3
"""Render a markdown-lite README with ANSI colours, so that `cat README` is readable.

    render-readme.py <input> <output>

Markup understood:
    # title, ## heading
    `code`, **bold**
    $ command lines, continued onto the next line by a trailing \\
    box-drawing tables (written out in full in the input)
"""

import re
import sys

ESC = "\x1b["
RESET = ESC + "0m"
BOLD = ESC + "1m"
DIM = ESC + "2m"
TITLE = ESC + "1;36m"
HEADING = ESC + "1;33m"
CODE = ESC + "36m"
CMD = ESC + "32m"


def inline(text):
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: BOLD + m.group(1) + RESET, text)
    text = re.sub(r"`([^`]+)`", lambda m: CODE + m.group(1) + RESET, text)
    return text


def render(lines):
    out = []
    continued = False
    for line in lines:
        if line.startswith("$ ") or continued:
            # shell commands, with trailing comments dimmed
            cmd, sep, comment = line.partition("  #")
            out.append("  " + CMD + cmd + RESET + (DIM + sep + comment + RESET if sep else ""))
            continued = line.endswith("\\")
        elif line.startswith("# "):
            title = line[2:]
            out += [TITLE + title + RESET, DIM + "═" * len(title) + RESET]
        elif line.startswith("## "):
            heading = line[3:]
            out += [HEADING + heading + RESET, DIM + "─" * len(heading) + RESET]
        elif line[:1] and line[0] in "┌├└":
            out.append(DIM + line + RESET)
        elif line.startswith("│"):
            out.append((DIM + "│" + RESET).join(line.split("│")))
        else:
            out.append(inline(line))
    return out


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    with open(argv[1]) as f:
        out = render(f.read().splitlines())
    with open(argv[2], "w") as f:
        f.write("\n".join(out) + "\n")
    print("wrote", argv[2])


if __name__ == "__main__":
    main(sys.argv)
