#!/bin/bash
exec "$@" --init-file <(echo "source /workspace/pykitti/bin/activate")