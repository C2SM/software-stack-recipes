import argparse
import collections
import re
import sys
import yaml


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
      1. the paramId in the priority file, if the shortName is listed;
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
            print(f"WARNING: priority '{name}' = {chosen}: "
                  f"unknown shortName; ignored.", file=sys.stderr)
        elif chosen not in pids:
            print(f"WARNING: priority '{name}' = {chosen} "
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
    parser.add_argument("--priority", type=str, default=None,
                        help="YAML file with 'shortName: paramId' entries. Sets "
                             "which paramId wins when a shortName has several.")

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

    # per-view priorities; empty means cosmo-preference only
    priority = {}
    if args.priority:
        with open(args.priority, 'r') as file:
            priority = {k.lower(): v for k, v in (yaml.safe_load(file) or {}).items()}

    # Reorder so the preferred paramId wins a shortName clash
    order = preferred_order(metkit_params, cosmo_shortname, priority)
    ordered = {pid: metkit_params[pid] for pid in order}

    with open(args.paramids, 'w') as file:
        yaml.dump(ordered, file, sort_keys=False, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()
