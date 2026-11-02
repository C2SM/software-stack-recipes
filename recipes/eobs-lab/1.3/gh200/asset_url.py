"""Print the API url of a GitHub release asset, picked by name suffix.

Usage: asset_url.py <release-json> <asset-name-suffix>

The API url is the one that accepts a token; on a private repo the
browser-facing releases/download/... url does not.
"""

import json
import sys

release_json, suffix = sys.argv[1], sys.argv[2]

with open(release_json) as f:
    assets = json.load(f)["assets"]

matches = [asset for asset in assets if asset["name"].endswith(suffix)]
if not matches:
    sys.exit(f"no release asset ends in '{suffix}' "
             f"(found: {', '.join(asset['name'] for asset in assets)})")
if len(matches) > 1:
    sys.exit(f"'{suffix}' matches several assets: "
             f"{', '.join(asset['name'] for asset in matches)}")

print(matches[0]["url"])
