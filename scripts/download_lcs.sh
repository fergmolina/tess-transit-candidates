#!/bin/sh
# Parallel download of SPOC 2-min light curves listed in data/lc_download_list.tsv (url<TAB>filename)
cd /Users/fernando/Desktop/NASA/data/lc || exit 1
awk -F'\t' '{print $2"\t"$1}' /Users/fernando/Desktop/NASA/data/lc_download_list.tsv | while IFS=$'\t' read -r fn url; do
  [ -s "$fn" ] || echo "$url -o $fn"
done > /tmp/claude-501/curl_jobs.txt 2>/dev/null || true
