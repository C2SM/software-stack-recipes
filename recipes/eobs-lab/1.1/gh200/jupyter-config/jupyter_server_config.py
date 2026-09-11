# Config for whatever jupyter server serves a launched notebook. post-install
# copies this directory to {mount}/jupyter/etc/jupyter, which the lab view
# puts on JUPYTER_CONFIG_PATH -- the only way into that server, since on
# jupyter-santis it is the Hub's own jupyterlab uenv at /user-tools and not
# anything this image starts.
import os

# `c` is injected by jupyter's config loader; get_config() returns that same
# object -- the official idiom for a file the server exec's, never runs.
c = get_config()  # noqa: F821

# ipywidgets 8 pulls in jupyterlab_widgets, its JupyterLab frontend, as a
# prebuilt labextension under the venv's share/jupyter/labextensions -- so it
# is already in this image, nothing needs installing. But that frontend is
# served by the Hub's jupyterlab uenv, not by the venv the kernel runs in,
# and a server only scans the labextension directories on its *own* data
# path, which never includes this venv. Without this every widget degrades to
# its text repr -- a Dropdown prints `Dropdown(description=..., options=...)`
# instead of rendering -- and nothing anywhere reports an error.
#
# extra_labextensions_path and not a JUPYTER_PATH entry: it is scoped to
# labextensions, where widening the server's whole data path would also hand
# that server this venv's kernelspecs.
#
# VIRTUAL_ENV comes from the view (environments.yaml). The fallback, for a
# server started without it, is this file's own location rather than a
# hardcoded mount point: traitlets sets __file__ to the full path of the
# config file it is exec'ing, and this file is installed three directories
# below the mount ({mount}/jupyter/etc/jupyter/), beside {mount}/venv.
_venv = os.environ.get("VIRTUAL_ENV") or os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "venv"
    )
)
c.LabApp.extra_labextensions_path = [
    os.path.join(_venv, "share", "jupyter", "labextensions")
]
