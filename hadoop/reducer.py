#!/usr/bin/env python3
import sys

current_profession = None
current_count = 0

for line in sys.stdin:
    profession, count = line.strip().split("\t")
    count = int(count)

    if current_profession == profession:
        current_count += count
    else:
        if current_profession:
            print(f"{current_profession}\t{current_count}")
        current_profession = profession
        current_count = count

if current_profession:
    print(f"{current_profession}\t{current_count}")
