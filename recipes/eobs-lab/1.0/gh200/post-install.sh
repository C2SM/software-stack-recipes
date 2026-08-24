#!/bin/bash

EOBS_LAB_VIEW="eobs-lab"

# -----------------------------------------------
# Install uv

UV_INSTALL_DIR="{{ env.mount }}/uv"
mkdir -p "${UV_INSTALL_DIR}"

curl -LsSf https://astral.sh/uv/install.sh > uv-installer.sh
UV_INSTALL_DIR="${UV_INSTALL_DIR}" sh uv-installer.sh
rm uv-installer.sh

# -----------------------------------------------
# Install the analysis / notebook packages

UV="${UV_INSTALL_DIR}/uv"
EOBS_LAB_VENV="{{ env.mount }}/eobs-lab_venv"

# Create venv
${UV} venv --relocatable --python="{{ env.mount }}/env/${EOBS_LAB_VIEW}/bin/python" ${EOBS_LAB_VENV}
source ${EOBS_LAB_VENV}/bin/activate

# Install packages
${UV} pip install --no-cache \
    jupyterlab \
    pandas \
    geopandas \
    pillow \
    seaborn \
    netcdf4

# Cleanup
rm -rf ${UV_INSTALL_DIR}

# Install in "eobs-lab" view
echo "source ${EOBS_LAB_VENV}/bin/activate" >> {{ env.mount }}/env/${EOBS_LAB_VIEW}/activate.sh
