#!/bin/sh
if [[ ! -e snapshot.json ]]; then
  echo "Snapshot file not found"
  exit 1
fi

gunicorn -w 4 -b 0.0.0.0:8586 'main:app'
