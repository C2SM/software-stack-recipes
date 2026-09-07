import argparse
import collections
import re
import sys
import yaml


# Priority for shortNames that map to more than one paramId.
SHORTNAME_PRIORITY = {
    "asob_s": 500078,     # alt 500421
    "athb_s": 500080,     # alt 500422
    "cdct": 502775,       # alt 502771
    "clch": 502341,       # alt 500050 (REA-L-CH1)
    "clcl": 502343,       # alt 500048 (REA-L-CH1)
    "clcm": 502342,       # alt 500049 (REA-L-CH1)
    "edp": 503675,        # alt 500585
    "runoff_g": 502349,   # alt 500066 (REA-L-CH1)
    "runoff_s": 502348,   # alt 500068 (REA-L-CH1)
    # More shortNames with two cosmo paramIds, currently not in ingested data
    #   "asob_t":          500082 / 500419
    #   "athb_t":          500084 / 500420
    #   "denc":            503126 / 503322
    #   "deng":            503125 / 503321
    #   "denh":            503128 / 503324
    #   "deni":            503127 / 503323
    #   "denr":            503123 / 503319
    #   "dens":            503124 / 503320
    #   "ncgraupel":       503118 / 503314
    #   "nchail":          503119 / 503315
    #   "ncrain":          503115 / 503311
    #   "ncsnow":          503117 / 503313
    #   "ndgraupel":       503121 / 503317
    #   "ndhail":          503122 / 503318
    #   "ndrain":          503116 / 503312
    #   "ndsnow":          503120 / 503316
    #   "radionuc_ac_vi":  503282 / 503326
    #   "sm":              500548 / 500549
    #   "tsec":            502864 / 502942
}


def parse_file(filepath):
    entries = {}

    with open(filepath, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        # Look for lines with paramId
        param_match = re.match(r"#paramId:\s*(\d+)", lines[i])
        if param_match:
            param_id = param_match.group(1)
            description = lines[i + 1].strip().lstrip("#").strip()
            key_match = re.match(r"'([^']+)'", lines[i + 2])
            key = key_match.group(1) if key_match else ""
            entries[param_id] = ((key, description))

    return entries


def preferred_order(params, cosmo_shortname, priority):
    """Order paramIds so the preferred paramId wins a shortName clash.

    metkit keeps the first paramId it reads for a shortName. Set the first entry based on:
      1. the paramId in SHORTNAME_PRIORITY, if the shortName is listed;
      2. else the single cosmo paramId that owns the shortName;
      3. else undefined (metkit keeps the smaller paramId).
    """
    ids = [k for k in params if isinstance(k, int)]

    # shortName -> paramIds (first list element is the shortName)
    by_shortname = collections.defaultdict(list)
    for pid in ids:
        entry = params[pid]
        if isinstance(entry, list) and entry:
            by_shortname[str(entry[0]).lower()].append(pid)

    # shortName -> cosmo paramIds
    cosmo_by_shortname = collections.defaultdict(list)
    for pid, name in cosmo_shortname.items():
        cosmo_by_shortname[name].append(pid)

    for name, chosen in priority.items():
        pids = by_shortname.get(name)
        if not pids:
            print(f"WARNING: SHORTNAME_PRIORITY['{name}'] = {chosen}: "
                  f"unknown shortName; ignored.", file=sys.stderr)
        elif chosen not in pids:
            print(f"WARNING: SHORTNAME_PRIORITY['{name}'] = {chosen} "
                  f"is not a paramId of '{name}' {sorted(set(pids))}; ignored.",
                  file=sys.stderr)

    winners = set()
    for name, pids in by_shortname.items():
        if len(set(pids)) < 2:
            continue  # no clash

        if name in priority and priority[name] in pids:
            winners.add(priority[name])
            continue

        cosmo_ids = [p for p in cosmo_by_shortname.get(name, []) if p in pids]
        if len(cosmo_ids) == 1:
            winners.add(cosmo_ids[0])  # one cosmo owner -> prefer it

    rest = [p for p in ids if p not in winners]
    return sorted(winners) + sorted(rest)


def main():
    parser = argparse.ArgumentParser(description="Process two filenames.")
    parser.add_argument("paramids", type=str, help="Path to the first file")
    parser.add_argument("paramdefs", type=str, help="Path to the second file")

    args = parser.parse_args()

    # Convert the comma-separated string into a list
    paramdef_list = args.paramdefs.split(',')

    with open(args.paramids, 'r') as file:
        metkit_params = yaml.safe_load(file)

    # shortName of every cosmo paramId (first file wins per paramId)
    cosmo_shortname = {}

    for paramdef in paramdef_list:

        icon_params = parse_file(paramdef)

        for key in icon_params:
            pid = int(key)
            cosmo_shortname.setdefault(pid, icon_params[key][0].lower())
            if pid not in metkit_params:
                metkit_params[int(key)] = list(s.lower() for s in icon_params[key])

    priority = {k.lower(): v for k, v in SHORTNAME_PRIORITY.items()}

    # Reorder so the preferred paramId wins a shortName clash
    order = preferred_order(metkit_params, cosmo_shortname, priority)
    ordered = {pid: metkit_params[pid] for pid in order}

    with open(args.paramids, 'w') as file:
        yaml.dump(ordered, file, sort_keys=False, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()
