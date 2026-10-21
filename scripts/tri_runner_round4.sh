#!/bin/bash
# Round-4 TRICERATOPS on the triage survivors (in-sample local QLP sectors only; default = last 3 local sectors)
cd /Users/fernando/Desktop/NASA
for t in 343298093 188664994 195343302 151767028; do
  echo "start $t $(date -u +%H:%M)"; .venv_tri/bin/python -I scripts/triceratops_qlp.py $t > logs/tri_round4_$t.log 2>&1; echo "done $t exit $? $(date -u +%H:%M)"
done
echo "tri runner finished $(date -u)"
