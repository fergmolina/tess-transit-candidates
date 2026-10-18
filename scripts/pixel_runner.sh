#!/bin/bash
# Run ffi_pixel_test.py for a list of TICs (args), using each star's vet_allsky report for P/T0/dur and its three latest 200-s QLP sectors.
cd /Users/fernando/Desktop/NASA; export TSEARCH_SOURCE=qlp TSEARCH_LC_DIR=/Users/fernando/Desktop/NASA/data/qlp_allsky TSEARCH_SUFFIX=_allsky
for tic in "$@"; do
  [ -f results/vet_allsky/$tic/report.json ] || { echo "no report for $tic"; continue; }
  SECS=$(ls data/qlp_allsky/ | grep "0*${tic}_" | sed 's/.*_s\([0-9]*\)-.*/\1/' | sed 's/^0*//' | awk '$1>=56' | tail -3 | tr '\n' ' ')
  [ -z "$SECS" ] && { echo "no 200-s sectors for $tic"; continue; }
  P=$(.venv/bin/python -I -c "import json;r=json.load(open('results/vet_allsky/$tic/report.json'));b=r['bls_refine'];print(b['period'],b['T0'],b['duration_h'])")
  echo "start $tic sectors $SECS $(date -u +%H:%M)"
  .venv/bin/python -I scripts/ffi_pixel_test.py $tic $P --sectors $SECS > logs/ffi_pixel_$tic.log 2>&1
  mkdir -p results/vet_allsky/$tic; cp results/vet_qlp/$tic/ffi_pixel_S* results/vet_allsky/$tic/ 2>/dev/null
  echo "done $tic: $(grep -v -i warn logs/ffi_pixel_$tic.log | grep '^S' | sed 's/; depth vs r.*//' | tr '\n' '|')"
done
echo "pixel runner finished $(date -u)"
