#!/usr/bin/env python3
import json
import re
import sys

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker, StdinStream
from antlr4.tree.Tree import TerminalNodeImpl
from AdvLexer import AdvLexer
from AdvParser import AdvParser


RULE_NAMES = []


def get_rule_name(tree):
    return RULE_NAMES[tree.getRuleIndex()]


def is_terminal(tree):
    return isinstance(tree, TerminalNodeImpl)


def parse_script(tree: AdvParser.ScriptContext):
    return traverse(tree)


def parse_json(tree: AdvParser.JsonContext):
    json_text = tree.getText()
    json_text = re.sub("\\\{", "{", json_text)
    json_text = re.sub("\\\}", "}", json_text)
    return {
        "typ": "json",
        "obj": json.loads(json_text)
    }


def parse_line(tree: AdvParser.LineContext):
    child = list(tree.getChildren())[0]
    rule = get_rule_name(child)
    if rule == "title_item":
        return parse_title_item(child)
    elif rule == "item":
        return parse_item(child)


def parse_item(tree: AdvParser.ItemContext):
    children = list(tree.getChildren())
    ret = {
        "typ": "item",
        "org": {
            "name": children[1].getText(),
            "props": list(map(get_key_value, children[2:-1]))
        }
    }
    return ret


def parse_title_item(tree: AdvParser.Title_itemContext):
    children = list(tree.getChildren())
    return {
        "typ": "title_item",
        "title": " ".join(list(map(lambda x: x.getText(), children[4:-1])))
    }


def get_key_value(tree: AdvParser.Key_valueContext):
    children = list(tree.getChildren())
    return {
        "key": children[0].getText(),
        "value": get_value(children[2])
    }


def get_value(tree: AdvParser.ValueContext):
    child = tree.getChild(0)
    if isinstance(child, TerminalNodeImpl):
        return {
            "typ": "txt",
            "txt": child.getText()
        }
    rule = get_rule_name(child)
    if rule == "item":
        return parse_item(child)
    elif rule == "json":
        return parse_json(child)


RULE_MAP = {
    'script': parse_script,
    'line': parse_line,
    'item': parse_item,
    'title_item': parse_title_item
}


def traverse(tree):
    if isinstance(tree, TerminalNodeImpl):
        print("[ERR] Reaching raw string")
        return None
    ret = []
    for i in tree.getChildren():
        if is_terminal(i):
            print("[ERR] Reaching raw string within children")
            ret.append(None)
        typ = get_rule_name(i)
        if typ in RULE_MAP:
            try:
                here = RULE_MAP[typ](i)
            except Exception as e:
                print("[Exception]", e, file=sys.stderr)
                print("[Exception]", "Line:", i.getText(), file=sys.stderr)
                print("[Exception]", "Rule:", typ,
                      RULE_MAP[typ], file=sys.stderr)
                print("[Exception]", "Components:", list(
                    i.getChildren()), file=sys.stderr)
                sys.exit(1)
            ret.append(here)
        else:
            print("[ERR] Rule not found:", typ)
            ret.append(None)
    return ret


def main():
    global RULE_NAMES
    # To use STDIN
    input_stream = StdinStream(encoding='utf-8')
    # To use file
    # filename = sys.argv[1]
    # input_stream = FileStream(filename, encoding='utf-8')
    lexer = AdvLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AdvParser(stream)
    tree = parser.script()
    RULE_NAMES = parser.ruleNames
    # print("All rules:", RULE_NAMES, file=sys.stderr)

    ret = traverse(tree)
    print(json.dumps(ret, ensure_ascii=False))


if __name__ == "__main__":
    main()
