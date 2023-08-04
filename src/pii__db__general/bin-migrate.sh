#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit
set -o pipefail
set -o nounset



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../../
CWD="$(pwd)"


# ENV
# ======================================================================================================

export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"
export FLASK_APP="${CWD}/src/pii__db__general/manager.py"

sleep 3

MIGRATIONS_DIR="${CWD}/src/pii__db__general/migrations"

case "$1" in
  --init)
    flask db init --directory "${MIGRATIONS_DIR}"
    ;;
  --migrate)
    flask db migrate --directory "${MIGRATIONS_DIR}"
    ;;
  --upgrade)
    flask db upgrade --directory "${MIGRATIONS_DIR}"
    ;;
  --downgrade)
    flask db downgrade --directory "${MIGRATIONS_DIR}"
    ;;
  --revision)
    flask db revision --directory "${MIGRATIONS_DIR}"
    ;;
  *)
    echo "Error: Unsupported flag $1" >&2
    exit 1
    ;;
esac
