#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

if env ls -1 | grep -E -o '[[:digit:]]+'; then
  # assuming it's sorted
  next="$(env ls -1 | grep -E -o '[[:digit:]]+' | tail -1 | xargs expr 1 '+')"
else
  # for the first one
  next='01'
fi

next_with_leading_zero="$(printf '%02d\n' "${next}")"

cp -r template "${next_with_leading_zero}"

cd "${next_with_leading_zero}"

rm ./README.md

sed -i 's/\[x\]/'"${next}/" part1.py
sed -i 's/\[x\]/'"${next}/" part2.py
