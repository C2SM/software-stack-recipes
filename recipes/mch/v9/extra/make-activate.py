#!/usr/bin/python3
"""Generate bash activate scripts for uenv views.

    make-activate.py <mount> <view> <output> [<view> <output> ...]

Each output script applies the environment changes of the view described in
<mount>/meta/env.json: the same changes `uenv start --view=<view>` applies.
Sourcing one of them sets up the view when the image is mounted without uenv,
e.g. permanently at boot.

Unlike uenv, the scripts do not set UENV_VIEW, UENV_MOUNT_LIST, etc.: those
describe a uenv session, and would stop users from starting one.
"""

import json
import shlex
import sys


def prepend(var, value):
    return 'export %s=%s"${%s:+:$%s}"' % (var, value, var, var)


def append(var, value):
    return 'export %s="${%s:+$%s:}"%s' % (var, var, var, value)


def script(meta, mount, name):
    values = meta["views"][name]["env"]["values"]
    lines = [
        "# Source this file to set up the environment of the %s view of the %s uenv." % (name, meta["name"]),
        "# Equivalent to `uenv start --view=%s` with the image mounted at %s." % (name, mount),
        "# Generated from %s/meta/env.json by meta/extra/make-activate.py." % mount,
        "",
    ]

    for var, ops in sorted(values["list"].items()):
        for op in ops:
            value = shlex.quote(":".join(op["value"]))
            kind = op["op"]
            if kind == "prepend":
                lines.append(prepend(var, value))
            elif kind == "append":
                lines.append(append(var, value))
            elif kind == "set":
                lines.append("export %s=%s" % (var, value))
            elif kind == "unset":
                lines.append("unset %s" % var)
            else:
                sys.exit("unknown op '%s' for %s in view %s" % (kind, var, name))

    for var, value in sorted(values["scalar"].items()):
        if value is None:
            lines.append("unset %s" % var)
        else:
            lines.append("export %s=%s" % (var, shlex.quote(value)))

    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 4 or len(argv) % 2:
        sys.exit(__doc__)

    mount = argv[1]
    with open(mount + "/meta/env.json") as f:
        meta = json.load(f)

    for name, output in zip(argv[2::2], argv[3::2]):
        with open(output, "w") as f:
            f.write(script(meta, mount, name))
        print("wrote", output)


if __name__ == "__main__":
    main(sys.argv)
