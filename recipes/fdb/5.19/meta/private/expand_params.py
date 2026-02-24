import argparse
import re 
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


def main():
    parser = argparse.ArgumentParser(description="Process two filenames.")
    parser.add_argument("paramids", type=str, help="Path to the first file")
    parser.add_argument("paramdefs", type=str, help="Path to the second file")
    
    args = parser.parse_args()

    # Convert the comma-separated string into a list
    paramdef_list = args.paramdefs.split(',')

    with open(args.paramids, 'r') as file:
        metkit_params = yaml.safe_load(file)

    for paramdef in paramdef_list:

        icon_params = parse_file(paramdef)

        for key in icon_params:
            if int(key) not in metkit_params:
                metkit_params[int(key)] = list(s.lower() for s in icon_params[key]) 

    with open(args.paramids, 'w') as file:
        yaml.dump(metkit_params, file, sort_keys=True, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    main()