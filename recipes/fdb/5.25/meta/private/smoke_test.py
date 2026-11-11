"""Smoke test of the Python stack in the uenv.

Run it in each view after a build:
    uenv run --view=<view> fdb/5.25:<tag> -- python /user-environment/meta/recipe/meta/private/smoke_test.py

Fails if an import or a basic operation fails, or if a library of the uenv is loaded
more than once (for example also as a copy from a wheel).
"""

import os
import re
import sys
import tempfile

# eccodes is imported last on purpose (APNRZ-998)
import pyfdb  # noqa: F401
import pygribjump  # noqa: F401
import eckit.geo  # noqa: F401
import mir
import pyproj
import earthkit.data  # noqa: F401
import earthkit.geo  # noqa: F401
import eccodes

pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2056").transform(46.95, 7.44)

sample = os.path.join(eccodes.codes_samples_path(), "regular_ll_sfc_grib2.tmpl")
with tempfile.NamedTemporaryFile(suffix=".grib") as output:
    mir.Job(grid="1/1").execute(mir.GribFileInput(sample), mir.GribFileOutput(output.name))

# Wheels can bundle their own copies of a library (e.g. numpy and scipy), that is allowed.
# A library of the uenv must be loaded only once, and not also as a wheel copy.
loaded = {}
for line in open("/proc/self/maps"):
    path = line.split()[-1]
    name = re.match(r"(lib[\w+]+?)(-[0-9a-f]{8})?\.so", os.path.basename(path))
    if name:
        loaded.setdefault(name.group(1), set()).add(path)
duplicates = {lib: paths for lib, paths in loaded.items() if len(paths) > 1 and any("site-packages" not in p for p in paths)}

for lib, paths in sorted(duplicates.items()):
    print(f"{lib} is loaded more than once: {', '.join(sorted(paths))}")
if duplicates:
    sys.exit("SMOKE TEST FAILED")
print("SMOKE TEST PASSED")
