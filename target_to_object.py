#!/usr/bin/env python3
import json
from sys import stdin

GLOBAL_PROPS = {}


def disp_item(item):
    return {
        "name": item["name"],
        "props": parse_props(item["props"])
    }


def parse_props(props):
    ret = {}
    for i in props:
        key = i["key"]
        value_type = i["value"]["typ"]
        if value_type == "txt":
            val = i["value"]["txt"]
        elif value_type == "json":
            val = i["value"]["obj"]
        elif value_type == "item":
            val = disp_item(i["value"]["org"])
        else:
            raise TypeError
        ret[key] = val
    return ret


def parse(item):
    global GLOBAL_PROPS
    if item["typ"] == "title_item":
        GLOBAL_PROPS["title"] = item["title"]
        return None
    if item["typ"] == "item":
        return disp_item(item["org"])


def main():
    file = json.load(stdin)
    ret = []
    for i in file:
        local_ret = parse(i)
        if local_ret is not None:
            ret.append(local_ret)
    print(
        json.dumps({
            "meta": GLOBAL_PROPS,
            "data": ret
        }, ensure_ascii=False)
    )


if __name__ == "__main__":
    main()
