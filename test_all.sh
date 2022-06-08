#!/bin/bash
set -u

v=0

for i in ./adv/*.txt; do
    echo $i
    cat $i | python main.py | python target_to_object.py >/dev/null
done
