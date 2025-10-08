"""
Convert ICON short names to their corresponding paramIds.

Provides `var_to_paramid(names)` for mapping ICON short names
(e.g. 'ASOB_S', 'CLCM') to paramIds used in the rea-l-ch1 environment.

Uses the fixed table:
    /user-environment/env/rea-l-ch1/share/metkit/paramids.yaml
extended with our custom ICON parameter definitions.

Includes only local parameters (paramId ≥ 500000) and applies a few
overrides for shortNames that have multiple paramIds, matching the
metadata found in the REA-L-CH1 dataset.

Example:
    >>> from uenv_param_map import var_to_paramid
    >>> var_to_paramid(["ASOB_S", "CLCM"])
    [500078, 500049]
"""

import yaml

# For shortNames with multiple paramIds, use the paramIds used in the REA-L-CH1 dataset.
_OVERRIDES = {
    "clcl": 500048,
    "clch": 500050,
    "asob_s": 500078,
    "athb_s": 500080,
    "runoff_g": 500066,
    "runoff_s": 500068,
    "clcm": 500049,
}

# Absolute path to the paramId table used by this environment.
_PARAMIDS_PATH = "/user-environment/env/rea-l-ch1/share/metkit/paramids.yaml"


def _load_table() -> dict:
    """Load the paramId table from the paramids YAML file."""
    with open(_PARAMIDS_PATH, "r") as f:
        return yaml.safe_load(f) or {}

def _build_map(table: dict, min_pid: int = 500000) -> dict:
    """
    Build a mapping of short names to paramIds for the REA-L-CH1 dataset.

    This function filters the entries from `paramids.yaml` to include only
    local parameters (paramId >= min_pid). Some shortNames appear with
    multiple paramIds in the ICON definitions; for those, the mapping
    is overridden with the paramIds actually used in the REA-L-CH1 dataset.

    Args:
        table (dict): Contents of the paramids.yaml file.
        min_pid (int, optional): Minimum paramId to include. Defaults to 500000.

    Returns:
        dict: Mapping of lowercase shortName -> paramId (int), aligned with REA-L-CH1.
    """
    mapping = {}

    for pid_str, values in table.items():
        try:
            pid = int(pid_str)
        except (TypeError, ValueError):
            continue

        # Only include local parameter IDs (>= 500000)
        if pid < min_pid or not isinstance(values, (list, tuple)) or not values:
            continue

        shortname = str(values[0]).lower()
        if shortname and shortname not in mapping:
            mapping[shortname] = pid

    # Apply overrides for shortNames with multiple paramIds (use REA-L-CH1 metadata)
    mapping.update(_OVERRIDES)
    return mapping


def var_to_paramid(names: list[str]) -> list[int]:
    """
    Convert a list of ICON short names to their corresponding paramIds.

    Args:
        names (list[str]): List of short names (e.g. ['ASOB_S', 'CLCM']).

    Returns:
        list[int]: List of corresponding paramIds.

    Raises:
        KeyError: If any short name is not found in the mapping.
    """
    table = _load_table()
    mapping = _build_map(table)

    missing = [n for n in names if n.lower() not in mapping]
    if missing:
        raise KeyError(f"Short names not found in param mapping: {missing}")

    return [mapping[n.lower()] for n in names]
