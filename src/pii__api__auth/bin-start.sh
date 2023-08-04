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


# ARGS
# ======================================================================================================
APPLICATION_WORKERS="${APPLICATION_WORKERS:-*}"
APPLICATION_PORT="${APPLICATION_PORT:-5005}"
APP_MODULE="src.pii__api__auth.app"

if [ "${APPLICATION_WORKERS}" == "*" ]; then
  APPLICATION_WORKERS=$(expr 1 + $(grep -c ^processor /proc/cpuinfo))
fi


# ENV
# ======================================================================================================
export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"
export FLASK_APP="${CWD}/src/pii__api__auth/app.py"


# START
# ======================================================================================================
gunicorn -w ${APPLICATION_WORKERS} --timeout 120 ${APP_MODULE}:app -b 0.0.0.0:${APPLICATION_PORT} --capture-output --reload
