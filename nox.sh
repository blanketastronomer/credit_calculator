#!/usr/bin/env bash

nox --no-reuse-existing-virtualenvs --noxfile "$(dirname "$0")/noxfile.py" --non-interactive
