#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    data = json.loads(line)
    deputes = data.get("deputes", [])
    for item in deputes:
        depute = item.get("depute", {})
        profession = depute.get("profession", "Inconnue")
        print(f"{profession}\t1")
