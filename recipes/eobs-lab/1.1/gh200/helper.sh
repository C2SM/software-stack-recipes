#!/bin/bash
# Helper functions for this recipe's post-install, which sources this file
# from the copy of the recipe directory stackinator makes inside the build.

NARTHEX_HELPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Download one asset of a GitHub release, picked by the suffix of its file
# name.
#
#   $1  asset name suffix, e.g. narthex-launcher.tar.bz2 or .whl
#   $2  where to write it
#
# Expects NARTHEX_RELEASE_JSON (the release metadata, already fetched) and
# EOBS_GH_TOKEN in the environment.
narthex_fetch() {
    local url
    url=$(python3 "${NARTHEX_HELPER_DIR}/asset_url.py" \
        "${NARTHEX_RELEASE_JSON}" "$1")
    curl -LsSf \
        -H "Authorization: token ${EOBS_GH_TOKEN}" \
        -H "Accept: application/octet-stream" \
        "${url}" -o "$2"
}
