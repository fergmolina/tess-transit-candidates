#!/bin/zsh
# Run vet.py on every row of results/allsky_classA.csv, N at a time. Usage: vet_runner.sh [N]
cd /Users/fernando/Desktop/NASA; N=${1:-3}
export TSEARCH_SOURCE=qlp TSEARCH_LC_DIR=/Users/fernando/Desktop/NASA/data/qlp_allsky TSEARCH_SUFFIX=_allsky
tail -n +2 results/allsky_classA.csv | while IFS=, read tic P T0 dur depth sde nxt dl; do
  [ -f results/vet_allsky/$tic/report.json ] && continue
  echo "$tic $P $T0 $dur"
done | xargs -n 4 -P $N sh -c 'echo "start $0 $(date -u +%H:%M)"; .venv/bin/python -I scripts/vet.py $0 $1 $2 $3 > logs/vet_allsky_$0.log 2>&1; echo "done $0 $(date -u +%H:%M) exit $?"'
echo "runner finished $(date -u)"
