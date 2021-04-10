#!/usr/bin/env bash

set -euo pipefail

echo 'Starting PyPi server'
pypi-server -p 80 ./packages
