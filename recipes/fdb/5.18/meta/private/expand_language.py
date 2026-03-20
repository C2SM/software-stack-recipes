import argparse
import yaml


def convert_nested_lists(obj):
    if isinstance(obj, dict):
        return {k: convert_nested_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If it's a list of lists, convert inner lists to tuples
        return [
            (
                tuple(convert_nested_lists(item))
                if isinstance(item, list)
                else convert_nested_lists(item)
            )
            for item in obj
        ]
    else:
        return obj


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


# Force tuples to be dumped in flow style
def tuple_representer(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


def main():
    parser = argparse.ArgumentParser(
        description="expand the metkit language.yaml for the meteoswiss mars model"
    )
    parser.add_argument("langyaml", type=str, help="Path to the first file")

    args = parser.parse_args()

    with open(args.langyaml, "r") as file:
        metkit_lang = yaml.safe_load(file)

    metkit_lang["_field"]["model"]["type"].append(
        {
            "type": "enum",
            "values": [["icon-ch1-eps"], ["icon-ch2-eps"], ["icon-rea-l-ch1"]],
        }
    )

    metkit_lang["_field"]["stream"]["values"].append(
        ["reanl", "icon reanalysis light CH1"]
    )

    yaml.add_representer(tuple, tuple_representer, Dumper=NoAliasDumper)
    # convert list to tuples so that the yaml dump generates [] (original formatting of the yaml) instead of rows of "-"
    metkit_lang = convert_nested_lists(metkit_lang)

    with open(args.langyaml, "w") as file:
        yaml.dump(
            metkit_lang,
            file,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            Dumper=NoAliasDumper,
            width=float("inf"),
        )


if __name__ == "__main__":
    main()
