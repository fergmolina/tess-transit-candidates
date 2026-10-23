#!/bin/bash
# Round-5 TRICERATOPS on the triage survivors (in-sample local QLP sectors only; default = last 3 local sectors)
cd /Users/fernando/Desktop/NASA
for t in 240488148 372343190 13450993; do
  echo "start $t $(date -u +%H:%M)"; .venv_tri/bin/python -I scripts/triceratops_qlp.py $t > logs/tri_round5_$t.log 2>&1; echo "done $t exit $? $(date -u +%H:%M)"
done
echo "tri runner finished $(date -u)"
