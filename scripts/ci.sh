#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
sh scripts/setup.sh
sh scripts/check.sh
