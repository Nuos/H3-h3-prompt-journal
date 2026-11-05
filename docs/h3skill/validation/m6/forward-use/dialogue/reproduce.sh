#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHONDONTWRITEBYTECODE=1 python -B run_trial.py
PYTHONDONTWRITEBYTECODE=1 python -B revise_and_finish.py
